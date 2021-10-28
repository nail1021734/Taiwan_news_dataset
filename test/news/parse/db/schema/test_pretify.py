import textwrap
from datetime import datetime, timezone

import news.parse.db.schema


def test_pretify() -> None:
    r"""Ensure format consistency."""
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
        idx=123,
        article='abc',
        category='def',
        company_id=456,
        reporter='ghi',
        timestamp=timestamp,
        title='jkl',
        url_pattern='mno',
    )

    assert parsed_news.pretify() == textwrap.dedent(
        '''\
        +-------------------------------------+--------------------------+
        | idx                                 | 123                      |
        +-------------------------------------+--------------------------+
        | company_id                          | 456                      |
        +-------------------------------------+--------------------------+
        | url_pattern                         | mno                      |
        +-------------------------------------+--------------------------+
        | datetime (timestamp)                | 813456000                |
        +-------------------------------------+--------------------------+
        | datetime (YYYY-mm-dd HH:MM:SS+0000) | 1995-10-12 00:00:00+0000 |
        +-------------------------------------+--------------------------+

        category:
            def

        reporter:
            ghi

        title:
            jkl

        article:
        abc
        '''
    )


def test_default_category() -> None:
    r"""Must show `None` when category is empty."""
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
        idx=123,
        article='abc',
        category=None,
        company_id=456,
        reporter='ghi',
        timestamp=timestamp,
        title='jkl',
        url_pattern='mno',
    )

    assert parsed_news.pretify() == textwrap.dedent(
        '''\
        +-------------------------------------+--------------------------+
        | idx                                 | 123                      |
        +-------------------------------------+--------------------------+
        | company_id                          | 456                      |
        +-------------------------------------+--------------------------+
        | url_pattern                         | mno                      |
        +-------------------------------------+--------------------------+
        | datetime (timestamp)                | 813456000                |
        +-------------------------------------+--------------------------+
        | datetime (YYYY-mm-dd HH:MM:SS+0000) | 1995-10-12 00:00:00+0000 |
        +-------------------------------------+--------------------------+

        category:
            None

        reporter:
            ghi

        title:
            jkl

        article:
        abc
        '''
    )


def test_default_reporter() -> None:
    r"""Must show `None` when reporter is empty."""
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
        idx=123,
        article='abc',
        category='def',
        company_id=456,
        reporter=None,
        timestamp=timestamp,
        title='jkl',
        url_pattern='mno',
    )

    assert parsed_news.pretify() == textwrap.dedent(
        '''\
        +-------------------------------------+--------------------------+
        | idx                                 | 123                      |
        +-------------------------------------+--------------------------+
        | company_id                          | 456                      |
        +-------------------------------------+--------------------------+
        | url_pattern                         | mno                      |
        +-------------------------------------+--------------------------+
        | datetime (timestamp)                | 813456000                |
        +-------------------------------------+--------------------------+
        | datetime (YYYY-mm-dd HH:MM:SS+0000) | 1995-10-12 00:00:00+0000 |
        +-------------------------------------+--------------------------+

        category:
            def

        reporter:
            None

        title:
            jkl

        article:
        abc
        '''
    )
