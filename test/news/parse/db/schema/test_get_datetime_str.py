from datetime import datetime, timezone

import news.parse.db.schema


def test_get_datetime_str() -> None:
    r"""Return correct datetime string format."""
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

    assert parsed_news.get_datetime_str() == '1995-10-12 00:00:00+0000'
