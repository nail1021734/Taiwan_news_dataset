import textwrap
from dataclasses import dataclass
from datetime import datetime, timezone


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

    def get_datetime(self) -> datetime:
        r"""Return datetime object in UTC timezone."""
        return datetime.fromtimestamp(self.timestamp).astimezone(timezone.utc)

    def get_datetime_str(self) -> str:
        r"""Convert `self.timestamp` to `YYYY-mm-dd HH:MM:SS+0000`."""
        return self.get_datetime().strftime('%Y-%m-%d %H:%M:%S%z')

    def pretify(self) -> str:
        r"""Return informations with pretty format."""
        # Category can be `None`.
        if self.category:
            category = self.category
        else:
            category = 'None'

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
            datetime (YYYYMMDD):  {self.get_datetime_str()}

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
