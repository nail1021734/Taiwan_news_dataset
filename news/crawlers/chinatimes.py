from collections import Counter
from datetime import datetime, timedelta
from typing import List

import requests
from tqdm import tqdm

import news
from news.crawlers.db.schema import RawNews
from news.crawlers.util.normalize import (company_id, compress_raw_xml,
                                          compress_url)

CONTINUE_FAIL_COUNT = 1000
COMPANY = '中時'


def get_news_list(
    current_datetime: datetime,
    past_datetime: datetime,
    *,
    debug: bool = False,
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()

    date = current_datetime

    fail_count = 0
    date_str = date.strftime('%Y%m%d')

    # Only show progress bar in debug mode.
    iter_range = range(100000)
    if debug:
        iter_range = tqdm(iter_range)

    for i in iter_range:
        # No more news to crawl.
        if fail_count >= CONTINUE_FAIL_COUNT:
            break

        check_get_news = False
        for category, api in CATEGORIES.items():
            url = f'https://www.chinatimes.com/realtimenews/{date_str}{i:06d}-{api}?chdtv'
            try:
                response = requests.get(
                    url,
                    timeout=news.crawlers.util.status_code.REQUEST_TIMEOUT,
                )
                response.close()

                # Raise exception if status code is not 200.
                news.crawlers.util.status_code.check_status_code(
                    company='chinatimes',
                    response=response
                )

                news_list.append(RawNews(
                    company_id=company_id(company=COMPANY),
                    raw_xml=compress_raw_xml(raw_xml=response.text),
                    url_pattern=compress_url(url=url, company=COMPANY),
                ))

                # If already get news in this id then break to next id.
                check_get_news = True
                break
            except Exception as err:
                if err.args:
                    logger.update([err.args[0]])
        if not check_get_news:
            fail_count += 1
            logger.update(['Index not found.'])
        else:
            # If `status_code == 200`, reset `fail_count`.
            fail_count = 0

    # Only show error stats in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


CATEGORIES = {
    '政治': '260407',
    '時尚、玩食': '260405',
    '財經': '260410',
    '社會': '260402',
    '哈燒日韓、西洋熱門': '260404',
    '兩岸': '260409',
    '球類': '260403',
    '國際': '260408',
    '寶島': '260421',
    '科技': '260412',
    '健康': '260418',
    '運勢': '260423',
    '軍事': '260417',
    '新消息': '262301',
    '中時社論': '262101',
    '旺報社評': '262102',
    '工商社論': '262113',
    '快評': '262103',
    '時論廣場': '262104',
    '尚青論壇': '262114',
    '兩岸徵文': '262106',
    '兩岸史話': '262107',
    '海納百川': '262110',
    '消費': '260113',
    '華人星光': '262404',
    '高爾夫': '260111',
    '萌寵': '260819',
    '搜奇': '260809',
    '歷史': '260812',
    '時人真話': '260102',
}


def main(
    current_datetime: datetime,
    db_name: str,
    past_datetime: datetime,
    *,
    debug: bool = False,
):

    if past_datetime > current_datetime:
        raise ValueError('Must have `past_datetime <= current_datetime`.')

    # Get database connection.
    db_path = news.crawlers.db.util.get_db_path(db_name=db_name)
    conn = news.db.get_conn(db_path=db_path)
    cur = conn.cursor()
    news.crawlers.db.create.create_table(cur=cur)

    date = current_datetime
    # Commit database once a day.
    while date >= past_datetime:
        news.crawlers.db.write.write_new_records(
            cur=cur,
            news_list=get_news_list(
                current_datetime=date,
                debug=debug,
                past_datetime=date - timedelta(days=1),
            ),
        )
        # Go back 1 day.
        date = date - timedelta(days=1)

        conn.commit()

    # Close database connection.
    conn.close()
