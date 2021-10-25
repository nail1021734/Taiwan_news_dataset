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
    url = r'https://www.cna.com.tw/news/aipl/201810030025.aspx'
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
            粵深港高鐵已於9月23日投入服務,有人說,連同預定稍後通車的港珠澳大橋,粵港澳大灣區
            規畫已經有了必須的交通基礎,下一步就看具體推動內容。
            '''
        ),
    )
    assert parsed_news.category == '兩岸'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1538496000
    assert parsed_news.reporter is None
    assert parsed_news.title == '粵深港高鐵通車 落實大灣區理念'
    assert parsed_news.url_pattern == '201810030025'
