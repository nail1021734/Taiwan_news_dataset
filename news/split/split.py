import os

import news.split.db


def split_db(db_path: str, save_path: str, id_interval: int):
    # Get db name.
    src_db_name = db_path.split('/')[-1].split('.')[0]

    # Initial offset.
    offset = 0
    # Save `src_data` in split db.
    while True:
        # Get source data.
        src_data = news.split.db.read.AllRecords(
            db_name=db_path,
            offset=offset,
            interval=id_interval,
        )

        # Get column names.
        column_names = list(src_data[0].keys())

        # 計算保存檔案時檔案名稱的index
        index = offset // id_interval

        # Get target db path.
        tgt_path = os.path.join(
            save_path, f'{src_db_name}_{index}.db')

        # Get target db conncetion.
        tgt_conn = news.split.db.util.get_conn(tgt_path)
        # Create table in target db.
        news.split.db.create.create_table(
            cur=tgt_conn.cursor(), columns=column_names)

        # Save data into db.
        news.split.db.write.write_new_records(
            cur=tgt_conn.cursor(),
            news_list=src_data,
        )

        # Commit and close.
        tgt_conn.commit()
        tgt_conn.close()

        if len(src_data) < id_interval:
            break
        else:
            offset += id_interval


def main(db_path: str, save_dir: str, id_interval: int):
    split_db(
        db_path=db_path,
        save_path=save_dir,
        id_interval=id_interval
    )
