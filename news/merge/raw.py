import argparse
import gc

from tqdm import trange

import news.crawlers.db.create
import news.crawlers.db.read
import news.crawlers.db.util
import news.crawlers.db.write
import news.db


def merge_raw_news_db(args: argparse.Namespace) -> None:
    db_paths = news.db.get_db_paths(
        file_paths=list(
            map(
                news.crawlers.db.util.get_db_path,
                args.db_name + args.db_dir,
            )
        )
    )

    # No sqlite database files found.  In this case no need to merge anything.
    if not db_paths:
        return

    # Get connection and create table if table does not exists.
    conn = news.db.get_conn(
        db_path=news.crawlers.db.util.get_db_path(args.save_db_name)
    )
    cur = conn.cursor()
    news.crawlers.db.create.create_table(cur=cur)
    conn.commit()

    # Map relative paths to absolute paths. `db_paths` will only include paths
    # of database files.
    for db_path in db_paths:
        num_of_records = news.crawlers.db.read.get_num_of_records(
            db_name=db_path,
        )
        for offset in trange(
                0,
                num_of_records,
                args.batch_size,
                desc=f'Merging {db_path}',
                disable=not args.debug,
                dynamic_ncols=True,
        ):
            try:
                news.crawlers.db.write.write_new_records(
                    cur=cur,
                    news_list=news.crawlers.db.read.read_some_records(
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
