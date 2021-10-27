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
    url = r'https://www.cna.com.tw/news/aipl/201411080177.aspx'
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
            天候愈見涼爽,黑琵大舉抵台。台南市生態保育學會最新調查,台南黑琵已達1602隻,較去年
            同期多出700隻。
            '''
        ),
    )
    assert parsed_news.category == '社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1415376000
    assert parsed_news.reporter == '張榮祥台南'
    assert parsed_news.title == '黑琵大舉抵台 台南1602隻'
    assert parsed_news.url_pattern == '201411080177'
