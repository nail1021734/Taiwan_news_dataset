import news.crawlers.util.normalize


def test_get_company_url() -> None:
    r"""Must reserve company id and url mapping."""
    assert news.crawlers.util.normalize.get_company_url(0) \
        == r'https://www.chinatimes.com/'
    assert news.crawlers.util.normalize.get_company_url(1) \
        == r'https://www.cna.com.tw/news/aipl/'
    assert news.crawlers.util.normalize.get_company_url(2) \
        == r'https://www.epochtimes.com/b5/'
    assert news.crawlers.util.normalize.get_company_url(3) \
        == r'https://star.ettoday.net/news/'
    assert news.crawlers.util.normalize.get_company_url(4) \
        == r'https://www.ftvnews.com.tw/news/detail/'
    assert news.crawlers.util.normalize.get_company_url(5) \
        == r'https://news.ltn.com.tw/ajax/breakingnews/'
    assert news.crawlers.util.normalize.get_company_url(6) \
        == r'https://www.ntdtv.com/b5/'
    assert news.crawlers.util.normalize.get_company_url(7) \
        == r'https://www.setn.com/'
    assert news.crawlers.util.normalize.get_company_url(8) \
        == r'https://www.storm.mg/article/'
    assert news.crawlers.util.normalize.get_company_url(9) \
        == r'https://news.tvbs.com.tw/'
    assert news.crawlers.util.normalize.get_company_url(10) \
        == r'https://udn.com/'
