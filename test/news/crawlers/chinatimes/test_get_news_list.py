import test.news.crawlers.conftest
from datetime import datetime, timedelta
from typing import Final

import news.crawlers.chinatimes
import news.crawlers.db.schema
import news.crawlers.util.request_url


def test_get_news_list(capsys: Final) -> None:
    r"""Crawling news on October 12th, 2020."""
    continue_fail_count = 5

    news_list = news.crawlers.chinatimes.get_news_list(
        continue_fail_count=continue_fail_count,
        current_datetime=datetime(
            year=2020,
            month=10,
            day=12,
            hour=0,
            minute=0,
            second=0,
        ),
        debug=False,
    )
    captured = capsys.readouterr()

    # If news were successfully crawled, then `news_list` is not empty.
    # Otherwise output log messages to stdout.
    assert (
        len(news_list) + len(captured.out.strip().split('\n'))
        <=
        continue_fail_count
    )

    for n in news_list:
        assert isinstance(n, news.crawlers.db.schema.RawNews)


def test_show_progress_bar(
    response_200: Final[test.news.crawlers.conftest.MockResponse],
    capsys: Final,
    monkeypatch: Final,
) -> None:
    r"""Must show progress bar when `debug = True`."""

    def mock_get(**kwargs) -> test.news.crawlers.conftest.MockResponse:
        return response_200

    monkeypatch.setattr(
        news.crawlers.util.request_url,
        'get',
        mock_get,
    )

    news.crawlers.chinatimes.get_news_list(
        continue_fail_count=1,
        current_datetime=datetime.now() - timedelta(days=1),
        debug=True,
    )
    captured = capsys.readouterr()

    # `tqdm` will output to stderr and thus `captured.err` is not empty.
    assert captured.err
