import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2013/03/27/a870104.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            由於北京遭遇重度污染的霧霾天,大部份地方處於重度污染之上,不過,面對北京嚴重的
            空氣污染問題,近日老外發明了空氣過濾單車“會呼吸的自行車”來抵抗北京空氣污染
            。 3月26日,北京,英國藝術家麥特-霍普騎著他自製的“會呼吸的自行車”行進在
            東三環央視新台址附近。 麥特-霍普2007年移居到北京,從事藝術創作,近年來不時惡化
            的空氣質量,讓他萌發製造一輛帶有空氣濾化功用的自行車。 這輛名為“會呼吸的自行車”
            ,將一個廢棄的宜家渣滓桶裝置在後座,經過輪式動力發電機和過濾系統連結到
            戰役機飛行員呼吸面具和摩托車頭盔上,當踩動踏板時,發電機開端發電供給過濾器,
            過濾器發作正電荷除去灰塵,帶負電荷的金屬就吸住霧霾中的微粒。 霍普說,“除了自行車
            是買的,其他的造價十分低,都是用藝術工作室的廢棄’渣滓’組裝而成的。 霍普佩帶著
            飛行員呼吸面具和摩托車頭盔。
            '''
        ),
    )
    assert parsed_news.category == '大陸,社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1364313600
    assert parsed_news.reporter is None
    assert parsed_news.title == '高清:老外自製空氣過濾單車應對北京污染'
    assert parsed_news.url_pattern == '2013-03-27-870104'
