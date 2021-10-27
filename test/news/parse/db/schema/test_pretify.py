import textwrap
from datetime import datetime, timezone

import news.parse.db.schema


def test_pretify() -> None:
    r"""Ensure format consistency."""
    idx = 123
    article = 'abc'
    category = 'def'
    company_id = 456
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
    reporter = 'ghi'
    title = 'jkl'
    url_pattern = 'mno'

    parsed_news = news.parse.db.schema.ParsedNews(
        idx=idx,
        article=article,
        category=category,
        company_id=company_id,
        reporter=reporter,
        timestamp=timestamp,
        title=title,
        url_pattern=url_pattern,
    )
    datetime_str = parsed_news.get_datetime_str()

    assert parsed_news.pretify() == textwrap.dedent(
        f'''\
        company_id:           {company_id}
        idx:                  {idx}
        url_pattern:          {url_pattern}
        datetime (timestamp): {timestamp}
        datetime (YYYYMMDD):  {datetime_str}

        category:
            {category}

        reporter:
            {reporter}

        title:
            {title}

        article:
            {article}
        '''
    )


def test_default_category() -> None:
    r"""Must show `None` when category is empty."""
    idx = 123
    article = 'abc'
    company_id = 456
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
    reporter = 'ghi'
    title = 'jkl'
    url_pattern = 'mno'

    parsed_news = news.parse.db.schema.ParsedNews(
        idx=idx,
        article=article,
        category=None,
        company_id=company_id,
        reporter=reporter,
        timestamp=timestamp,
        title=title,
        url_pattern=url_pattern,
    )
    datetime_str = parsed_news.get_datetime_str()

    assert parsed_news.pretify() == textwrap.dedent(
        f'''\
        company_id:           {company_id}
        idx:                  {idx}
        url_pattern:          {url_pattern}
        datetime (timestamp): {timestamp}
        datetime (YYYYMMDD):  {datetime_str}

        category:
            None

        reporter:
            {reporter}

        title:
            {title}

        article:
            {article}
        '''
    )


def test_default_reporter() -> None:
    r"""Must show `None` when reporter is empty."""
    idx = 123
    article = 'abc'
    category = 'def'
    company_id = 456
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
    title = 'jkl'
    url_pattern = 'mno'

    parsed_news = news.parse.db.schema.ParsedNews(
        idx=idx,
        article=article,
        category=category,
        company_id=company_id,
        reporter=None,
        timestamp=timestamp,
        title=title,
        url_pattern=url_pattern,
    )
    datetime_str = parsed_news.get_datetime_str()

    assert parsed_news.pretify() == textwrap.dedent(
        f'''\
        company_id:           {company_id}
        idx:                  {idx}
        url_pattern:          {url_pattern}
        datetime (timestamp): {timestamp}
        datetime (YYYYMMDD):  {datetime_str}

        category:
            {category}

        reporter:
            None

        title:
            {title}

        article:
            {article}
        '''
    )
