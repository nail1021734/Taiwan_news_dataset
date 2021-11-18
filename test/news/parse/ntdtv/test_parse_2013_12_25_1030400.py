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
    url = r'https://www.ntdtv.com/b5/2013/12/25/a1030400.html'
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
            12月24日每日新鮮數 704 今年聖誕假期期間平均每位美國民眾購買禮物的金額預估為
            704美元
            '''
        ),
    )
    assert parsed_news.category == '美國'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1387900800
    assert parsed_news.reporter is None
    assert parsed_news.title == '12月24日每日新鮮數'
    assert parsed_news.url_pattern == '2013-12-25-1030400'
