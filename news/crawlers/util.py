import random
import time

from requests import Response

BEFORE_BANNED_SLEEP_SECS = 0.0
AFTER_BANNED_SLEEP_SECS = 120.0
REQUEST_TIMEOUT = 60


def after_banned_sleep() -> None:
    time.sleep(AFTER_BANNED_SLEEP_SECS)


def before_banned_sleep() -> None:
    pass


def check_status_code(response: Response) -> None:
    # Got banned.
    if response.status_code == 403:
        after_banned_sleep()
        raise Exception('Got banned.')

    # Missing news or no news.
    if response.status_code in [404, 410]:
        raise Exception('News not found.')

    # Something weird happend.
    if response.status_code != 200:
        raise Exception('Weird.')

    # Status code 200.
    before_banned_sleep()
