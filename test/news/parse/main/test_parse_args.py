import argparse

import news.parse.main


def test_parse_args() -> None:
    args = news.parse.main.parse_args(
        argv=[
            '--db_name',
            'rel/my.db',
            '--db_name',
            '/abs/my.db',
            '--db_dir',
            'rel_dir',
            '--db_dir',
            '/abs_dir',
            '--debug',
            '--save_db_name',
            'out.db',
        ]
    )
    assert isinstance(args, argparse.Namespace)
    assert args.db_name == ['rel/my.db', '/abs/my.db']
    assert args.db_dir == ['rel_dir', '/abs_dir']
    assert args.debug
    assert args.save_db_name == 'out.db'
