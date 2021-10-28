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
    url = r'https://www.epochtimes.com/b5/13/1/15/n3777183.htm'
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
            1月15日自由門7.38版增強突破封鎖能力。歡迎大家繼續反饋。 如果不能使用,請上傳反饋
            信息。謝謝。 然
            '''
        ),
    )
    assert parsed_news.category == '科技新聞,IT 動向'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1358179200
    assert parsed_news.reporter is None
    assert parsed_news.title == '翻牆自由門發布最新7.38版'
    assert parsed_news.url_pattern == '13-1-15-3777183'
