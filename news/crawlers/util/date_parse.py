import re
from datetime import datetime
from typing import Final

import dateutil.parser

NTDTV_URL_PATTERN = re.compile(
    r'https://www.ntdtv.com/b5/(\d+)/(\d+)/(\d+)/a\d+.html'
)


def ntdtv(url: Final[str]) -> datetime:
    r"""從網址取得 ntdtv 新聞的日期."""
    match = NTDTV_URL_PATTERN.match(url)
    year = int(match.group(1))
    month = int(match.group(2))
    day = int(match.group(3))
    news_datetime = dateutil.parser.isoparse(
        f'{year:04d}-{month:02d}-{day:02d}T00:00:00Z'
    )
    return news_datetime
