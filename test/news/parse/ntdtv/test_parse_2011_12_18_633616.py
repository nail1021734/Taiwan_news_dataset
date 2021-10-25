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
    url = r'https://www.ntdtv.com/b5/2011/12/18/a633616.html'
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
            法國是航海業很發達的國家,在全球經濟不穩定的情況下,其產量增長了11%,讓我們一起去
            今年的巴黎遊艇展看看法國最新款遊艇及明年的航海比賽計劃。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1324137600
    assert parsed_news.reporter is None
    assert parsed_news.title == '2011年巴黎遊艇展'
    assert parsed_news.url_pattern == '2011-12-18-633616'
