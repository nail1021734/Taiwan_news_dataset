import argparse
import sys
import textwrap
from typing import List

import news.crawlers.db.create
import news.crawlers.db.read
import news.crawlers.db.util
import news.crawlers.db.write
import news.db
import news.merge.parsed
import news.merge.raw
import news.parse.db.create
import news.parse.db.read
import news.parse.db.util
import news.parse.db.write
import news.path


def parse_args(argv: List[str]) -> argparse.Namespace:
    r"""Parse command line arguments.

    Example
    =======
    python -m news.merge.main \
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
            Batch size of reading records.  Normally database consume large
            memories. Thus we will read records by batch. Each batch has at
            most `--batch_size` number of records.
            """
        ),
    )
    parser.add_argument(
        '--db_name',
        action='append',
        type=str,
        help=textwrap.dedent(
            f"""\
            SQLite database file names wanted to merge.  If absolute path is
            given, then treat the given path as database file and read records
            directly from the given path.

            For example, excuting

                --db_type parsed --db_name /abs/a.db --db_name /abs/b.db
                --save_db_name out.db

            will merge the files

                /abs/a.db
                /abs/b.db

            into

                PROJECT_ROOT/data/parsed/out.db

            If relative path is given, then we assume the given path is under
            the path `PROJECT_ROOT/data/db_type`, where `db_type` is
            determined by `--db_type` argument.`.  Currently project root is
            set to {news.path.PROJECT_ROOT}.

            For example, executing

                --db_type raw --db_name rel/a.db --db_name rel/b.db
                --save_db_name out.db

            will merge the file

                PROJECT_ROOT/data/raw/rel/a.db
                PROJECT_ROOT/data/raw/rel/b.db

            into

                PROJECT_ROOT/data/raw/out.db
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
            given, then recursively search the directory to find all SQLite
            database files.

            For example, if `/abs/dir` contains

                a.db
                subdir/b.db

            then executing

                --db_type raw --db_dir /abs/dir --save_db_name out.db

            will merge all the following files

                /abs/dir/a.db
                /abs/dir/subdir/b.db

            into

                PROJECT_ROOT/data/raw/out.db

            If relative path is given, then we assume the given directory is
            under the path `PROJECT_ROOT/data/db_type`, where `db_type` is
            determined by `--db_type` argument.  Currently project root is set
            to {news.path.PROJECT_ROOT}.

            For example, if `PROJECT_ROOT/data/parsed/rel/dir` contains

                c.db
                subdir/d.db

            then executing

                --db_type parsed --db_dir rel/dir --save_db_name out.db

            will merge all the following files

                PROJECT_ROOT/data/parsed/rel/dir/c.db
                PROJECT_ROOT/data/parsed/rel/dir/subdir/d.db

            into

                PROJECT_ROOT/data/parsed/out.db

            One can specify multiple directory at the same time using multiple
            `--db_dir`.

            Continue from previouse example, excuting

                --db_type parsed --db_dir rel/dir --db_dir /abs/dir

            will merge all the following files

                /abs/dir/a.db
                /abs/dir/subdir/b.db
                PROJECT_ROOT/data/parsed/rel/dir/c.db
                PROJECT_ROOT/data/parsed/rel/dir/subdir/d.db

            into

                PROJECT_ROOT/data/parsed/out.db
            """
        ),
    )
    parser.add_argument(
        '--db_type',
        type=str,
        choices=['raw', 'parsed'],
        required=True,
        help=textwrap.dedent(
            """\
            Type of records to merge.  Currently only support two options:

            - `raw`: Merge `news.crawlers.db.schema.RawNews` in the database
              file.  All relative paths specified by `--db_name` and `--db_dir`
              are assumed to be under the path `PROJECT_ROOT/data/raw`. All
              database files specified by `--db_name` and `--db_dir` will be
              queried with:

              - `news.crawlers.db.read.read_some_records`
              - `news.crawlers.db.read.get_num_of_records`

              Merging ordered are random.  No temporary files will be created.

            - `parsed`: Merge `news.parse.db.schema.ParsedNews` in the database
              file.  All relative paths specified by `--db_name` and `--db_dir`
              are assumed to be under the path `PROJECT_ROOT/data/parse`.
              All database files specified by `--db_name` and `--db_dir`
              will be queried with:

              - `news.parse.db.read.read_some_records`
              - `news.parse.db.read.get_num_of_records`
              - `news.parse.db.read.get_timestamp_bounds`

              Merging records are ordered by timestamp.  Since in memory
              sorting with huge number of records is impossible, we will create
              lots of temporary files and sort those much smaller files.
              Temporary files will be removed in the run. Both merged file and
              temporary files together will consume huge disk space, so make
              sure you have enough disk space.
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
            Name of the database to save merging results.  Create file if given
            path does not exist (along with non-existed directories in the
            path).  If absolute path is given, then treat the given path as
            SQLite database file.

            For example, executing

                --save_db_name /abs/my.db

            will output parsed news to the file

                /abs/my.db

            If relative path is given, then we assume the given path is under
            the path `PROJECT_ROOT/data/db_type/merge`, where `db_type` is
            determined by `--db_type` argument.  Currently project root is set
            to {news.path.PROJECT_ROOT}.

            For example, executing

                --save_db_name rel/my.db

            will output parsed news to the file

                PROJECT_ROOT/data/parsed/rel/my.db

            If the given path already exists and is a database file which
            contains records, then existing records will not be affected, and
            new records will be appended to the end.
            """
        ),
    )

    return parser.parse_args(argv)


def main(argv: List[str]) -> None:
    args = parse_args(argv=argv)

    if args.db_name is None:
        args.db_name = []
    if args.db_dir is None:
        args.db_dir = []

    if args.db_type == 'raw':
        news.merge.raw.merge_raw_news_db(args=args)
    elif args.db_type == 'parsed':
        news.merge.parsed.merge_parsed_news_db(args=args)
    else:
        raise ValueError('Invalid `db_type`.')


if __name__ == '__main__':
    main(argv=sys.argv[1:])
