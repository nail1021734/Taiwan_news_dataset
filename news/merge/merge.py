import os

from tqdm import tqdm

import news.merge.db


def merge_db(dir_path: str, save_db: str, reserve_id: bool):
    # 取得輸入資料夾`dir_path`中所有資料庫名稱
    db_names = os.listdir(os.path.join('data', dir_path))

    # 建立寫入目標資料庫的connection
    tgt_conn = news.merge.db.util.get_conn(save_db)

    create_table = False
    for db_name in tqdm(db_names):
        db_path = os.path.join(dir_path, db_name)
        src_data = news.merge.db.read.AllRecords(db_path)

        # Check if database already created table.
        if not create_table:
            # Get column names.
            column_names = list(src_data[0].keys())
            # Create table.
            news.merge.db.create.create_table(
                cur=tgt_conn.cursor(),
                columns=column_names
            )
            create_table = True

        if not reserve_id:
            # remove id from src data.
            for i in src_data:
                del i['id']

        # Write data into db.
        news.merge.db.write.write_new_records(
            cur=tgt_conn.cursor(),
            news_list=src_data
        )

        # Commit.
        tgt_conn.commit()

    tgt_conn.close()
