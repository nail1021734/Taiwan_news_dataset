import test.news.crawlers.conftest

import news.crawlers.db.schema
import news.crawlers.storm
import news.crawlers.util.request_url


def test_get_news_list() -> None:
    r"""Crawling news with index ranging from 3992300 to 3992400."""
    news_list = news.crawlers.storm.get_news_list(
        continue_fail_count=50,
        debug=False,
        first_idx=3992300,
        latest_idx=3992400,
    )

    # If news were successfully crawled, then `news_list` is not empty.
    assert len(news_list) >= 1

    for n in news_list:
        assert isinstance(n, news.crawlers.db.schema.RawNews)
        assert isinstance(n.idx, int)
        assert n.company_id == news.crawlers.storm.COMPANY_ID
        assert isinstance(n.raw_xml, str)
        assert isinstance(n.url_pattern, str)


def test_show_progress_bar(
    response_200: test.news.crawlers.conftest.MockResponse,
    capsys,
    monkeypatch,
) -> None:
    r"""Must show progress bar when `debug = True`."""

    def mock_get(**kwargs) -> test.news.crawlers.conftest.MockResponse:
        return response_200

    monkeypatch.setattr(
        news.crawlers.util.request_url,
        'get',
        mock_get,
    )

    news.crawlers.storm.get_news_list(
        continue_fail_count=1,
        debug=True,
        first_idx=1,
        latest_idx=2,
    )
    captured = capsys.readouterr()

    # `tqdm` will output to stderr and thus `captured.err` is not empty.
    assert 'Crawling' in captured.err


def test_show_error_statistics(
    response_410: test.news.crawlers.conftest.MockResponse,
    capsys,
    monkeypatch,
) -> None:
    r"""Must show error statistics when `debug = True`."""

    def mock_get(**kwargs) -> test.news.crawlers.conftest.MockResponse:
        return response_410

    monkeypatch.setattr(
        news.crawlers.util.request_url,
        'get',
        mock_get,
    )

    news.crawlers.storm.get_news_list(
        continue_fail_count=1,
        debug=True,
        first_idx=1,
        latest_idx=2,
    )
    captured = capsys.readouterr()

    assert 'URL not found.' in captured.out
