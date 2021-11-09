import gc
import argparse
from typing import Tuple, List
from operator import itemgetter
import news.db
import news.parse.db.util
import news.parse.db.read
import news.parse.db.create
import news.parse.db.write
import numpy as np
import sqlite3


def get_timestamp(db_path):
    conn: sqlite3.Connection = news.db.get_conn(db_path=db_path)
    cur: sqlite3.Cursor = conn.cursor()
    return cur.execute("SELECT id, timestamp FROM parsed_news;").fetchall()


def get_by_id(db_path, ids):
    conn: sqlite3.Connection = news.db.get_conn(db_path=db_path)
    cur: sqlite3.Cursor = conn.cursor()
    q = f'= {ids[0]}' if len(ids) == 1 else f'IN {tuple(ids)}'
    return cur.execute(f"""
        SELECT id, article, category, company_id, reporter, timestamp, title, url_pattern
        FROM   parsed_news
        WHERE id {q};
        """).fetchall()


def sort_index(db_paths):
    ts = []
    for idx, db_path in enumerate(db_paths):
        t = np.array(get_timestamp(db_path))
        ts.append(np.c_[t, np.ones(t.shape[0], dtype=int) * idx])
    ts = np.vstack(ts)
    ts = np.take(ts, np.argsort(ts[:, 1], kind='mergesort'), axis=0)
    return ts[:, [0, 2]]


def merge_parsed_news_db(args: argparse.Namespace) -> None:
    # Map relative paths to absolute paths. `db_paths` will only include paths
    # of database files.
    db_paths = news.db.get_db_paths(file_paths=list(
        map(
            news.parse.db.util.get_db_path,
            args.db_name + args.db_dir,
        )))

    # No sqlite database files found.  In this case no need to merge anything.
    if not db_paths:
        return

    # Get connection and create table if table does not exists.
    conn = news.db.get_conn(
        db_path=news.parse.db.util.get_db_path(args.save_db_name))
    cur = conn.cursor()
    news.parse.db.create.create_table(cur=cur)
    conn.commit()

    indices = sort_index(db_paths)
    for s in range(0, indices.shape[0], args.batch_size):
        batch_ids = indices[s:s + args.batch_size]
        batch = []
        for db_idx, db_path in enumerate(db_paths):
            q = batch_ids[:, 1] == db_idx
            if not any(q):
                continue
            batch.extend(get_by_id(db_path, batch_ids[q][:, 0]))
        batch = sorted(batch, key=itemgetter(5))

        news.parse.db.write.write_new_records(
            cur=cur,
            news_list=[
                news.parse.db.schema.ParsedNews(
                    idx=idx,
                    article=article,
                    category=category,
                    company_id=company_id,
                    reporter=reporter,
                    timestamp=timestamp,
                    title=title,
                    url_pattern=url_pattern,
                ) for (
                    idx,
                    article,
                    category,
                    company_id,
                    reporter,
                    timestamp,
                    title,
                    url_pattern,
                ) in batch
            ])
        conn.commit()

    conn.close()
