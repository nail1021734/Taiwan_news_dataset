import argparse
import gc
import os
import pathlib
import sys
import textwrap
from typing import List, Tuple

from tqdm import trange

import news.crawlers.db.create
import news.crawlers.db.read
import news.crawlers.db.util
import news.crawlers.db.write
import news.db
import news.parse.db.create
import news.parse.db.read
import news.parse.db.util
import news.parse.db.write
import news.path


def parse_args(argv: List[str]) -> argparse.Namespace:
    r"""Parse command line arguments.

    Example
    =======
    python -m news.split.main    \
        --db_name rel/my.db      \
        --db_name /abs/my.db     \
        --db_dir rel_dir         \
        --db_dir /abs_dir        \
        --db_type raw            \
        --debug                  \
        --records_per_split 1000
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        '--db_name',
        action='append',
        type=str,
        help=textwrap.dedent(
            f"""\
            SQLite database file name wanted to split.  If absolute path is
            given, then treat the given path as database file and read records
            directly from the given path.

            For example, excuting

                --db_type parsed --db_name /abs/my.db

            will split the file

                /abs/my.db

            into

                PROJECT_ROOT/data/parsed/split/abs/my__1_1000.db
                PROJECT_ROOT/data/parsed/split/abs/my__1001_2000.db
                PROJECT_ROOT/data/parsed/split/abs/my__2001_3000.db
                ...

            If relative path is given, then we assume the given path is under
            the path `PROJECT_ROOT/data/db_type`, where `db_type` is
            determined by `--db_type` argument.`.  Currently project root is
            set to {news.path.PROJECT_ROOT}.

            For example, executing

                --db_type raw --db_name rel/my.db

            will split the file

                PROJECT_ROOT/data/raw/rel/my.db

            into

                PROJECT_ROOT/data/raw/split/rel/my__1_1000.db
                PROJECT_ROOT/data/raw/split/rel/my__1001_2000.db
                PROJECT_ROOT/data/raw/split/rel/my__2001_3000.db
                ...

            One can specify multiple database files at the same time using
            multiple `--db_name`.

            For example, executing

                --db_type raw --db_name rel/a.db --db_name /abs/b.db

            will split all the following files

                PROJECT_ROOT/data/raw/rel/a.db
                /abs/b.db

            into

                PROJECT_ROOT/data/raw/split/rel/a__1_1000.db
                PROJECT_ROOT/data/raw/split/rel/a__1001_2000.db
                PROJECT_ROOT/data/raw/split/rel/a__2001_3000.db
                ...
                PROJECT_ROOT/data/raw/split/abs/b__1_1000.db
                PROJECT_ROOT/data/raw/split/abs/b__1001_2000.db
                PROJECT_ROOT/data/raw/split/abs/b__2001_3000.db
                ...
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

                --db_type raw --db_dir /abs/dir

            will split all the following files

                /abs/dir/a.db
                /abs/dir/subdir/b.db

            into

                PROJECT_ROOT/data/raw/split/abs/dir/a__1_1000.db
                PROJECT_ROOT/data/raw/split/abs/dir/a__1001_2000.db
                PROJECT_ROOT/data/raw/split/abs/dir/a__2001_3000.db
                ...
                PROJECT_ROOT/data/raw/split/abs/dir/subsir/b__1_1000.db
                PROJECT_ROOT/data/raw/split/abs/dir/subsir/b__1001_2000.db
                PROJECT_ROOT/data/raw/split/abs/dir/subsir/b__2001_3000.db
                ...

            If relative path is given, then we assume the given directory is
            under the path `PROJECT_ROOT/data/db_type`, where `db_type` is
            determined by `--db_type` argument.  Currently project root is set
            to {news.path.PROJECT_ROOT}.

            For example, if `PROJECT_ROOT/data/parsed/rel/dir` contains

                c.db
                subdir/d.db

            then executing

                --db_type parsed --db_dir rel/dir

            will split all the following files

                PROJECT_ROOT/data/parsed/rel/dir/c.db
                PROJECT_ROOT/data/parsed/rel/dir/subdir/d.db

            into

                PROJECT_ROOT/data/parsed/split/rel/dir/c__1_1000.db
                PROJECT_ROOT/data/parsed/split/rel/dir/c__1001_2000.db
                PROJECT_ROOT/data/parsed/split/rel/dir/c__2001_3000.db
                ...
                PROJECT_ROOT/data/parsed/split/rel/dir/subsir/d__1_1000.db
                PROJECT_ROOT/data/parsed/split/rel/dir/subsir/d__1001_2000.db
                PROJECT_ROOT/data/parsed/split/rel/dir/subsir/d__2001_3000.db
                ...

            One can specify multiple directory at the same time using multiple
            `--db_dir`.

            Continue from previouse example, excuting

                --db_type parsed --db_dir rel/dir --db_dir /abs/dir

            will split all the following files

                /abs/dir/a.db
                /abs/dir/subdir/b.db
                PROJECT_ROOT/data/parsed/rel/dir/c.db
                PROJECT_ROOT/data/parsed/rel/dir/subdir/d.db

            into

                PROJECT_ROOT/data/parsed/split/abs/dir/a__1_1000.db
                PROJECT_ROOT/data/parsed/split/abs/dir/a__1001_2000.db
                PROJECT_ROOT/data/parsed/split/abs/dir/a__2001_3000.db
                ...
                PROJECT_ROOT/data/parsed/split/abs/dir/subsir/b__1_1000.db
                PROJECT_ROOT/data/parsed/split/abs/dir/subsir/b__1001_2000.db
                PROJECT_ROOT/data/parsed/split/abs/dir/subsir/b__2001_3000.db
                ...
                PROJECT_ROOT/data/parsed/split/rel/dir/c__1_1000.db
                PROJECT_ROOT/data/parsed/split/rel/dir/c__1001_2000.db
                PROJECT_ROOT/data/parsed/split/rel/dir/c__2001_3000.db
                ...
                PROJECT_ROOT/data/parsed/split/rel/dir/subsir/d__1_1000.db
                PROJECT_ROOT/data/parsed/split/rel/dir/subsir/d__1001_2000.db
                PROJECT_ROOT/data/parsed/split/rel/dir/subsir/d__2001_3000.db
                ...
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
            Type of records to split.  Currently only support two options:

            - `raw`: Split `news.crawlers.db.schema.RawNews` in the database
              file.  All relative paths specified by `--db_name` and `--db_dir`
              are assumed to be under the path `PROJECT_ROOT/data/raw`. All
              database files specified by `--db_name` and `--db_dir` will be
              queried with:

              - `news.crawlers.db.read.read_some_records`
              - `news.crawlers.db.read.get_num_of_records`

            - `parsed`: Split `news.parse.db.schema.ParsedNews` in the database
              file.  All relative paths specified by `--db_name` and `--db_dir`
              are assumed to be under the path `PROJECT_ROOT/data/parse`.
              All database files specified by `--db_name` and `--db_dir`
              will be queried with:

              - `news.parse.db.read.read_some_records`
              - `news.parse.db.read.get_num_of_records`
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
        '--records_per_split',
        type=int,
        default=1000,
        help=textwrap.dedent(
            """\
            Number of records to put into each split.  Each output database
            file will contain records no more than `--records_per_split`.
            Output database files will have the same file names and extensions
            but with records offset append at the end of file names.

            For example, suppose that `my.db` has 2500 records. If we split
            `my.db` with `--records_per_split 1000`, then we will output
            following files

                my__1_1000.db
                my__1001_2000.db
                my__2001_2500.db
            """
        ),
    )

    return parser.parse_args(argv)


def get_output_db_path(
    db_name: str,
    db_type: str,
    start_idx: int,
    end_idx: int,
) -> str:
    db_name_no_ext, db_name_ext = os.path.splitext(db_name)
    # Split files are output to path `PROJECT_ROOT/data/split/{db_type}` with
    # file name `{filename}__{start_idx}_{end_idx}.{fileext}`.
    return os.path.join(
        news.path.DATA_PATH,
        db_type,
        'split',
        f'{db_name_no_ext}__{start_idx}_{end_idx}{db_name_ext}',
    )


def main(argv: List[str]) -> None:
    args = parse_args(argv=argv)

    if args.db_name is None:
        args.db_name = []
    if args.db_dir is None:
        args.db_dir = []

    if args.db_type == 'raw':
        create_table = news.crawlers.db.create.create_table
        get_num_of_records = news.crawlers.db.read.get_num_of_records
        get_db_path = news.crawlers.db.util.get_db_path
        read_some_records = news.crawlers.db.read.read_some_records
        write_new_records = news.crawlers.db.write.write_new_records
    elif args.db_type == 'parsed':
        create_table = news.parse.db.create.create_table
        get_num_of_records = news.parse.db.read.get_num_of_records
        get_db_path = news.parse.db.util.get_db_path
        read_some_records = news.parse.db.read.read_some_records
        write_new_records = news.parse.db.write.write_new_records
    else:
        raise ValueError('Invalid `db_type`.')

    # Map relative paths to absolute paths according to `--db_type`.
    # `db_paths` will only include paths of database files.  See `--db_dir`
    # argument helper text for behavior details.
    db_path_prefix = get_db_path(db_name='')
    db_paths_and_names: Tuple[str, str] = []
    for db_path in news.db.get_db_paths(file_paths=list(map(
            get_db_path,
            args.db_name + args.db_dir,
    )),):
        # Remove prefix to get output file name.  See `--db_name` and
        # `--db_dir` arguments helper text for behavior details.
        db_name = db_path.replace(db_path_prefix, '')

        # `db_path` is originally an absolute path, and is not under the path
        # `db_path_prefix`.  In this case we remove the root symbol (which is
        # os dependent) and use all the path from the root as part of database
        # file name.
        if os.path.isabs(db_name):
            root = pathlib.PurePath(db_name).anchor
            db_name = db_name[len(root):]

        db_paths_and_names.append((db_path, db_name))

    # Start spliting.
    for db_path, db_name in db_paths_and_names:
        # Must use absolute path `db_path` instead of `db_name` since some
        # absolute paths is not in default locations (which is
        # `PROJECT_ROOT/data`).  This is fine since `get_num_of_records` use
        # `get_db_path` internally.
        num_of_records = get_num_of_records(db_name=db_path)
        for offset in trange(
                0,
                num_of_records,
                args.records_per_split,
                desc=f'Splitting {db_name}',
                disable=not args.debug,
                dynamic_ncols=True,
        ):
            try:
                news_list = read_some_records(
                    db_name=db_path,
                    limit=args.records_per_split,
                    offset=offset,
                )

                # Use `offset + 1` since SQLite id start with 1 but offset
                # start with 0.
                output_db_path = get_output_db_path(
                    db_name=db_name,
                    db_type=args.db_type,
                    start_idx=offset + 1,
                    end_idx=min(
                        offset + args.records_per_split,
                        num_of_records,
                    ),
                )

                conn = news.db.get_conn(db_path=output_db_path)
                cur = conn.cursor()
                create_table(cur=cur)

                write_new_records(cur=cur, news_list=news_list)
                conn.commit()

                # Avoid using too many memories.
                del news_list
                gc.collect()
            except Exception:
                print(f'Failed to split {db_name} into {output_db_path}')
            finally:
                conn.close()


if __name__ == '__main__':
    main(argv=sys.argv[1:])
