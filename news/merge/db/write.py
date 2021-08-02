import sqlite3
from typing import Dict, List


def write_new_records(cur: sqlite3.Cursor, news_list: List[Dict]):
    existed_url = list(cur.execute('''
        SELECT url_pattern FROM news
    '''))
    existed_url = set(map(lambda url: url[0], existed_url))

    # Filter out existed news.
    tmp = []
    for n in news_list:
        if n['url_pattern'] not in existed_url:
            tmp.append(n)
            existed_url.add(n['url_pattern'])

    # Dynamic handle column.
    columns = list(news_list[0].keys())
    column_num = len(columns)
    columns_str = ', '.join(columns)
    column_num_str = '?, ' * (column_num - 1) + '?'

    news_list = [tuple(news.values()) for news in tmp]

    cur.executemany(
        f'''
        INSERT INTO news({columns_str})
        VALUES ({column_num_str})
        ''',
        news_list
    )
