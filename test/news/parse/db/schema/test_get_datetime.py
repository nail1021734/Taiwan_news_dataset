from datetime import datetime, timezone

import news.parse.db.schema


def test_get_datetime() -> None:
    r"""Return correct datetime object."""
    timestamp = int(
        datetime(
            year=1995,
            month=10,
            day=12,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=timezone.utc,
        ).timestamp()
    )

    parsed_news = news.parse.db.schema.ParsedNews(
        idx=0,
        article='',
        category=None,
        company_id=0,
        reporter=None,
        timestamp=timestamp,
        title='',
        url_pattern='',
    )

    assert isinstance(parsed_news.get_datetime(), datetime)
    assert parsed_news.get_datetime().timestamp() == timestamp
