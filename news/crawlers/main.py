import argparse
import sys
import textwrap
from datetime import datetime, timedelta, timezone
from typing import Callable, Dict, List

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
import news.crawlers.util
import news.path

CRAWLER_SCRIPT_LOOKUP_TABLE: Dict[str, Callable] = {
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


def parse_args(argv: List[str]) -> argparse.Namespace:
    r"""Parse command line arguments.

    Example
    =======
    python -m news.crawlers.main           \
        --crawler_name chinatimes          \
        --current_datetime 2010-01-02+0000 \
        --db_name chinatimes.db            \
        --debug True                       \
        --past_datetime 2010-01-01+0000
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        '--crawler_name',
        choices=CRAWLER_SCRIPT_LOOKUP_TABLE.keys(),
        type=str,
        required=True,
        help=textwrap.dedent(
            """\
            Name of the crawler.  See `news/crawlers/README.md` for all
            available crawlers.
            """
        ),
    )
    parser.add_argument(
        '--db_name',
        type=str,
        required=True,
        help=textwrap.dedent(
            f"""\
            Name of the database to save crawled news.  Create file if given
            path does not exist (along with non-existed directories in the
            path).  If absolute path is given, then treat the given path as
            SQLite database file.

            For example, executing

                --db_name /abs/my.db

            will output crawled news to the file

                /abs/my.db

            If relative path is given, then we assume the given path is under
            the path `PROJECT_ROOT/data/raw`. Currently project root is set to
            {news.path.PROJECT_ROOT}.

            For example, executing

                --db_name rel/my.db

            will output crawled news to the file

                PROJECT_ROOT/data/raw/rel/my.db
            """
        ),
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help=textwrap.dedent(
            """\
            Select whether to use debug mode.  In debug mode it outputs
            progress bar to stderr and error messages to stdout.
            """
        ),
    )
    parser.add_argument(
        '--current_datetime',
        type=str,
        default=None,
        help=textwrap.dedent(
            """\
            The latest news published time wanted to include in crawling
            result.  `current_datetime` must follow the format (in utc
            timezone):

                YYYY-mm-dd+zzzz

            For example, 2014-01-29+0000 or 2021-10-12+0800.

            News published later than `current_datetime` will be discard.  Not
            all crawler use `current_datetime` argument.  To see which crawler
            use `current_datetime` argument, see `news/crawlers` for details.
            Set to `datetime.now(tz=timezone.utc)` if not present.
            """
        ),
    )
    parser.add_argument(
        '--past_datetime',
        type=str,
        default=None,
        help=textwrap.dedent(
            """\
            The earliest news published time wanted to include in crawling
            result.  `current_datetime` must follow the format (in utc
            timezone):

                YYYY-mm-dd+zzzz

            For example, 2014-01-29+0000 or 2021-10-12+0800.

            News published earlier than `past_datetime` will be discard.  Not
            all crawler use `past_datetime` argument.  To see which crawler use
            `past_datetime` argument, see `news/crawlers` for details. Set to
            `datetime.now(tz=timezone.utc) - timedelta(days=1)` if not present.
            """
        ),
    )
    parser.add_argument(
        '--first_idx',
        type=int,
        default=1,
        help=textwrap.dedent(
            """\
            The smallest news index wanted to include in crawling result.  News
            index smaller than `first_idx` will be discard.  Not all crawler
            use `first_idx` argument.  To see which crawler use `first_idx`
            argument, see `news/crawlers` for details.  Defaults to `1`.
            """
        ),
    )
    parser.add_argument(
        '--latest_idx',
        type=int,
        default=-1,
        help=textwrap.dedent(
            """\
            The largest news index wanted to include in crawling result.  Set
            to `-1` to crawle as much news as possible. News index larger than
            `latest_idx` will be discard.  Not all crawler use `latest_idx`
            argument.  To see which crawler use `latest_idx` argument, see
            `news/crawlers` for details.  Defaults to `-1`.
            """
        ),
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> None:
    args = parse_args(argv=argv)

    # `current_datetime` is default to now.
    if not args.current_datetime:
        args.current_datetime = datetime.now(tz=timezone.utc)
    else:
        args.current_datetime = datetime.strptime(
            args.current_datetime,
            '%Y-%m-%d%z',
        ).astimezone(tz=timezone.utc)

    # `past_datetime` is default to yesterday.
    if not args.past_datetime:
        args.past_datetime = args.current_datetime - timedelta(days=1)
    else:
        args.past_datetime = datetime.strptime(
            args.past_datetime,
            '%Y-%m-%d%z',
        ).astimezone(tz=timezone.utc)

    # Run crawler.
    crawler_script = CRAWLER_SCRIPT_LOOKUP_TABLE[args.crawler_name]
    crawler_script(**args.__dict__)


if __name__ == '__main__':
    main(argv=sys.argv[1:])
