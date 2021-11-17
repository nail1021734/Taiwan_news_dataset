import argparse
import gc
from datetime import datetime, timezone
from typing import List, Tuple

from tqdm import trange

import news.db
import news.parse.db.create
import news.parse.db.read
import news.parse.db.util
import news.parse.db.write
from news.merge.bucket import ParsedNewsBucket


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

    for db_path in db_paths:
        num_of_records = news.parse.db.read.get_num_of_records(db_name=db_path)
        for offset in trange(
                0,
                num_of_records,
                args.batch_size,
                desc=f'Merging {db_path}',
                disable=not args.debug,
                dynamic_ncols=True,
        ):
            try:
                news.parse.db.write.write_new_records(
                    cur=cur,
                    news_list=news.parse.db.read.read_some_records(
                        db_name=db_path,
                        limit=args.batch_size,
                        offset=offset,
                    ),
                )
                conn.commit()

                # Avoid using too many memories.
                gc.collect()
            except Exception:
                print(f'Failed to merge {db_path} into {args.save_db_name}')

    conn.close()
