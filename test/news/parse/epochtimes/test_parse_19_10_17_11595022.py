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
    url = r'https://www.epochtimes.com/b5/19/10/17/n11595022.htm'
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
            這個故事的每一細節都是真實的,逼真還原了中國北京的看守所、北京新安女子勞教所、北京
            女子監獄的場景及發生的事件,只是掩去了人物的真實姓名。 六、新女監
            '''
        ),
    )
    assert parsed_news.category == '文化網,藝海漫遊,美術長廊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1571241600
    assert parsed_news.reporter is None
    assert parsed_news.title == '連環畫:走過劫難'
    assert parsed_news.url_pattern == '19-10-17-11595022'
