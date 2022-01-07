from time import time

import news.crawlers.util.status_code


def test_sleep_enough() -> None:
    r"""Must sleep enough time."""
    tolerance_secs = 2.0

    time_start = time()
    news.crawlers.util.status_code.sleep_after_banned(company_id=0)
    time_end = time()
    time_diff = abs(time_end - time_start)
    assert (
        abs(
            time_diff - news.crawlers.util.status_code
            .SLEEP_SECS_AFTER_BANNED_FASTEST_LOOKUP_TABLE[0]
        ) < tolerance_secs
    )
