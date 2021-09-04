import argparse
import time
from datetime import datetime, timedelta, timezone

import dateutil.parser

import news.crawlers

CRAWLER_DICT = {
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


def parse_argument():
    r'''
    `crawler_name` example: 'cna'
    `current_datetime` example: 2021-06-24T00:00:00Z
    `first_id` example: 55688
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--crawler_name',
        choices=CRAWLER_DICT.keys(),
        type=str,
        help='Select crawler.',
    )
    parser.add_argument(
        '--db_name',
        type=str,
        help='Assign database to store news.',
    )
    parser.add_argument(
        '--debug',
        type=bool,
        default=False,
        help='Select whether use debug mode.',
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
        help='Specify first index id. (smallest)',
    )
    parser.add_argument(
        '--latest_idx',
        type=int,
        default=-1,
        help='Specify latest index id. (largest)',
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = parse_argument()

    # Defaule `current_datetime` now.
    if not args.current_datetime:
        args.current_datetime = datetime.now(timezone.utc)
    else:
        args.current_datetime = dateutil.parser.isoparse(
            args.current_datetime
        )

    # Default crawl one day news.
    if not args.past_datetime:
        args.past_datetime = args.current_datetime - timedelta(days=1)
    else:
        args.past_datetime = dateutil.parser.isoparse(
            args.past_datetime
        )

    # Run crawler.
    func = CRAWLER_DICT[args.crawler_name]
    param = dict((k, v) for k, v in vars(args).items()
                 if k in func.__code__.co_varnames)
    func(**param)
