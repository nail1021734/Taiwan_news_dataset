import argparse
import gc
import sys
import textwrap
from typing import Callable, Dict, List

from tqdm import trange

import news.crawlers.db.read
import news.crawlers.db.util
import news.crawlers.util.normalize
import news.db
import news.parse.chinatimes
import news.parse.cna
import news.parse.db.create
import news.parse.db.util
import news.parse.db.write
import news.parse.epochtimes
import news.parse.ettoday
import news.parse.ftv
import news.parse.ltn
import news.parse.ntdtv
import news.parse.setn
import news.parse.storm
import news.parse.tvbs
import news.parse.udn
import news.path
from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

PARSER_LOOKUP_TABLE: Dict[int, Callable[[RawNews], ParsedNews]] = {
    news.crawlers.util.normalize.get_company_id(company='中時'):
        news.parse.chinatimes.parser,
    news.crawlers.util.normalize.get_company_id(company='中央社'):
        news.parse.cna.parser,
    news.crawlers.util.normalize.get_company_id(company='大紀元'):
        news.parse.epochtimes.parser,
    news.crawlers.util.normalize.get_company_id(company='東森'):
        news.parse.ettoday.parser,
    news.crawlers.util.normalize.get_company_id(company='民視'):
        news.parse.ftv.parser,
    news.crawlers.util.normalize.get_company_id(company='自由'):
        news.parse.ltn.parser,
    news.crawlers.util.normalize.get_company_id(company='新唐人'):
        news.parse.ntdtv.parser,
    news.crawlers.util.normalize.get_company_id(company='三立'):
        news.parse.setn.parser,
    news.crawlers.util.normalize.get_company_id(company='風傳媒'):
        news.parse.storm.parser,
    news.crawlers.util.normalize.get_company_id(company='tvbs'):
        news.parse.tvbs.parser,
    news.crawlers.util.normalize.get_company_id(company='聯合報'):
        news.parse.udn.parser,
}

# List lookup with index is O(1).
PARSER_FASTEST_LOOKUP_TABLE: List[Callable[[RawNews], ParsedNews]] = [
    PARSER_LOOKUP_TABLE[company_id]
    for company_id in sorted(PARSER_LOOKUP_TABLE.keys())
]


def parse_args(argv: List[str]) -> argparse.Namespace:
    r"""Parse command line arguments.

    Example
    =======
    python -m news.parse.main \
        --batch_size 1000     \
        --db_name rel/my.db   \
        --db_name /abs/my.db  \
        --db_dir rel_dir      \
        --db_dir /abs_dir     \
        --debug               \
        --save_db_name out.db
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        '--batch_size',
        type=int,
        default=1000,
        help=textwrap.dedent(
            """\
            Parsing batch size.  Normally database containing `RawNews` records
            will consume large memories.  Thus we will parse `RawNews` by batch
            with each batch has `--batch_size` number of records.
            """
        ),
    )
    parser.add_argument(
        '--db_name',
        action='append',
        type=str,
        help=textwrap.dedent(
            f"""\
            SQLite database file name wanted to parse.  If absolute path is
            given, then treat the given path as database file and read records
            directly from the given path.

            For example, excuting

                --db_name /abs/my.db

            will collect the file

                /abs/my.db

            If relative path is given, then we assume the given path is under
            the path `PROJECT_ROOT/data/raw`.  Currently project root is set to
            {news.path.PROJECT_ROOT}.

            For example, executing

                --db_name rel/my.db

            will collect the file

                PROJECT_ROOT/data/raw/rel/my.db

            One can specify multiple database files at the same time using
            multiple `--db_name`.

            For example, executing

                --db_name rel/a.db --db_name rel/b.db --db_name /abs/c.db

            will collect all the following files

                PROJECT_ROOT/data/raw/rel/a.db
                PROJECT_ROOT/data/raw/rel/b.db
                /abs/c.db
            """
        ),
    )
    parser.add_argument(
        '--db_dir',
        action='append',
        type=str,
        help=textwrap.dedent(
            f"""\
            Directory contains SQLite database files.  If absolute path is
            given, then recursively search the directory to find all sqlite
            database files.

            For example, if `/abs/dir` contains

                a.db
                b.db
                subdir/c.db
                subdir/d.db

            then executing

                --db_dir /abs/dir

            will collect all the following files

                /abs/dir/a.db
                /abs/dir/b.db
                /abs/dir/subdir/c.db
                /abs/dir/subdir/d.db

            If relative path is given, then we assume the given directory is
            under the path `PROJECT_ROOT/data/raw`.  Currently project root is
            set to {news.path.PROJECT_ROOT}.

            For example, if `PROJECT_ROOT/data/raw/rel/dir` contains

                a.db
                b.db
                subdir/c.db
                subdir/d.db

            then executing

                --db_dir rel/dir

            will collect all the following files

                PROJECT_ROOT/data/raw/rel/dir/a.db
                PROJECT_ROOT/data/raw/rel/dir/b.db
                PROJECT_ROOT/data/raw/rel/dir/subdir/c.db
                PROJECT_ROOT/data/raw/rel/dir/subdir/d.db

            One can specify multiple directory at the same time using multiple
            `--db_dir`.

            Continue from previouse example, excuting

                --db_dir rel/dir --db_dir /abs/dir

            will collect all the following files

                /abs/dir/a.db
                /abs/dir/b.db
                /abs/dir/subdir/c.db
                /abs/dir/subdir/d.db
                PROJECT_ROOT/data/raw/rel/dir/a.db
                PROJECT_ROOT/data/raw/rel/dir/b.db
                PROJECT_ROOT/data/raw/rel/dir/subdir/c.db
                PROJECT_ROOT/data/raw/rel/dir/subdir/d.db
            """
        ),
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help=textwrap.dedent(
            """\
            Select whether to use debug mode.  In debug mode it outputs
            progress bar to stderr and error messages to stdout.
            """
        ),
    )
    parser.add_argument(
        '--save_db_name',
        type=str,
        required=True,
        help=textwrap.dedent(
            f"""\
            Name of the database to save parsing results.  Create file if given
            path does not exist (along with non-existed directories in the
            path).  If absolute path is given, then treat the given path as
            SQLite database file.

            For example, executing

                --save_db_name /abs/my.db

            will output parsed news to the file

                /abs/my.db

            If relative path is given, then we assume the given path is under
            the path `PROJECT_ROOT/data/parsed`. Currently project root is set
            to {news.path.PROJECT_ROOT}.

            For example, executing

                --save_db_name rel/my.db

            will output parsed news to the file

                PROJECT_ROOT/data/parsed/rel/my.db
            """
        ),
    )

    return parser.parse_args(argv)


def parse_raw_news(
    db_path: str,
    raw_news_list: List[RawNews],
) -> List[ParsedNews]:
    r"""根據公司用不同方法 parse `RawNews`."""
    parsed_news_list: List[ParsedNews] = []
    for raw_news in raw_news_list:
        try:
            parsed_news_list.append(
                PARSER_FASTEST_LOOKUP_TABLE[raw_news.company_id](
                    raw_news=raw_news
                )
            )
        except Exception as err:
            print(f'Failed to parse idx {raw_news.idx} in {db_path}: {err}')

    return parsed_news_list


def main(argv: List[str]) -> None:
    args = parse_args(argv=argv)

    if args.db_name is None:
        args.db_name = []
    if args.db_dir is None:
        args.db_dir = []

    # Map relative paths to absolute paths under `PROJECT_ROOT/data/raw`.
    db_paths = news.db.get_db_paths(
        file_paths=list(
            map(
                news.crawlers.db.util.get_db_path,
                args.db_name + args.db_dir,
            )
        ),
    )

    save_db_path = news.parse.db.util.get_db_path(db_name=args.save_db_name)
    save_conn = news.db.get_conn(db_path=save_db_path)
    save_cur = save_conn.cursor()
    news.parse.db.create.create_table(cur=save_cur)

    for db_path in db_paths:
        try:
            # Must use absolute path `db_path` since some absolute paths is not
            # in default locations (which is `PROJECT_ROOT/data/raw`).  This is
            # fine since `get_num_of_records` use `get_db_path` internally.
            # Note that this statement usually take a long times.
            num_of_records = news.crawlers.db.read.get_num_of_records(
                db_name=db_path,
            )
        except Exception as err:
            print(f'Failed to get number of records in {db_path}: {err}')

        # Parsing `RawNews` by batch.
        for offset in trange(
                0,
                num_of_records,
                args.batch_size,
                desc=f'Parsing {db_path}',
                disable=not args.debug,
                dynamic_ncols=True,
        ):
            try:
                raw_news_list = news.crawlers.db.read.read_some_records(
                    db_name=db_path,
                    offset=offset,
                    limit=args.batch_size,
                )

                news.parse.db.write.write_new_records(
                    cur=save_cur,
                    news_list=parse_raw_news(
                        db_path=db_path,
                        raw_news_list=raw_news_list,
                    ),
                )

                save_conn.commit()

                # Avoid using too many memories.
                gc.collect()
            except Exception:
                print(f'Failed to write records at id {offset} of {db_path}.')

    save_conn.close()


if __name__ == '__main__':
    main(argv=sys.argv[1:])
