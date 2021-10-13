import os

from tqdm import tqdm

import news.merge.db


def merge_db(dir_path: str, save_db: str, reserve_id: bool):
    # 取得輸入資料夾`dir_path`中所有資料庫名稱
    db_names = os.listdir(os.path.join('data', dir_path))

    # 建立寫入目標資料庫的connection
    tgt_conn = news.merge.db.util.get_conn(save_db)

    # 預設此資料庫沒有建立過news table
    create_table = False
    for db_name in tqdm(db_names):
        # 初始化來源資料庫路徑
        db_path = os.path.join(dir_path, db_name)
        # 讀取來源資料庫資料
        src_data = news.merge.db.read.AllRecords(db_path)

        # 若沒有建立過news table則在目標資料庫中建立table
        if not create_table:
            # 取得來源資料庫的欄位名稱
            column_names = list(src_data[0].keys())
            # 建立news table
            news.merge.db.create.create_table(
                cur=tgt_conn.cursor(), columns=column_names
            )
            create_table = True

        if not reserve_id:
            # 如果使用者決定不保留原始資料ID，則將ID欄位移除
            for i in src_data:
                del i['id']

        # 將資料寫入目標資料庫
        news.merge.db.write.write_new_records(
            cur=tgt_conn.cursor(), news_list=src_data
        )

        # Commit.
        tgt_conn.commit()

    tgt_conn.close()
