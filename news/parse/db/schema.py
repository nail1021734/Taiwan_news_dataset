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

        idx_str = str(self.idx)
        company_id_str = str(self.company_id)
        url_pattern = self.url_pattern
        timestamp_str = str(self.timestamp)
        datetime_str = self.get_datetime_str()

        # Category can be `None`.
        if self.category:
            category_str = self.category
        else:
            category_str = 'None'

        # Reporter can be `None`.
        if self.reporter:
            reporter_str = self.reporter
        else:
            reporter_str = 'None'

        # Calculate column width.
        header_len = max(
            map(
                len,
                [
                    idx_str,
                    company_id_str,
                    url_pattern,
                    timestamp_str,
                    datetime_str,
                ],
            )
        )
        header_text = '-' * header_len
        idx_str = idx_str.ljust(header_len)
        company_id_str = company_id_str.ljust(header_len)
        url_pattern = url_pattern.ljust(header_len)
        timestamp_str = timestamp_str.ljust(header_len)
        datetime_str = datetime_str.ljust(header_len)

        return textwrap.dedent(
            f'''\
            +-------------------------------------+-{header_text   }-+
            | idx                                 | {idx_str       } |
            +-------------------------------------+-{header_text   }-+
            | company_id                          | {company_id_str} |
            +-------------------------------------+-{header_text   }-+
            | url_pattern                         | {url_pattern   } |
            +-------------------------------------+-{header_text   }-+
            | datetime (timestamp)                | {timestamp_str } |
            +-------------------------------------+-{header_text   }-+
            | datetime (YYYY-mm-dd HH:MM:SS+0000) | {datetime_str  } |
            +-------------------------------------+-{header_text   }-+

            category:
                {category_str}

            reporter:
                {reporter_str}

            title:
                {self.title}

            article:
            {self.article}
            '''
        )
