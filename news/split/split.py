from news.split.db.util import get_conn
import sqlite3
import news.split.db
import os
from tqdm import tqdm


def split_db(db_path: str, save_path: str, id_interval: int):
    # Get db name.
    src_db_name = db_path.split('/')[-1].split('.')[0]

    # Get source data.
    src_data = news.split.db.read.AllRecords(db_name=db_path)
    interval_iter = list(range(0, len(src_data), id_interval))

    # Get column names.
    column_names = list(src_data[0].keys())

    # Save `src_data` in split db.
    for index, interval_cnt in tqdm(enumerate(interval_iter)):

        # Get target db path.
        tgt_path = os.path.join(save_path, f'{src_db_name}_{index}.db')

        # Get target db conncetion.
        tgt_conn = news.split.db.util.get_conn(tgt_path)
        # Create table in target db.
        news.split.db.create.create_table(
            cur=tgt_conn.cursor(), columns=column_names)

        # Save data into db.
        max_interval = min(len(src_data), interval_cnt + id_interval)
        news.split.db.write.write_new_records(
            cur=tgt_conn.cursor(),
            news_list=src_data[interval_cnt: max_interval]
        )

        # Commit and close.
        tgt_conn.commit()
        tgt_conn.close()


def main(db_path: str, save_dir: str, id_interval: int):
    split_db(
        db_path=db_path,
        save_path=save_dir,
        id_interval=id_interval
    )
