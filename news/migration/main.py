import argparse
import os

import news.crawlers.db
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
    origin_data: news.migration.db.schema.OldNews,
    migrate_version: str,
    save_path: str
):
    # 用指定版本的轉換函式，將舊資料
    raw_news = MIGRATE_VERSION[migrate_version](
        dataset=origin_data
    )

    # Get connection to `save_path`.
    conn = news.crawlers.db.util.get_conn(
        db_name=save_path
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

    # 檢查輸入的db檔還是資料夾
    if args.src.split('.')[-1] == 'db':
        # 若是db檔則只對單一db做處理，並將處理結果保存在raw資料夾下
        origin_data = news.migration.db.read.AllRecords(
            db_name=args.src
        )
        migrate(
            origin_data=origin_data,
            save_path=args.save_path,
            migrate_version=args.migrate_version
        )
    else:
        # 若是資料夾則對資料夾內每個db檔做處理，並將處理結果保存在raw資料夾下

        # 取得完整來源資料夾路徑
        dir_path = os.path.join('data', args.src)
        for filename in os.listdir(dir_path):
            # 讀取舊資料
            origin_data = news.migration.db.read.AllRecords(
                db_name=os.path.join(args.src, filename)
            )

            # 將舊資料轉為指定版本的格式並保存到目標資料庫
            migrate(
                origin_data=origin_data,
                save_path=os.path.join(args.save_path, filename),
                migrate_version=args.migrate_version
            )


if __name__ == '__main__':
    main()
