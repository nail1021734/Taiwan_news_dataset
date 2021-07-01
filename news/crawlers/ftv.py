from collections import Counter
from datetime import datetime, timedelta
from typing import List

import dateutil.parser
import requests
from tqdm import tqdm

import news.crawlers
import news.db
from news.db.schema import News

# <li> <a href='https://www.ftvnews.com.tw/realtime/'>即時</a> </li>
# <li> <a href='https://www.ftvnews.com.tw/popular/'>熱門</a> </li>
# <li> <a href='/tag/快新聞'>快新聞</a> </li>
# <li> <a href='/tag/政治'>政治</a> </li>
# <li> <a href='/tag/娛樂'>娛樂</a> </li>
# <li> <a href='/tag/財經'>財經</a> </li>
# <li> <a href='/tag/生活'>生活</a> </li>
# <li> <a href='/tag/國際'>國際</a> </li>
# <li> <a href='/tag/社會'>社會</a> </li>
# <li> <a href='/tag/體育'>體育</a> </li>
# <li> <a href='/tag/健康'>健康</a> </li>
# <li> <a href='/tag/美食'>美食</a> </li>
# <li> <a href='/tag/氣象'>氣象</a> </li>
# <li> <a href='/tag/武漢肺炎'>疫情擴散</a> </li>
# <li> <a href='/tag/熱門網搜'>熱門網搜</a> </li>
# <li> <a href='/tag/下雨'>世紀乾旱</a> </li>
# <li> <a href='https://englishnews.ftv.com.tw/'>英語新聞</a> </li>
# <li> <a href='/tag/疫苗'>疫苗</a> </li>
# <li> <a href='/tag/運勢'>運勢</a> </li>
# <li> <a href='/tag/PLEAGUE'>P.LEAGUE+</a> </li>
# <li> <a href='/tag/台灣演義'>台灣演義</a> </li>
# <li> <a href='/tag/新聞觀測站'>新聞觀測站</a> </li>
# <li> <a href='/tag/民視異言堂'>異言堂</a> </li>
# <li> <a href='/tag/工商好消息'>工商好消息</a> </li>

CONTINUE_FAIL_COUNT = 1000

CATEGORIES = {
    'A': '體育',
    'C': '一般',
    'F': '財經',
    'I': '國際',
    'J': '美食',
    # 'L': '生活',
    # 'N': '社會',
    # 'P': '政治',
    # 'R': '美食',
    # 'S': '社會',
    # 'U': '社會',
    # 'W': '一般',
}


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

    fail_count = 0
    date_str = \
        f'{date.strftime("%Y")}{int(date.strftime("%m")):x}{date.strftime("%d")}'

    # Only show progress bar in debug mode.
    if api == 'W':
        iter_range = range(10000)
    else:
        iter_range = range(30)

    if debug:
        iter_range = tqdm(iter_range)

    for i in iter_range:
        # No more news to crawl.
        if fail_count >= CONTINUE_FAIL_COUNT:
            break

        if api == 'W':
            url = f'https://www.ftvnews.com.tw/news/detail/{date_str}{api}{i:04}'
        else:
            url = f'https://www.ftvnews.com.tw/news/detail/{date_str}{api}{i:02}M1'

        try:
            response = requests.get(
                url,
                timeout=news.crawlers.util.REQUEST_TIMEOUT,
            )
            response.close()

            # Raise exception if status code is not 200.
            news.crawlers.util.check_status_code(
                company='ftv',
                response=response
            )

            # If `status_code == 200`, reset `fail_count`.
            fail_count = 0

            parsed_news = news.preprocess.ftv.parse(ori_news=News(
                raw_xml=response.text,
                url=url,
            ))

            news_datetime = dateutil.parser.isoparse(parsed_news.datetime)
            if news_datetime > current_datetime:
                continue
            if past_datetime > news_datetime:
                raise Exception('Time constraint violated.')

            news_list.append(parsed_news)
        except Exception as err:
            fail_count += 1

            if err.args:
                logger.update([err.args[0]])
            continue

    # Only show error stats in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


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

    for api, category in CATEGORIES.items():
        date = current_datetime
        # Commit database once a day.
        while date > past_datetime:
            news.db.write.write_new_records(
                cur=cur,
                news_list=get_news_list(
                    category=category,
                    current_datetime=date,
                    api=api,
                    debug=debug,
                    past_datetime=date - timedelta(days=1),
                ),
            )

            # Go back 1 day.
            date = date - timedelta(days=1)

            conn.commit()

    # Close database connection.
    conn.close()
