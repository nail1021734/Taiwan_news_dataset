import test.news.crawlers.conftest

import news.crawlers.db.schema
import news.crawlers.ettoday
import news.crawlers.util.request_url


def test_get_news_list() -> None:
    r"""Crawling news with index ranging from 2100000 to 2100100."""
    news_list = news.crawlers.ettoday.get_news_list(
        continue_fail_count=3,
        debug=False,
        first_idx=2100000,
        latest_idx=2100100,
    )

    # If news were successfully crawled, then `news_list` is not empty.
    assert len(news_list) >= 1

    for n in news_list:
        assert isinstance(n, news.crawlers.db.schema.RawNews)
        assert isinstance(n.idx, int)
        assert n.company_id == news.crawlers.ettoday.COMPANY_ID
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

    news.crawlers.ettoday.get_news_list(
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

    news.crawlers.ettoday.get_news_list(
        continue_fail_count=1,
        debug=True,
        first_idx=1,
        latest_idx=2,
    )
    captured = capsys.readouterr()

    assert 'URL not found.' in captured.out
