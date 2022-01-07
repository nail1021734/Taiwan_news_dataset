import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ettoday


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='東森')
    url = r'https://star.ettoday.net/news/1200592'
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

    parsed_news = news.parse.ettoday.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            今年北京車展時, Nissan 中國大陸合資夥伴東風日產推出了 SYLPHY (即 Sentra) 車系
            的純電動版本 SYLPHY Zero Emission,近日東風日產宣布正式開始接單,經政
            府補貼後售價 16.6 萬人民幣起(約合新台幣 76.7 萬元)。 SYLPHY Zero Emission 是首
            款 Nissan 針對中國市場量身訂作的純電動量產車,採用與全球純電動車銷售冠軍相同的平
            台設計,提供中國消費者潔淨而舒適的用車體驗。 動力配置
            上, SYLPHY 搭載 TZ200XS5UR 型電動馬達,可輸出 109 匹最大馬力及 254Nm 峰值
            扭力,電池方面為採用薄型輕量化設計的高能量密度三元鋰電池,最大續航力
            為 338 公里。 Nissan 也在 SYLPHY Zero Emission 上
            導入 Intelligent Mobility Technology 智行科技,包括 IEB 智慧型緊急煞車、行人
            偵測以及盲點偵測皆列入配備清單,也支援智慧型手機連接,更享有 NissanConnect 車聯網
            機能。
            '''
        ),
    )
    assert parsed_news.category == '車'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530172980
    assert parsed_news.reporter == '7car'
    assert parsed_news.title == 'Nissan Sentra電動車開始接單!補貼價76.7萬大陸獨享'
    assert parsed_news.url_pattern == '1200592'
