import re
from collections import Counter
from typing import Dict, Final, List, Optional

from tqdm import tqdm, trange

import news.crawlers.db.create
import news.crawlers.db.util
import news.crawlers.db.write
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.crawlers.util.status_code
import news.db
from news.crawlers.db.schema import RawNews

CATEGORY_API_LOOKUP_TABLE: Final[Dict[str, str]] = {
    'local': '1',
    'life': '2',
    'world': '3',
    'entertainment': '5',
    'china': '6',
    'politics': '7',
    'sports': '8',
    'tech': '12',
    'focus': '41',
    'fun': '50',
    'travel': '260',
    'health': '262',
    'cars': '269',
    'money': '270',
}
COMPANY_ID: Final[int] = news.crawlers.util.normalize.get_company_id(
    company='tvbs',
)
COMPANY_URL: Final[str] = news.crawlers.util.normalize.get_company_url(
    company_id=COMPANY_ID,
)


def get_latest_available_news_idx(
    category: Final[str],
    first_idx: Final[int],
    latest_idx: Final[int],
    *,
    continue_fail_count: Final[Optional[int]] = 500,
    debug: Final[Optional[bool]] = False,
    **kwargs: Final[Optional[Dict]],
) -> int:
    r"""TVBS's API will return latest news index if available.

    TVBS's API return news indices close to the query index (if available).
    Thus we use `latest_idx + 1` to make API consider `latest_idx`.  If no news
    indices are available, then we return `first_idx` to make the follow up
    crawling loops terminate earlier.
    """
    category_api = CATEGORY_API_LOOKUP_TABLE[category]
    logger = Counter()
    fail_count = 0

    # Only show progress bar in debug mode.
    for news_idx in trange(
            latest_idx + 1,
            first_idx,
            -1,
            desc='Find latest idx',
            disable=not debug,
            dynamic_ncols=True,
    ):
        category_api_url = (
            f'{COMPANY_URL}news/LoadMoreOverview'
            + f'?limit=100&offset=0&cateid={category_api}'
            + f'&cate={category}&newsid={news_idx}'
        )
        try:
            response = news.crawlers.util.request_url.get(url=category_api_url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=category_api_url,
            )

            # TVBS's API return json.  In the responed JSON, there is a field
            # called `newsid`, which is the lastest available news index.
            data_obj = response.json()

            # Successfully find the latest news index.
            if isinstance(data_obj, dict) and data_obj['news_id_list']:
                # `news_id_list` is a string, and first character in
                # `news_id_list` is comma.
                ava_news_idxs = data_obj['news_id_list'].split(',')[1:]
                # Get news indices within specified range.
                ava_news_idxs = map(
                    lambda news_idx:
                    int(re.search(r'(\d+)', news_idx).group(1)),
                    ava_news_idxs,
                )
                ava_news_idxs = filter(
                    lambda news_idx: first_idx <= news_idx <= latest_idx,
                    ava_news_idxs,
                )
                # Reture news index which is the closest to `latest_idx`.
                return max(ava_news_idxs)
        except Exception as err:
            if err.args:
                logger.update([err.args[0]])

        # Normally TVBS's API will return latest news index available directly.
        # So one only need to loop once.  We treat looping more than one times
        # as an indication of error occurences.
        fail_count += 1

        # No more news to crawl.  This happens when crawler got banned or there
        # is actually no news available.
        if fail_count >= continue_fail_count:
            break

    # Only show error statistics in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    # If we cannot find latest available news index, we skip crawling in the
    # current range.
    return first_idx


def get_all_available_news_idx(
    category: Final[str],
    first_idx: Final[int],
    latest_idx: Final[int],
    *,
    continue_fail_count: Final[Optional[int]] = 500,
    debug: Final[Optional[bool]] = False,
    **kwargs: Final[Optional[Dict]],
) -> List[int]:
    r"""Collecting all available news indices.

    In the responed JSON, there are only two fields we care about:
    - news_id_list:
          This is a list of news index disguises as a string.  Indices in the
          list also contains `newsid`.  Each news index surrounded by single
          quotes, with comma at the front.  For example:
          ",'123456','123457','123458'"
    - newsid:
          This is the smallest news index in `news_id_list`.
    """
    all_ava_news_idxs: List[int] = [latest_idx]
    category_api = CATEGORY_API_LOOKUP_TABLE[category]
    logger = Counter()
    fail_count = 0

    # Only show progress bar in debug mode.
    progress_bar = tqdm(
        desc='Collecting news ids',
        disable=not debug,
        dynamic_ncols=True,
    )
    current_idx = latest_idx
    while first_idx <= current_idx <= latest_idx:
        category_api_url = (
            f'{COMPANY_URL}news/LoadMoreOverview'
            + f'?limit=100&offset=0&cateid={category_api}'
            + f'&cate={category}&newsid={current_idx}'
        )
        try:
            response = news.crawlers.util.request_url.get(url=category_api_url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=category_api_url,
            )

            data_obj = response.json()

            # No more news indices were found.
            if not data_obj['news_id_list']:
                break

            # `news_id_list` is a string, and first character in `news_id_list`
            # is comma.
            ava_news_idxs = data_obj['news_id_list'].split(',')[1:]

            # Get news indices within specified range.
            ava_news_idxs = map(
                lambda news_idx: int(re.search(r'(\d+)', news_idx).group(1)),
                ava_news_idxs,
            )
            ava_news_idxs = filter(
                lambda news_idx: first_idx <= news_idx <= latest_idx,
                ava_news_idxs,
            )
            ava_news_idxs = list(ava_news_idxs)

            # Combine next news idx list into existed news idx list.
            all_ava_news_idxs.extend(ava_news_idxs)

            # We update current index with the smallest news index in
            # `data_obj['news_id_list']`.  Note that `current_idx` will
            # decrease through iteration (this is done by TVBS's API).
            current_idx = min(ava_news_idxs)

            # Reset `fail_count` if no error occurred.
            fail_count = 0
        except Exception as err:
            fail_count += 1

            if err.args:
                logger.update([err.args[0]])

        progress_bar.update()

        # No more news to crawl.  This happens when crawler got banned or there
        # is actually no news available.
        if fail_count >= continue_fail_count:
            break

    # Only show error statistics in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return list(set(all_ava_news_idxs))


def get_news_list(
    ava_news_idxs: Final[List[int]],
    category: Final[str],
    *,
    continue_fail_count: Final[Optional[int]] = 500,
    debug: Final[Optional[bool]] = False,
    **kwargs: Final[Optional[Dict]],
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()
    fail_count = 0

    # Only show progress bar in debug mode.
    for news_idx in tqdm(
            ava_news_idxs,
            desc='Crawling',
            disable=not debug,
            dynamic_ncols=True,
    ):
        news_url = f'{COMPANY_URL}{category}/{news_idx}'
        try:
            response = news.crawlers.util.request_url.get(url=news_url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=news_url,
            )

            news_list.append(
                RawNews(
                    company_id=COMPANY_ID,
                    raw_xml=news.crawlers.util.normalize.compress_raw_xml(
                        raw_xml=response.text,
                    ),
                    url_pattern=news.crawlers.util.normalize.compress_url(
                        url=news_url,
                        company_id=COMPANY_ID,
                    ),
                )
            )

            # Reset `fail_count` if no error occurred.
            fail_count = 0
        except Exception as err:
            fail_count += 1

            if err.args:
                logger.update([err.args[0]])

        # No more news to crawl.  This happens only when crawler got banned.
        if fail_count >= continue_fail_count:
            break

    # Only show error statistics in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


def main(
    db_name: Final[str],
    first_idx: Final[int],
    latest_idx: Final[int],
    *,
    records_per_commit: Final[Optional[int]] = 1000,
    **kwargs: Final[Optional[Dict]],
) -> None:
    # Value check.
    if first_idx <= 0:
        raise ValueError('Must have `first_idx > 0`.')
    if latest_idx <= 0:
        raise ValueError('Must have `latest_idx > 0`.')
    if first_idx > latest_idx:
        raise ValueError('Must have `first_idx <= latest_idx`.')

    # Get database connection.
    db_path = news.crawlers.db.util.get_db_path(db_name=db_name)
    conn = news.db.get_conn(db_path=db_path)
    cur = conn.cursor()

    # Ensure news table exists.
    news.crawlers.db.create.create_table(cur=cur)

    cur_latest_idx = latest_idx
    while first_idx <= cur_latest_idx:
        cur_first_idx = cur_latest_idx - records_per_commit
        cur_first_idx = max(cur_first_idx, first_idx)

        # Get news list with respect to each category.
        for category, category_api in CATEGORY_API_LOOKUP_TABLE.items():

            # Get latest available news index.
            cur_latest_ava_idx = get_latest_available_news_idx(
                category=category,
                first_idx=cur_first_idx,
                latest_idx=cur_latest_idx,
                **kwargs,
            )

            # Use latest available news index to get all available news indices
            # in specified range.
            ava_news_idxs = get_all_available_news_idx(
                category=category,
                first_idx=cur_first_idx,
                latest_idx=cur_latest_ava_idx,
                **kwargs,
            )

            news_list = get_news_list(
                ava_news_idxs=ava_news_idxs,
                category=category,
                **kwargs,
            )

            # Write news records to database.
            news.crawlers.db.write.write_new_records(
                cur=cur,
                news_list=news_list,
            )
            conn.commit()

        # Decrease crawling index.
        cur_latest_idx -= records_per_commit

    # Close database connection.
    conn.close()
