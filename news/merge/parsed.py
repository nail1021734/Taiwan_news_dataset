import argparse
import sqlite3
from operator import itemgetter
from typing import List, Tuple

import numpy as np

import news.db
import news.parse.db.create
import news.parse.db.read
import news.parse.db.util
import news.parse.db.write


def get_timestamp_list(db_path: str) -> List[Tuple[int, int]]:
    conn: sqlite3.Connection = news.db.get_conn(db_path=db_path)
    cur: sqlite3.Cursor = conn.cursor()
    return cur.execute("SELECT id, timestamp FROM parsed_news;").fetchall()


def get_by_id(
    db_path: str,
    ids: List[int],
) -> List[Tuple[int, str, str, int, str, int, str, str]]:
    """
    Query db by list of id
    """
    conn: sqlite3.Connection = news.db.get_conn(db_path=db_path)
    cur: sqlite3.Cursor = conn.cursor()
    q = f'= {ids[0]}' if len(ids) == 1 else f'IN {tuple(ids)}'
    return cur.execute(
        f"""
        SELECT id, article, category, company_id, reporter, timestamp, title, url_pattern
        FROM   parsed_news
        WHERE id {q};
        """
    ).fetchall()


def sort_index(db_paths: List[str]) -> np.ndarray:
    """
    Read timestamp and id from each db and return list of sorted id and db index by timestamp
    convert

    db_paths[0] -> (id 0, timestamp 0), (id 1, timestamp 1), ...., (id N0, timestamp N0)
    db_paths[1] -> (id 0, timestamp 0), (id 1, timestamp 1), ...., (id N1, timestamp N1)
    ...

    to

    list of ("id from it's own db", "index of db_paths inidcate which db")
    with shape (sum(Ni), 2)
    sorted by timestamp
    """
    id_column = 0
    timestamp_column = 1
    db_column = 2

    ts = []
    for idx, db_path in enumerate(db_paths):
        timestamp_list = np.array(get_timestamp_list(db_path))  # Ni, 2
        ts.append(
            np.hstack(
                (
                    timestamp_list,
                    np.full((timestamp_list.shape[0], 1), idx, dtype=int),
                )
            )
        )  # Ni, 3
    ts = np.vstack(ts)  # number of db, Ni, 3 -> sum(Ni), 3
    ts = np.take(
        ts,
        np.argsort(ts[:, timestamp_column], kind='mergesort'),
        axis=0,
    )  # sum(Ni), 3

    return ts[:, [id_column, db_column]]


def merge_parsed_news_db(args: argparse.Namespace) -> None:
    # Map relative paths to absolute paths. `db_paths` will only include paths
    # of database files.
    db_paths = news.db.get_db_paths(
        file_paths=list(
            map(
                news.parse.db.util.get_db_path,
                args.db_name + args.db_dir,
            )
        )
    )

    # No sqlite database files found.  In this case no need to merge anything.
    if not db_paths:
        return

    # Get connection and create table if table does not exists.
    conn = news.db.get_conn(
        db_path=news.parse.db.util.get_db_path(args.save_db_name)
    )
    cur = conn.cursor()
    news.parse.db.create.create_table(cur=cur)
    conn.commit()

    indices = sort_index(db_paths)
    for s in range(0, indices.shape[0], args.batch_size):
        # [N, 2] -> N * (id, db index)
        batch_ids = indices[s:s + args.batch_size]
        batch = []
        for db_idx, db_path in enumerate(db_paths):
            q = batch_ids[:, 1] == db_idx
            if not any(q):
                continue
            batch.extend(get_by_id(db_path, batch_ids[q][:, 0]))
        batch = sorted(batch, key=itemgetter(5))  # sort by timestamp

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
            ]
        )
        conn.commit()

    conn.close()
