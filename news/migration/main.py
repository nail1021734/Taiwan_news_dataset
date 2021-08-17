import argparse
import os

import news.migration.db
from news.migration.db_migration import v1

MIGRATE_VERSION = {
    'v1': v1,
}


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--src',
        type=str,
        help='Select db to perform migration.(PATH root: `data`)',
    )
    parser.add_argument(
        '--migrate_version',
        choices=MIGRATE_VERSION.keys(),
        type=str,
        help='Select migrate version.',
    )
    parser.add_argument(
        '--save_path',
        type=str,
        help='Specify path to save result.(PATH root: `data/raw`)',
    )
    args = parser.parse_args()
    return args


def migrate(
    origin_data,
    args
):
    raw_news = MIGRATE_VERSION[args.migrate_version](
        dataset=origin_data
    )

    # Get connection to `save_path`.
    conn = news.crawlers.db.util.get_conn(
        db_name=args.save_path
    )
    # Create table in `save_path`.
    news.crawlers.db.create.create_table(
        cur=conn.cursor()
    )
    # Write data into db.
    news.crawlers.db.write.write_new_records(
        cur=conn.cursor(),
        news_list=raw_news
    )

    # Commit and close connection.
    conn.commit()
    conn.close()


def main():
    args = parse_argument()

    # Check if `args.src` is file.
    if args.src.split('.')[-1] == 'db':
        origin_data = news.migration.db.read.AllRecords(
            db_name=args.src
        )
        migrate(
            origin_data=origin_data,
            args=args
        )
    else:
        dir_path = os.path.join('data', args.src)
        for filename in os.listdir(dir_path):
            origin_data = news.migration.db.read.AllRecords(
                db_name=os.path.join(args.src, filename)
            )
            clear_filename = filename.split('.')[0]
            tmp_args = argparse.Namespace(**vars(args))
            tmp_args.save_path = os.path.join(
                args.save_path,
                f'{clear_filename}.db'
            )
            migrate(
                origin_data=origin_data,
                args=tmp_args
            )


if __name__ == '__main__':
    main()
