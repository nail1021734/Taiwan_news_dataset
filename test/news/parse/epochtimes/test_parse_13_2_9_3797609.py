import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/13/2/9/n3797609.htm'
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

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            成湯王決定犧牲自己的生命去求雨,那麼上蒼真的要一個人的生命才下雨嗎?請聽故事:
            成湯王求雨(下)。
            '''
        ),
    )
    assert parsed_news.category == '文化網,教育園地,故事點播'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1360339200
    assert parsed_news.reporter is None
    assert parsed_news.title == '有聲故事:成湯王求雨'
    assert parsed_news.url_pattern == '13-2-9-3797609'
