from collections import Counter
from datetime import datetime, timedelta
from typing import List

import dateutil.parser
import requests
from tqdm import tqdm

import news.crawlers
import news.db
from news.db.schema import News

CONTINUE_FAIL_COUNT = 5000


def get_news_list(
    category: str,
    current_datetime: datetime,
    api: str,
    past_datetime: datetime,
    *,
    debug: bool = False,
) -> List[News]:
    news_list: List[News] = []
    logger = Counter()

    date = current_datetime

    while date > past_datetime:
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

            url = f'https://www.chinatimes.com/realtimenews/{date_str}{i:06d}-{api}?chdtv'
            try:
                response = requests.get(
                    url,
                    timeout=news.crawlers.util.REQUEST_TIMEOUT,
                )
                response.close()

                # Raise exception if status code is not 200.
                news.crawlers.util.check_status_code(
                    company='chinatimes',
                    response=response
                )

                # If `status_code == 200`, reset `fail_count`.
                fail_count = 0

                parsed_news = news.preprocess.chinatimes.parse(ori_news=News(
                    raw_xml=response.text,
                    url=url,
                ))

                news_datetime = dateutil.parser.isoparse(parsed_news.datetime)
                if past_datetime > news_datetime or news_datetime > current_datetime:
                    raise Exception('Time constraint violated.')

                news_list.append(parsed_news)
            except Exception as err:
                fail_count += 1

                if err.args:
                    logger.update([err.args[0]])

        # Go back 1 day.
        date = date - timedelta(days=1)

    # Only show error stats in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


CATEGORIES = {
    '政治': '260407',
    '中時社論': '262101',
    '旺報社評': '262102',
    '工商社論': '262113',
    '快評': '262103',
    '時論廣場': '262104',
    '尚青論壇': '262114',
    '兩岸徵文': '262106',
    '兩岸史話': '262107',
    '海納百川': '262110',
    '玩食': '260405',
    '消費': '260113',
    '時尚': '260405',
    '新消息': '262301',
    '華人星光': '262404',
    '哈燒日韓、西洋熱門': '260404',
    '財經': '260410',
    '國際': '260408',
    '兩岸': '260409',
    '社會': '260402',
    '軍事': '260417',
    '科技': '260412',
    '高爾夫': '260111',
    '球類': '260403',
    '萌寵': '260819',
    '搜奇': '260809',
    '歷史': '260812',
    '健康': '260418',
    '時人真話': '260102',
    '運勢': '260423',
    '寶島': '260421'
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
    conn = news.db.util.get_conn(db_name=db_name)
    cur = conn.cursor()
    news.db.create.create_table(cur=cur)

    for category, api in CATEGORIES.items():
        news.db.write.write_new_records(
            cur=cur,
            news_list=get_news_list(
                api=api,
                category=category,
                current_datetime=current_datetime,
                debug=debug,
                past_datetime=past_datetime,
            ),
        )

        conn.commit()

    # Close database connection.
    conn.close()
