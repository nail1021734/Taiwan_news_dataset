import news.crawlers.util.normalize


def test_compress_url() -> None:
    r"""Must remove url prefix."""
    assert news.crawlers.util.normalize.compress_url(
        company_id=0,
        url=r'https://www.chinatimes.com/realtimenews/20211012000001-260407',
    ) == r'r-20211012000001-260407'
    assert news.crawlers.util.normalize.compress_url(
        company_id=0,
        url=r'https://www.chinatimes.com/newspapers/20211012000001-260407',
    ) == r'n-20211012000001-260407'
    assert news.crawlers.util.normalize.compress_url(
        company_id=1,
        url=r'https://www.cna.com.tw/news/aipl/202110120001.aspx',
    ) == r'202110120001'
    assert news.crawlers.util.normalize.compress_url(
        company_id=2,
        url=r'https://www.epochtimes.com/b5/21/10/12/n00000001.htm',
    ) == r'21-10-12-00000001'
    assert news.crawlers.util.normalize.compress_url(
        company_id=3,
        url=r'https://star.ettoday.net/news/1',
    ) == r'1'
    assert news.crawlers.util.normalize.compress_url(
        company_id=4,
        url=r'https://www.ftvnews.com.tw/news/detail/2021A12W0001',
    ) == r'2021A12W0001'
    assert news.crawlers.util.normalize.compress_url(
        company_id=5,
        url=r'https://news.ltn.com.tw/news/life/breakingnews/0000001',
    ) == r'life-0000001'
    assert news.crawlers.util.normalize.compress_url(
        company_id=6,
        url=r'https://www.ntdtv.com/b5/2021/10/12/a000000001.html',
    ) == r'2021-10-12-000000001'
    assert news.crawlers.util.normalize.compress_url(
        company_id=7,
        url=r'https://www.setn.com/News.aspx?NewsID=1',
    ) == r'1'
    assert news.crawlers.util.normalize.compress_url(
        company_id=8,
        url=r'https://www.storm.mg/article/1?mode=whole',
    ) == r'1'
    assert news.crawlers.util.normalize.compress_url(
        company_id=9,
        url=r'https://news.tvbs.com.tw/entertainment/0000001',
    ) == r'entertainment-0000001'
    assert news.crawlers.util.normalize.compress_url(
        company_id=10,
        url=r'https://udn.com/news/story/122496/0000001',
    ) == r'122496-0000001'
