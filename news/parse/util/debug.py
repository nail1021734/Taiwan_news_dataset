import textwrap
from datetime import datetime, timezone
from typing import Final

import news.crawlers.util.normalize
import news.parse.db.schema


def pretty_print(parsed_news: Final[news.parse.db.schema.ParsedNews]) -> None:
    r"""Print each field to command line."""
    # Retrieve fields.
    idx = parsed_news.idx
    article = parsed_news.article
    if parsed_news.category:
        category = parsed_news.category
    else:
        category = 'None'
    company_id = parsed_news.company_id
    datetime_timestamp = parsed_news.datetime
    datetime_str = datetime.fromtimestamp(
        parsed_news.datetime,
    ).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z')
    if parsed_news.reporter:
        reporter = parsed_news.reporter
    else:
        reporter = 'None'
    title = parsed_news.title
    url_pattern = parsed_news.url_pattern

    # Print to CLI.
    print(
        textwrap.dedent(
            f'''\
            company_id:           {company_id}
            idx:                  {idx}
            url_pattern:          {url_pattern}
            datetime (timestamp): {datetime_timestamp}
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
    )
