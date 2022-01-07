from collections import Counter
from datetime import datetime, timezone
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

COMPANY_ID: int = news.crawlers.util.normalize.get_company_id(company='聯合報',)
COMPANY_URL: str = news.crawlers.util.normalize.get_company_url(
    company_id=COMPANY_ID,
)


def get_last_available_page(
    past_datetime: datetime,
    **kwargs: Optional[Dict],
) -> int:
    r"""Find last available page."""

    # Use exponential search to find an approximate upper bound of page number.
    # This algorithm is like TCP's congestion control protocal.
    for exp in range(17):
        # We expect there will be no more than 2 ** 16 = 65536 pages within
        # 100 year from 2021.
        page = 2**exp
        page_url = (
            f'{COMPANY_URL}api/more?page={page}'
            + '&channelId=2&type=cate_latest_news&totalRecNo=100'
        )
        try:
            response = news.crawlers.util.request_url.get(url=page_url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=page_url,
            )

            # UDN's API respond json.
            data_obj = response.json()

            # UND's API return json without `lists` field when there are no
            # more news.  This means we found an upper bound of page numbers.
            if not data_obj or 'lists' not in data_obj:
                break
        except Exception:
            # This only happen when crawler got banned or we have bugs.
            return 1

    # Use binary search to find precise upper bound of page number.  Note that
    # in this search we did not consider datetime constraints (we will do it in
    # the next search).  We initialize binary search lower and upper bound
    # according to previous search result.
    first_page = 2**(exp - 1)
    last_page = 2**exp
    break_state = None

    # Perform binary search.
    while first_page < last_page:
        mid_page = (first_page + last_page) // 2

        page_url = (
            f'{COMPANY_URL}api/more?page={mid_page}'
            + '&channelId=2&type=cate_latest_news&totalRecNo=100'
        )
        try:
            response = news.crawlers.util.request_url.get(url=page_url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=page_url,
            )

            # UDN's API respond json.
            data_obj = response.json()

            # UND's API return json without `lists` field when there are no
            # more news.  This means we found an upper bound of page numbers.
            if not data_obj or 'lists' not in data_obj:
                last_page = mid_page
                break_state = True
            else:
                first_page = mid_page + 1
                break_state = False
        except Exception:
            # This only happen when crawler got banned or we have bugs.
            return 1

    if break_state:
        return mid_page - 1
    return mid_page


def get_last_vaild_page(
    last_ava_page: int,
    past_datetime: datetime,
    **kwargs: Optional[Dict],
) -> int:
    r"""Find last page with `datetime >= past_datetime`."""
    # Use binary search to find precise upper bound of page number with
    # datetime constraint.  We initialize binary search lower and upper bound
    # according to the search result of the last available page number.
    first_page = 1
    last_page = last_ava_page
    break_state = None

    # Perform binary search.
    while first_page < last_page:
        mid_page = (first_page + last_page) // 2

        page_url = (
            f'{COMPANY_URL}api/more?page={mid_page}'
            + '&channelId=2&type=cate_latest_news&totalRecNo=100'
        )
        try:
            response = news.crawlers.util.request_url.get(url=page_url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=page_url,
            )

            # UDN's API respond json with datetime information.
            data_obj = response.json()
            news_datetimes = map(
                lambda o: o['time']['date'],
                data_obj['lists'],
            )
            news_datetimes = map(
                lambda nd: datetime.
                strptime(f'{nd} +0000', '%Y-%m-%d %H:%M %z'),
                news_datetimes,
            )

            # `lists` field is sorted by time.
            if min(news_datetimes) < past_datetime:
                last_page = mid_page
                break_state = True
            else:
                first_page = mid_page + 1
                break_state = False
        except Exception:
            # This only happen when crawler got banned or we have bugs.
            return 1

    if break_state:
        return mid_page - 1
    return mid_page


def get_first_vaild_page(
    last_valid_page: int,
    current_datetime: datetime,
    **kwargs: Optional[Dict],
) -> int:
    r"""Find first page with `datetime <= current_datetime`."""
    # Use binary search to find precise upper bound of page number with
    # datetime constraint.  We initialize binary search lower and upper bound
    # according to the search result of the last available page number.
    first_page = 1
    last_page = last_valid_page
    break_state = None

    # Perform binary search.
    while first_page < last_page:
        mid_page = (first_page + last_page) // 2

        page_url = (
            f'{COMPANY_URL}api/more?page={mid_page}'
            + '&channelId=2&type=cate_latest_news&totalRecNo=100'
        )
        try:
            response = news.crawlers.util.request_url.get(url=page_url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=page_url,
            )

            # UDN's API respond json with datetime information.
            data_obj = response.json()
            news_datetimes = map(
                lambda o: o['time']['date'],
                data_obj['lists'],
            )
            news_datetimes = map(
                lambda nd: datetime.
                strptime(f'{nd} +0000', '%Y-%m-%d %H:%M %z'),
                news_datetimes,
            )

            # `lists` field is sorted by time.
            if max(news_datetimes) < current_datetime:
                last_page = mid_page
                break_state = True
            else:
                first_page = mid_page + 1
                break_state = False
        except Exception:
            # This only happen when crawler got banned or we have bugs.
            return 1

    if break_state:
        return mid_page - 1
    return mid_page


def get_news_list(
    current_datetime: datetime,
    first_page: int,
    last_page: int,
    past_datetime: datetime,
    *,
    continue_fail_count: Optional[int] = 5,
    debug: Optional[bool] = False,
    **kwargs: Optional[Dict],
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()
    fail_count = 0

    # Only show progress bar in debug mode.
    for page in trange(
            first_page,
            last_page,
            desc='Crawling',
            disable=not debug,
            dynamic_ncols=True,
    ):
        # Cannot get news.  This situation is highly likely due to bugs.
        if fail_count >= continue_fail_count:
            break

        page_url = (
            f'{COMPANY_URL}api/more?page={page}'
            + '&channelId=2&type=cate_latest_news&totalRecNo=100'
        )
        try:
            response = news.crawlers.util.request_url.get(url=page_url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=page_url,
            )

            # Reset `fail_count` if no error occurred.
            fail_count = 0
        except Exception as err:
            fail_count += 1

            if err.args:
                logger.update([err.args[0]])
            continue

        data_obj = response.json()
        if 'lists' not in data_obj:
            fail_count += 1
            logger.update(['inconsistent api response.'])
            continue

        for o in data_obj['lists']:
            try:
                news_datetime = datetime.strptime(
                    f"{o['time']['date']} +0000",
                    '%Y-%m-%d %H:%M %z',
                )

                # News return from API will change through time.
                if not (past_datetime <= news_datetime <= current_datetime):
                    continue

                # Remove query string.
                news_url = o['titleLink'].split('?')[0]
                news_url = f'https://udn.com{news_url}'

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

            # Cannot get news.  This situation is highly likely due to bugs.
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
    *,
    commit_page_interval: Optional[int] = 10,
    **kwargs: Optional[Dict],
) -> None:
    r"""Crawling news using UDN's API.

    Note that `last_ava_page` will increase through time.
    """
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

    # We first find last available page number, then use last available page
    # number to find the last page number within datetime constraint, finally
    # do the same to find the first page number within datetime constraint.
    last_ava_page = get_last_available_page(
        past_datetime=past_datetime,
        **kwargs,
    )
    last_valid_page = get_last_vaild_page(
        last_ava_page=last_ava_page,
        past_datetime=past_datetime,
        **kwargs,
    )
    first_valid_page = get_first_vaild_page(
        last_valid_page=last_valid_page,
        current_datetime=current_datetime,
        **kwargs,
    )

    # Commit database when crawling 10 pages.  Use `last_valid_page + 1` to
    # make range inclusive.
    for first_page in range(
            first_valid_page,
            last_valid_page + 1,
            commit_page_interval,
    ):
        last_page = min(first_page + commit_page_interval, last_valid_page + 1)

        # Get news list.
        news_list = get_news_list(
            current_datetime=current_datetime,
            first_page=first_page,
            last_page=last_page,
            past_datetime=past_datetime,
            **kwargs,
        )

        # Write news records to database.
        news.crawlers.db.write.write_new_records(cur=cur, news_list=news_list)
        conn.commit()

    # Close database connection.
    conn.close()
