import random
import time

before_banned_sleep_secs = 0
after_banned_sleep_secs = 120


def before_banned_sleep() -> None:
    pass


def after_banned_sleep() -> None:
    time.sleep(after_banned_sleep_secs)
