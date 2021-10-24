r"""Positive case."""

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
    url = r'https://www.cna.com.tw/news/aipl/201812300114.aspx'
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
            元旦連假第二天,交通部高公局交通管理組科長莊國欽今天表示,今天國道車流量比原本
            預期多,傍晚東西部國道都有多路段塞車,預估晚間8時到9時之間才會紓解。 莊國欽說,
            今天雖然是連續假期第二天,但午後就出現明顯北返車潮,推測是和明、後2天的天氣不佳,
            民眾選擇提前北返有關,截至傍晚6時,國1北上西螺至埔鹽系統、銅鑼至頭份、新竹系統
            至湖口、國1南下三義至台中系統、國3北上竹山至中興、關西至樹林,國6西向東草屯至霧峰
            系統,以及國5北上宜蘭至坪林路段仍持續壅塞,預估要到晚間8時至9時才會紓解。 他提醒,
            明天是元旦連假第三天,預估午後北上車流將增加,車多路段將出現
            在國1北上西螺至埔鹽系統、南屯至后里、新竹系統至竹北、國3北上霧峰系統
            至霧峰、竹山至中興、大山至香山、關西至大溪、國5北上頭城至坪林、
            國6西向舊正至霧峰系統等路段,提醒民眾避開尖峰時段,或改走替代道路。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1546099200
    assert parsed_news.reporter == '陳葦庭台北'
    assert parsed_news.title == '元旦連假第3天午後北上車流增 9路段最易塞'
    assert parsed_news.url_pattern == '201812300114'
