import textwrap
from datetime import datetime, timezone
from dataclasses import dataclass


@dataclass
class ParsedNews:
    idx: int = 0
    article: str = ''
    category: str = None  # Some `RawNews` does not have category.
    company_id: int = 0
    reporter: str = None  # Some `RawNews` does not have reporter.
    timestamp: int = 0
    title: str = ''
    url_pattern: str = ''

    def __iter__(self):
        yield self.idx
        yield self.article
        yield self.category
        yield self.company_id
        yield self.reporter
        yield self.timestamp
        yield self.title
        yield self.url_pattern

    def pretify(self) -> str:
        r"""Return informations with pretty format."""
        # Category can be `None`.
        if self.category:
            category = self.category
        else:
            category = 'None'

        # Convert timestamp to `YYYY-mm-dd HH:MM:SS+0000`.
        datetime_str = datetime.fromtimestamp(
            self.timestamp,
        ).astimezone(
            timezone.utc,
        ).strftime(
            '%Y-%m-%d %H:%M:%S%z',
        )

        # Reporter can be `None`.
        if self.reporter:
            reporter = self.reporter
        else:
            reporter = 'None'

        return textwrap.dedent(
            f'''\
            company_id:           {self.company_id}
            idx:                  {self.idx}
            url_pattern:          {self.url_pattern}
            datetime (timestamp): {self.timestamp}
            datetime (YYYYMMDD):  {datetime_str}

            category:
                {category}

            reporter:
                {reporter}

            title:
                {self.title}

            article:
                {self.article}
            '''
        )
