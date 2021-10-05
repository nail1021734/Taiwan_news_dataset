import sqlite3
from typing import Dict, List


def write_new_records(cur: sqlite3.Cursor, news_list: List[Dict]):
    r"""輸入目標資料庫的 `cursor` 與 `news_list`, 將 `news_list` 內的資料保存到目標資料庫中"""

    # 取出已存在目標資料庫的url，避免重複保存相同的資料
    existed_url = list(cur.execute("""
        SELECT url_pattern FROM news
    """))
    existed_url = set(map(lambda url: url[0], existed_url))

    # 過濾掉`news_list`內重複的資料
    tmp = []
    for n in news_list:
        if n['url_pattern'] not in existed_url:
            tmp.append(n)
            existed_url.add(n['url_pattern'])

    # 根據輸入資料欄位自動調整寫入資料庫的指令
    columns = list(news_list[0].keys())
    column_num = len(columns)
    columns_str = ', '.join(columns)
    column_num_str = '?, ' * (column_num - 1) + '?'

    news_list = [tuple(news.values()) for news in tmp]

    cur.executemany(
        f"""
        INSERT INTO news({columns_str})
        VALUES ({column_num_str})
        """,
        news_list
    )
