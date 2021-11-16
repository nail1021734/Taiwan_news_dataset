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
    url = r'https://star.ettoday.net/news/2026310'
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
            台灣馬自達7月初宣布,為感謝國內醫護人員對於防疫工作的付出,將自7/3至7/31為止,
            推出名為「MAZDA挺你,醫起守護」活動;不限廠牌車主且同時具有醫護人員身份,
            台灣馬自達將免費提供機油更換、車室消毒、基礎車輛健檢、贈送原廠抗菌擦布等服務;
            當然活動看似「揪甘心」,執行實際狀況又是如何?這次《ETtoday車雲》就秉持著
            「謠言終結者」的求證精神,親身商借了一台符合資格的TOYOTA C-HR實際測試,
            看看台灣馬自達是否真的這麼「暖」。
            '''
        ),
    )
    assert parsed_news.category == '車'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1625792700
    assert parsed_news.reporter == '游鎧丞'
    assert parsed_news.title == 'TOYOTA神車也能到馬自達保養揪甘心 親身實測給你看'
    assert parsed_news.url_pattern == '2026310'
