import textwrap
from datetime import datetime, timezone

import news.parse.db.schema


def test_pretify() -> None:
    r"""Instance of `ParsedNews` must be iterable.

    Iterator will generate following attributes in order:
    - `idx`
    - `article`
    - `category`
    - `company_id`
    - `datetime`
    - `reporter`
    - `title`
    - `url_pattern`
    """
    idx = 123
    article = 'abc'
    category = 'def'
    company_id = 456
    timestamp = datetime.now().timestamp()
    datetime_str = datetime.fromtimestamp(
        timestamp,
    ).astimezone(
        timezone.utc,
    ).strftime(
        '%Y-%m-%d %H:%M:%S%z',
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
