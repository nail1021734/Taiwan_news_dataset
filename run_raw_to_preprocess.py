import sqlite3
import news.db
import gc
if __name__ == "__main__":
    data = [news.db.read.AllRecords(db_name='ftv.db') for _ in range(20)]
    # urls = set([n.url for n in data])
    # del data
    # gc.collect()
    input()
