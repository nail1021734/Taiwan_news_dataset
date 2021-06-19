import random
import time

from requests import Response

# Times (in seconds) to sleep for each request. Currently set to 0 since no
# website is blocking us.
BEFORE_BANNED_SLEEP_SECS = {
    'apple': 0.0,
    'chinatimes': 0.0,
    'cna': 0.0,
    'epochtimes': 0.0,
    'ettoday': 0.0,
    'ltn': 1.0,
    'ntdtv': 0.0,
    'setn': 0.0,
    'storm': 0.0,
    'tvbs': 0.0,
    'uni': 0.0,
    'yahoo': 0.0,
}
# Times (in seconds) to sleep when crawler get banned. Currently set to 0 since
# no website is blocking us. Note that ltn will ban us.
AFTER_BANNED_SLEEP_SECS = {
    'apple': 0.0,
    'chinatimes': 0.0,
    'cna': 0.0,
    'epochtimes': 0.0,
    'ettoday': 0.0,
    'ltn': 0.0,
    'ntdtv': 0.0,
    'setn': 0.0,
    'storm': 0.0,
    'tvbs': 0.0,
    'uni': 0.0,
    'yahoo': 0.0,
}
REQUEST_TIMEOUT = 60


def after_banned_sleep(company: str) -> None:
    time.sleep(AFTER_BANNED_SLEEP_SECS[company])


def before_banned_sleep(company: str) -> None:
    time.sleep(BEFORE_BANNED_SLEEP_SECS[company])


def check_status_code(company: str, response: Response) -> None:
    # Got banned.
    if response.status_code == 403:
        after_banned_sleep(company=company)
        raise Exception('Got banned.')

    # Missing news or no news.
    # ETtoday use 410 instead of 404.
    if response.status_code in [404, 410]:
        raise Exception('News not found.')

    # Something weird happend.
    if response.status_code != 200:
        raise Exception(f'{response.url} is weird.')

    # Status code 200.
    before_banned_sleep(company=company)
