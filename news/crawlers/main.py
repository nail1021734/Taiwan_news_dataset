import argparse
import sys
from datetime import datetime, timedelta, timezone
from typing import Callable, Dict, Final, List

import news.crawlers.chinatimes
import news.crawlers.cna
import news.crawlers.epochtimes
import news.crawlers.ettoday
import news.crawlers.ftv
import news.crawlers.ltn
import news.crawlers.ntdtv
import news.crawlers.setn
import news.crawlers.storm
import news.crawlers.tvbs
import news.crawlers.udn

CRAWLER_SCRIPT_LOOKUP_TABLE: Final[Dict[str, Callable]] = {
    'chinatimes': news.crawlers.chinatimes.main,
    'cna': news.crawlers.cna.main,
    'epochtimes': news.crawlers.epochtimes.main,
    'ettoday': news.crawlers.ettoday.main,
    'ftv': news.crawlers.ftv.main,
    'ltn': news.crawlers.ltn.main,
    'ntdtv': news.crawlers.ntdtv.main,
    'setn': news.crawlers.setn.main,
    'storm': news.crawlers.storm.main,
    'tvbs': news.crawlers.tvbs.main,
    'udn': news.crawlers.udn.main,
}


def parse_args(argv: Final[List[str]]) -> argparse.Namespace:
    r"""Parse command line arguments.

    Example
    =======
    python -m news.crawlers.main \
        --crawler_name chinatimes \
        --current_datetime 2010-01-02+0000
        --db_name chinatimes.db \
        --debug True \
        --past_datetime 2010-01-01+0000
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--crawler_name',
        choices=CRAWLER_SCRIPT_LOOKUP_TABLE.keys(),
        type=str,
        help='Select crawler.',
    )
    parser.add_argument(
        '--db_name',
        type=str,
        help='Name of the database to store news.',
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Select whether use debug mode.  In debug mode it outputs '
        'progress bar and error messages.',
    )
    parser.add_argument(
        '--current_datetime',
        type=str,
        default=None,
        help='Specify the upper bound of the news release time. (latest)',
    )
    parser.add_argument(
        '--past_datetime',
        type=str,
        default=None,
        help='Specify the lower bound of the news release time. (oldest)',
    )
    parser.add_argument(
        '--first_idx',
        type=int,
        default=1,
        help='Specify first news index. (smallest)',
    )
    parser.add_argument(
        '--latest_idx',
        type=int,
        default=-1,
        help='Specify latest news index. (largest)',
    )
    return parser.parse_args(argv)


def main(argv: Final[List[str]]) -> None:
    args = parse_args(argv=argv)

    # `current_datetime` is default to now.
    if not args.current_datetime:
        args.current_datetime = datetime.now(tz=timezone.utc)
    else:
        args.current_datetime = datetime.strptime(
            args.current_datetime,
            '%Y-%m-%d%z',
        )

    # `past_datetime` is default to yesterday.
    if not args.past_datetime:
        args.past_datetime = args.current_datetime - timedelta(days=1)
    else:
        args.past_datetime = datetime.strptime(
            args.past_datetime,
            '%Y-%m-%d%z',
        )

    # Run crawler.
    crawler_script = CRAWLER_SCRIPT_LOOKUP_TABLE[args.crawler_name]
    crawler_script(**args.__dict__)


if __name__ == '__main__':
    main(argv=sys.argv)
