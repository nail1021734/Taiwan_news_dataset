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
    url = r'https://www.epochtimes.com/b5/19/12/27/n11750208.htm'
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
            台灣2020大選倒數兩週,中共動作加大,美國也在加戲。美中在台灣戰場持續角力,2020關鍵
            戰役將攸關未來。本期《走向2020 新聞大破解》將為觀眾解析: 1. 防紅色滲透!美國2020
            保台抗共捍衛戰 2. 中共武統論調再現 戰力不足只是政治恫嚇? 3. 反滲透法照妖鏡!
            本會期過不過是關鍵
            '''
        ),
    )
    assert parsed_news.category == '台灣'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577376000
    assert parsed_news.reporter is None
    assert parsed_news.title == '美中角力台灣 2020攸關未來'
    assert parsed_news.url_pattern == '19-12-27-11750208'
