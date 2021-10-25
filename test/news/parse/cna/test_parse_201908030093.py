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
    url = r'https://www.cna.com.tw/news/aipl/201908030093.aspx'
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
            基隆一名女飼主日前將柴犬「浩呆」綁在頂樓,由於當時天氣炎熱,氣溫高達攝氏35度,
            柴犬不斷伸舌頭散熱,動保所接獲檢舉到場稽查,依法開罰新台幣6000元。
            '''
        ),
    )
    assert parsed_news.category == '社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1564761600
    assert parsed_news.reporter == '王朝鈺基隆市'
    assert parsed_news.title == '35度高溫柴犬綁頂樓 飼主遭罰6千'
    assert parsed_news.url_pattern == '201908030093'
