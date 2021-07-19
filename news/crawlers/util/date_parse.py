import re
import dateutil.parser


def epochtimes(url):
    URL_PATTERN = re.compile(
        r'https://www.epochtimes.com/b5/(\d+)/(\d+)/(\d+)/n\d+\.htm'
    )
    match = URL_PATTERN.match(url)
    year = int(match.group(1))
    month = int(match.group(2))
    day = int(match.group(3))
    news_datetime = dateutil.parser.isoparse(
        f"20{year:02d}-{month:02d}-{day:02d}T00:00:00Z"
    )
    return news_datetime
