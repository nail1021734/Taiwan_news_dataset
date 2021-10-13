from datetime import datetime, timezone

import news.crawlers.ntdtv


def test_get_datetime_from_url() -> None:
    r"""Must return instance of `datetime` in UTC timezone."""
    # Test case: bad input.
    bad_url = ''
    assert news.crawlers.ntdtv.get_datetime_from_url(url=bad_url) is None

    # Test case: good input.
    good_url = r'https://www.ntdtv.com/b5/2021/10/12/a123456789.html'
    news_datetime = news.crawlers.ntdtv.get_datetime_from_url(url=good_url)
    assert isinstance(news_datetime, datetime)
    assert news_datetime == datetime(
        year=2021,
        month=10,
        day=12,
        tzinfo=timezone.utc,
    )
