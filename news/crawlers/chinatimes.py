from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from tqdm import trange

import news.crawlers.db.create
import news.crawlers.db.util
import news.crawlers.db.write
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.crawlers.util.status_code
import news.db
from news.crawlers.db.schema import RawNews

# `category_id` is sorted based on request hit rates.
###############################################################################
#                                  WARNING
# DO NOT change the order unless you know what you are doing.
###############################################################################
CATEGORY_ID_LOOKUP_TABLE: Dict[str, str] = {
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
COMPANY_ID: int = news.crawlers.util.normalize.get_company_id(company='中時',)
COMPANY_URL: str = news.crawlers.util.normalize.get_company_url(
    company_id=COMPANY_ID,
)


def get_news_list(
    current_datetime: datetime,
    *,
    continue_fail_count: Optional[int] = 1000,
    debug: Optional[bool] = False,
    max_news_per_day: Optional[int] = 100000,
    **kwargs: Optional[Dict],
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()
    fail_count = 0
    datetime_str = current_datetime.strftime('%Y%m%d')

    # Only show progress bar in debug mode.
    for news_idx in trange(
            max_news_per_day,
            desc='Crawling',
            disable=not debug,
            dynamic_ncols=True,
    ):
        # Each `news_idx` only appear in exactly one category.  But we don't
        # know which one.  Thus we loop through all categories to find the
        # correct `category_idx` which the `news_idx` belongs to.  If no
        # `category_idx` match, then `news_idx` does not exist.
        for category_idx in CATEGORY_ID_LOOKUP_TABLE.values():
            # 觀察到 chinatimes 有兩種 URL 路徑都有新聞,由於 'newspapers' 的
            # hit rate 比較高因此排在前面先搜尋
            for domain_path in ['newspapers', 'realtimenews']:
                url = f'{COMPANY_URL}{domain_path}/{datetime_str}' + \
                    f'{news_idx:06d}-{category_idx}'
                response = None
                try:
                    response = news.crawlers.util.request_url.get(url=url)

                    # Raise exception if status code is not 200.
                    news.crawlers.util.status_code.check_status_code(
                        company_id=COMPANY_ID,
                        status_code=response.status_code,
                        url=url,
                    )
                    news_list.append(
                        RawNews(
                            company_id=COMPANY_ID,
                            raw_xml=news.crawlers.util.normalize
                            .compress_raw_xml(raw_xml=response.text,),
                            url_pattern=news.crawlers.util.normalize
                            .compress_url(
                                company_id=COMPANY_ID,
                                url=url,
                            ),
                        )
                    )

                    # Reset `fail_count` if no error occurred.
                    fail_count = 0
                    break
                except Exception as err:
                    if err.args \
                            and response is not None \
                            and response.status_code != 404:
                        fail_count += 1
                        logger.update([err.args[0]])
                        break
            # If hit then break category loop.
            if response is not None and response.status_code == 200:
                break

        # Request timeout.
        if response is None:
            fail_count += 1
            logger.update(['Request timeout.'])
        # `news_idx` does not exist.
        elif response.status_code == 404:
            fail_count += 1
            logger.update(['URL not found.'])

        # No more news to crawl.
        if fail_count >= continue_fail_count:
            break

    # Only show error statistics in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


def main(
    current_datetime: datetime,
    db_name: str,
    past_datetime: datetime,
    **kwargs: Optional[Dict],
) -> None:
    # Value check.
    if current_datetime.tzinfo != timezone.utc:
        raise ValueError('`current_datetime` must in utc timezone.')
    if past_datetime.tzinfo != timezone.utc:
        raise ValueError('`past_datetime` must in utc timezone.')
    if past_datetime > current_datetime:
        raise ValueError('Must have `past_datetime <= current_datetime`.')

    # Get database connection.
    db_path = news.crawlers.db.util.get_db_path(db_name=db_name)
    conn = news.db.get_conn(db_path=db_path)
    cur = conn.cursor()

    # Ensure news table exists.
    news.crawlers.db.create.create_table(cur=cur)

    # Commit transaction for each day.
    loop_datetime = current_datetime
    while loop_datetime >= past_datetime:
        # Get news list.
        news_list = get_news_list(current_datetime=loop_datetime, **kwargs)

        # Write news records to database.
        news.crawlers.db.write.write_new_records(cur=cur, news_list=news_list)
        conn.commit()

        # Go back 1 day.
        loop_datetime = loop_datetime - timedelta(days=1)

    # Close database connection.
    conn.close()
