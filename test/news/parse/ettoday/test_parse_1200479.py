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
    url = r'https://star.ettoday.net/news/1200479'
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
            六月到了,炎夏的熱情強力來襲,說走就走的夏日冒險,你是否準備好給2018上半年,畫一個
            完美的句點了呢?
            '''
        ),
    )
    assert parsed_news.category == '運勢'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530091800
    assert parsed_news.reporter == '靈機文化'
    assert parsed_news.title == '0628好星運開關│金牛開好運,為天蠍打打氣'
    assert parsed_news.url_pattern == '1200479'
