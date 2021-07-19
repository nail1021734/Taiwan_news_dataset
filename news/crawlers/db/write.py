import sqlite3
from typing import Sequence

from news.crawlers.db.schema import News


def write_new_records(cur: sqlite3.Cursor, news_list: Sequence[News]):
    existed_url = list(cur.execute('''
        SELECT url_pattern FROM news
    '''))
    existed_url = set(map(lambda url: url[0], existed_url))

    # Filter out existed news.
    tmp = []
    for n in news_list:
        if n.url_pattern not in existed_url:
            tmp.append(n)
            existed_url.add(n.url_pattern)

    news_list = [tuple(news) for news in tmp]

    cur.executemany(
        '''
        INSERT INTO news(company_id, raw_xml, url_pattern)
        VALUES (?, ?, ?)
        ''',
        news_list
    )
