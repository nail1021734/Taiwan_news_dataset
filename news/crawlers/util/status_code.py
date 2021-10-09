import random
import time
from typing import Dict, Final, List, Optional

import news.crawlers.util.normalize

# Seconds to sleep before launching new request.  Set to 0.0 if the website is
# not blocking crawlers.
###############################################################################
#                        WARNING
# LTN, SETN, FTV, STORM, TVBS use cloudfront services and cloudfront will
# banned crawlers.
###############################################################################
SLEEP_SECS_BEFORE_BANNED_LOOKUP_TABLE: Final[Dict[int, float]] = {
    news.crawlers.util.normalize.get_company_id(company='中時'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='中央社'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='大紀元'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='東森'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='民視'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='自由'): 60.0,
    news.crawlers.util.normalize.get_company_id(company='新唐人'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='三立'): 60.0,
    # STORM response bad request with status 200.
    news.crawlers.util.normalize.get_company_id(company='風傳媒'): 1.0,
    news.crawlers.util.normalize.get_company_id(company='tvbs'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='聯合報'): 0.0,
}

# List lookup with index is O(1).  See `news.crawlers.util.normalize` for
# `company_id` information.
SLEEP_SECS_BEFORE_BANNED_FASTEST_LOOKUP_TABLE: List[float] = [
    SLEEP_SECS_BEFORE_BANNED_LOOKUP_TABLE[company_id]
    for company_id in sorted(SLEEP_SECS_BEFORE_BANNED_LOOKUP_TABLE.keys())
]

# Seconds to sleep when crawler get banned.  Set to 0.0 if the website is not
# blocking crawlers.
###############################################################################
#                        WARNING
# LTN, SETN, FTV, STORM, TVBS use cloudfront services and cloudfront will
# banned crawlers.
#
# FTV is set to 0.0 since it response 200 instead of 404 for missing pages.
# (The responding page will use javascript to redirect to actual 404 page.)
#
# STORM is set to 0.0 since it response 200 instead of 404 for missing pages.
#
# TVBS is set to 0.0 since we use API without bad request.
###############################################################################
SLEEP_SECS_AFTER_BANNED_LOOKUP_TABLE: Final[Dict[int, float]] = {
    news.crawlers.util.normalize.get_company_id(company='中時'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='中央社'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='大紀元'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='東森'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='民視'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='自由'): 86400.0,
    news.crawlers.util.normalize.get_company_id(company='新唐人'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='三立'): 86400.0,
    news.crawlers.util.normalize.get_company_id(company='風傳媒'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='tvbs'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='聯合報'): 86400.0,
}

# List lookup with index is O(1).  See `news.crawlers.util.normalize` for
# `company_id` information.
SLEEP_SECS_AFTER_BANNED_FASTEST_LOOKUP_TABLE: List[float] = [
    SLEEP_SECS_AFTER_BANNED_LOOKUP_TABLE[company_id]
    for company_id in sorted(SLEEP_SECS_AFTER_BANNED_LOOKUP_TABLE.keys())
]


# Seconds to sleep when crawler get banned by 429.  Set to 0.0 if the website
# is not blocking crawlers.
###############################################################################
#                        WARNING
# LTN, SETN, FTV, STORM, TVBS use cloudfront services and cloudfront will
# banned crawlers.
###############################################################################
SLEEP_SECS_AFTER_429_LOOKUP_TABLE: Final[Dict[int, float]] = {
    news.crawlers.util.normalize.get_company_id(company='中時'): 120.0,
    news.crawlers.util.normalize.get_company_id(company='中央社'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='大紀元'): 120.0,
    news.crawlers.util.normalize.get_company_id(company='東森'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='民視'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='自由'): 120.0,
    news.crawlers.util.normalize.get_company_id(company='新唐人'): 120.0,
    news.crawlers.util.normalize.get_company_id(company='三立'): 120.0,
    news.crawlers.util.normalize.get_company_id(company='風傳媒'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='tvbs'): 0.0,
    news.crawlers.util.normalize.get_company_id(company='聯合報'): 120.0,
}

# List lookup with index is O(1).  See `news.crawlers.util.normalize` for
# `company_id` information.
SLEEP_SECS_AFTER_429_FASTEST_LOOKUP_TABLE: List[float] = [
    SLEEP_SECS_AFTER_429_LOOKUP_TABLE[company_id]
    for company_id in sorted(SLEEP_SECS_AFTER_429_LOOKUP_TABLE.keys())
]


def gen_non_neg(
    *,
    mu: Final[Optional[float]] = 1.0,
    sigma: Final[Optional[float]] = 2.0,
    upper_bound: Final[Optional[float]] = 10.0,
) -> float:
    r"""Sample non-negative random numbers from normal distribution."""
    rand_secs = random.gauss(mu=mu, sigma=sigma)
    # Avoid negative random seconds and large random seconds.
    while rand_secs < 0.0 or rand_secs > upper_bound:
        rand_secs = random.gauss(mu=mu, sigma=sigma)
    return rand_secs


def sleep_after_banned(company_id: Final[int]) -> None:
    r"""Sleep specified seconds when got banned.

    Sleeping seconds only depends on `company_id`, which are set based on
    experiments.
    """
    secs = SLEEP_SECS_AFTER_BANNED_FASTEST_LOOKUP_TABLE[company_id]
    if secs != 0.0:
        time.sleep(secs + gen_non_neg())


def sleep_after_429(company_id: Final[int]) -> None:
    r"""Sleep specified seconds when launching too many request.

    Sleeping seconds only depends on `company_id`, which are set based on
    experiments.
    """
    secs = SLEEP_SECS_AFTER_429_FASTEST_LOOKUP_TABLE[company_id]
    if secs != 0.0:
        time.sleep(secs + gen_non_neg())


def sleep_before_banned(company_id: Final[int]) -> None:
    r"""Sleep specified seconds between each request.

    Sleeping seconds only depends on `company_id`, which are set based on
    experiments.
    """
    secs = SLEEP_SECS_BEFORE_BANNED_FASTEST_LOOKUP_TABLE[company_id]
    if secs != 0.0:
        time.sleep(secs + gen_non_neg())


def check_status_code(
    company_id: Final[int],
    status_code: Final[int],
    url: Final[str],
) -> None:
    r"""Sleep specified seconds based on `company_id` and `status_code`.

    Sleeping seconds only depends on `company_id`, which are set based on
    experiments.

    If status code is 403 (which means requests got banned), then this function
    trigger sleeping process automatically (the sleeping interval is very
    long).  The purpose of sleeping is to wait for the host unbannded crawlers
    IP address.  See `sleep_after_banned` for sleeping details.

    If status code is 404 or 410 (which means URL not found), then this
    function trigger sleeping process automatically (the sleeping interval is
    very short).  The purpose of sleeping is to avoid launching too many bad
    requests which will get banned at the end.  See `sleep_before_banned` for
    sleeping details.  Note that ETtoday use 410 instead of 404.

    If status code is 429 (which means too many requests), then this function
    trigger sleeping process automatically (the sleeping interval is short).
    The purpose of sleeping is to avoid launching too many requests (either
    good or bad) since host is already warning. This type of blocking usually
    get release in a short interval.

    If status code is not 200 or any status codes described above, then this
    function treat this case as 404.

    If status code is 200, do nothing.
    """
    # Got banned.
    if status_code == 403:
        sleep_after_banned(company_id=company_id)
        raise Exception('Got banned.')

    # Missing news or no news.
    # ETtoday use 410 instead of 404.
    if status_code in [404, 410]:
        sleep_before_banned(company_id=company_id)
        raise Exception('URL not found.')

    # To many consecutive requests or too many crawler at the same time.
    if status_code == 429:
        sleep_after_429(company_id=company_id)
        raise Exception('Too many requests.')

    # Something weird happend.
    if status_code != 200:
        sleep_before_banned(company_id=company_id)
        raise Exception(f'{url} is weird.')

    # Do nothing when status code 200.
    return
