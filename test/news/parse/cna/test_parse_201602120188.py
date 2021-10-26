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
    url = r'https://www.cna.com.tw/news/aipl/201602120188.aspx'
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
            中華職棒Lamigo桃猿隊赴日本石垣島與羅德隊交流比賽,現場有攤位為台南地震募款
            ,桃猿副領隊浦韋青說,日方希望這樣的舉動能帶給災民勇氣。
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1455206400
    assert parsed_news.reporter == "林宏翰石垣市"
    assert parsed_news.title == '日職羅德為台灣地震募款 盼給災民勇氣'
    assert parsed_news.url_pattern == '201602120188'
