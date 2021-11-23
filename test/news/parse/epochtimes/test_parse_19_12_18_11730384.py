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
    url = r'https://www.epochtimes.com/b5/19/12/18/n11730384.htm'
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
            中華民國2020總統大選首場電視政見發表會今(18日)晚7時在華視登場,三組候選人包括總統
            蔡英文、國民黨候選人韓國瑜、親民黨候選人宋楚瑜,首度同台講述政見。新唐人電視台和
            大紀元將進行網絡直播,
            '''
        ),
    )
    assert parsed_news.category == '台灣'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576598400
    assert parsed_news.reporter is None
    assert parsed_news.title == '台灣總統選舉 首場電視政見會'
    assert parsed_news.url_pattern == '19-12-18-11730384'
