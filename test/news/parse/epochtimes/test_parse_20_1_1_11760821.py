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
    url = r'https://www.epochtimes.com/b5/20/1/1/n11760821.htm'
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
            冬來陰霾促 襲寒虐枝倏 帔玉逐光綻 玲瓏鶴影出 不問今何年 芳韻煉丹爐 亂世難擾心 絕
            塵綻華殊
            '''
        ),
    )
    assert parsed_news.category == '文化網,文學世界,詩詞歌曲,古體詩詞創作'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577808000
    assert parsed_news.reporter is None
    assert parsed_news.title == '天雪:臘梅迎新年'
    assert parsed_news.url_pattern == '20-1-1-11760821'
