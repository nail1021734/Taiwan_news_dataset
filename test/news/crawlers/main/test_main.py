from datetime import datetime, timezone

import news.crawlers
from news.crawlers.main import CRAWLER_SCRIPT_LOOKUP_TABLE, main


def test_main(monkeypatch) -> None:

    def mock_crawler_script(**kwargs) -> None:
        assert kwargs['crawler_name'] in CRAWLER_SCRIPT_LOOKUP_TABLE
        assert kwargs['current_datetime'] == datetime(
            year=2021,
            month=10,
            day=13,
            tzinfo=timezone.utc,
        )
        assert kwargs['db_name'] == 'test.db'
        assert kwargs['debug']
        assert kwargs['first_idx'] == 123
        assert kwargs['latest_idx'] == 456
        assert kwargs['past_datetime'] == datetime(
            year=2021,
            month=10,
            day=12,
            tzinfo=timezone.utc,
        )

    monkeypatch.setattr(
        news.crawlers.main,
        'CRAWLER_SCRIPT_LOOKUP_TABLE',
        {
            'chinatimes': mock_crawler_script,
            'cna': mock_crawler_script,
            'epochtimes': mock_crawler_script,
            'ettoday': mock_crawler_script,
            'ftv': mock_crawler_script,
            'ltn': mock_crawler_script,
            'ntdtv': mock_crawler_script,
            'setn': mock_crawler_script,
            'storm': mock_crawler_script,
            'tvbs': mock_crawler_script,
            'udn': mock_crawler_script,
        },
    )

    for crawler_script in CRAWLER_SCRIPT_LOOKUP_TABLE.keys():
        main(
            [
                '--crawler_name',
                crawler_script,
                '--current_datetime',
                '2021-10-13+0000',
                '--db_name',
                'test.db',
                '--debug',
                '--first_idx',
                '123',
                '--latest_idx',
                '456',
                '--past_datetime',
                '2021-10-12+0000',
            ]
        )
