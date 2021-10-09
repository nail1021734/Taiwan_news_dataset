from collections import Counter
from typing import Dict, Final, List, Optional

from tqdm import tqdm

import news.crawlers.db.create
import news.crawlers.db.util
import news.crawlers.db.write
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.crawlers.util.status_code
import news.db
from news.crawlers.db.schema import RawNews

RECORD_PER_COMMIT = 1000
COMPANY_ID = news.crawlers.util.normalize.get_company_id(company='三立')


def get_news_list(
    api: int,
    *,
    debug: Optional[bool] = False,
    **kwargs: Optional[Dict],
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()

    # Setn only 20 page per category.
    iter_range = range(1, 21)

    # Only show progress bar in debug mode.
    if debug:
        iter_range = tqdm(iter_range)

    for page in iter_range:
        url = f'https://www.setn.com/ViewAll.aspx?PageGroupID={api}&p={page}'

        try:
            news_url_patterns = news.crawlers.util.pre_parse.get_setn_link(url)
            for news_url_pattern in news_url_patterns:
                news_url = 'https://www.setn.com' + news_url_pattern

                response = news.crawlers.util.request_url(url=news_url)

                # Raise exception if status code is not 200.
                news.crawlers.util.status_code.check_status_code(
                    company_id=COMPANY_ID,
                    status_code=response.status_code,
                    url=news_url,
                )

                news_list.append(RawNews(
                    company_id=COMPANY_ID,
                    raw_xml=news.crawlers.util.normalize.compress_raw_xml(
                        raw_xml=response.text),
                    url_pattern=news.crawlers.util.normalize.compress_url(
                        url=news_url, company_id=COMPANY_ID),
                ))
        except Exception as err:
            if err.args:
                logger.update([err.args[0]])

    # Only show error stats in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


CATEGORY = {
    '政治': 6,
    '社會': 41,
    '國際': 5,
    '生活': 4,
    '健康': 65,
    '運動': 34,
    '汽車': 12,
    '地方': 97,
    '名家': 9,
    '新奇': 42,
    '科技': 7,
    '財經': 2,
    '寵物': 47,
}


def main(
    db_name: str,
    *,
    debug: Optional[bool] = False,
    **kwargs: Optional[Dict],
):
    # Get database connection.
    db_path = news.crawlers.db.util.get_db_path(db_name=db_name)
    conn = news.db.get_conn(db_path=db_path)
    cur = conn.cursor()

    # Ensure news table exists.
    news.crawlers.db.create.create_table(cur=cur)

    for category, api in CATEGORY.items():
        # Get news list.
        news_list = get_news_list(debug=debug, api=api)

        # No more news to crawl.
        if not news_list:
            break

        # Write news records to database.
        news.crawlers.db.write.write_new_records(cur=cur, news_list=news_list)
        conn.commit()

    # Close database connection.
    conn.close()
