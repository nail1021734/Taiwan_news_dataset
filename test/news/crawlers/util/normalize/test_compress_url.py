import news.crawlers.util.normalize


def test_compress_url() -> None:
    r"""Must remove url prefix."""
    assert (
        news.crawlers.util.normalize.compress_url(
            company_id=0,
            url=r'https://www.chinatimes.com/realtimenews/abc',
        )
        ==
        r'abc'
    )
    assert (
        news.crawlers.util.normalize.compress_url(
            company_id=1,
            url=r'https://www.cna.com.tw/abc',
        )
        ==
        r'abc'
    )
    assert (
        news.crawlers.util.normalize.compress_url(
            company_id=2,
            url=r'https://www.epochtimes.com/abc',
        )
        ==
        r'abc'
    )
    assert (
        news.crawlers.util.normalize.compress_url(
            company_id=3,
            url=r'https://star.ettoday.net/abc',
        )
        ==
        r'abc'
    )
    assert (
        news.crawlers.util.normalize.compress_url(
            company_id=4,
            url=r'https://www.ftvnews.com.tw/abc',
        )
        ==
        r'abc'
    )
    assert (
        news.crawlers.util.normalize.compress_url(
            company_id=5,
            url=r'https://news.ltn.com.tw/abc',
        )
        ==
        r'abc'
    )
    assert (
        news.crawlers.util.normalize.compress_url(
            company_id=6,
            url=r'https://www.ntdtv.com/abc',
        )
        ==
        r'abc'
    )
    assert (
        news.crawlers.util.normalize.compress_url(
            company_id=7,
            url=r'https://www.setn.com/abc',
        )
        ==
        r'abc'
    )
    assert (
        news.crawlers.util.normalize.compress_url(
            company_id=8,
            url=r'https://www.storm.mg/abc',
        )
        ==
        r'abc'
    )
    assert (
        news.crawlers.util.normalize.compress_url(
            company_id=9,
            url=r'https://news.tvbs.com.tw/abc',
        )
        ==
        r'abc'
    )
    assert (
        news.crawlers.util.normalize.compress_url(
            company_id=10,
            url=r'https://udn.com/news/abc',
        )
        ==
        r'abc'
    )
