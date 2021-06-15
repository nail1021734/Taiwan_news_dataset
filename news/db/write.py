import sqlite3
from typing import Sequence

from news.db.schema import News


def write_new_records(cur: sqlite3.Cursor, news_list: Sequence[News]):
    existed_url = list(cur.execute('''
        SELECT url from news
    '''))
    existed_url = set(map(lambda url: hash(url[0]), existed_url))

    news_list = [
        tuple(news)
        for news in news_list if hash(news.url) not in existed_url
    ]

    cur.executemany(
        '''
        INSERT INTO news(article, category, company, datetime, raw_xml, reporter, title, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        news_list
    )
