import argparse

import news.crawlers.main


def test_parse_args() -> None:
    args = news.crawlers.main.parse_args(
        argv=[
            '--crawler_name',
            'chinatimes',
            '--current_datetime',
            '2010-01-02+0000',
            '--db_name',
            'chinatimes.db',
            '--debug',
            '--past_datetime',
            '2010-01-01+0000',
        ]
    )
    assert isinstance(args, argparse.Namespace)
    assert args.crawler_name == 'chinatimes'
    assert args.current_datetime == '2010-01-02+0000'
    assert args.db_name == 'chinatimes.db'
    assert args.debug
    assert args.past_datetime == '2010-01-01+0000'
