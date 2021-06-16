import sqlite3
from typing import Sequence

from news.db.schema import News


def write_new_records(cur: sqlite3.Cursor, news_list: Sequence[News]):
    existed_url = list(cur.execute('''
        SELECT url FROM news
    '''))
    existed_url = set(map(lambda url: url[0], existed_url))

    # Filter out existed news.
    tmp = []
    for n in news_list:
        if n.url not in existed_url:
            tmp.append(n)
            existed_url.add(n.url)

    news_list = [tuple(news) for news in tmp]

    cur.executemany(
        '''
        INSERT INTO news(article, category, company, datetime, raw_xml, reporter, title, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        news_list
    )
