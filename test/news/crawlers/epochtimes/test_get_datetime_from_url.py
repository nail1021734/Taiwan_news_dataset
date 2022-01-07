from datetime import datetime, timezone

import news.crawlers.epochtimes


def test_get_datetime_above_2010_from_url() -> None:
    r"""Must return instance of `datetime` in UTC timezone."""
    # Test case: bad input.
    bad_url = ''
    assert news.crawlers.epochtimes.get_datetime_from_url(url=bad_url) is None

    # Test case: good input.
    good_url = r'https://www.epochtimes.com/b5/17/10/12/n12345678.htm'
    news_datetime = news.crawlers.epochtimes.get_datetime_from_url(
        url=good_url,
    )
    assert isinstance(news_datetime, datetime)
    assert news_datetime == datetime(
        year=2017,
        month=10,
        day=12,
        tzinfo=timezone.utc,
    )


def test_get_datetime_below_2010_from_url() -> None:
    r"""Must return instance of `datetime` in UTC timezone."""
    # Test case: bad input.
    bad_url = ''
    assert news.crawlers.epochtimes.get_datetime_from_url(url=bad_url) is None

    # Test case: good input.
    good_url = r'https://www.epochtimes.com/b5/5/10/12/n12345678.htm'
    news_datetime = news.crawlers.epochtimes.get_datetime_from_url(
        url=good_url,
    )
    assert isinstance(news_datetime, datetime)
    assert news_datetime == datetime(
        year=2005,
        month=10,
        day=12,
        tzinfo=timezone.utc,
    )
