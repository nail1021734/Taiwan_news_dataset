import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201801010009.aspx'
    response = news.crawlers.util.request_url.get(url=url)

    raw_news = news.crawlers.db.schema.RawNews(
        company_id=company_id,
        raw_xml=news.crawlers.util.normalize.compress_raw_xml(
            raw_xml=response.text,
        ),
        url_pattern=news.crawlers.util.normalize.compress_url(
            company_id=company_id,
            url=url,
        )
    )

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            美國科羅拉多州丹佛市郊今天上午驚傳槍擊案,截至目前不知有多少警察遭槍擊,道格拉斯郡
            警方特種武器和戰術部隊(SWAT)一組人已經趕到現場。 「丹佛郵報」(Denver Post)
            報導,副警長布朗查德(Jason Blanchard)針對這起發生在高原牧場(Highlands Ranch)
            銅峽谷公寓大樓(Copper Canyon Apartments)的事件表示,「有多名警察遭槍擊」、
            「此刻我們還不公布數字和現場情況。我們還在努力要將嫌犯緝拿到案」。 當局要求居民
            待在家中,避免接近窗戶和外牆。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1514736000
    assert parsed_news.reporter == '丹佛'
    assert parsed_news.title == '美國丹佛驚傳槍擊 多名警察中槍'
    assert parsed_news.url_pattern == '201801010009'
