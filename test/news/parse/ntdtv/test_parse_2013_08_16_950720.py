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
    url = r'https://www.ntdtv.com/b5/2013/08/16/a950720.html'
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
            保加利亞一名女童,日前經過6小時飛行後,累到完全走不動,直接趴在行李箱上呼呼大睡,
            父親只好將她一起與旅行箱拖著走,吸引了路過旅客們的目光。視頻上傳YouTube後,網友
            大讚模樣超萌
            '''
        ),
    )
    assert parsed_news.category == '奇聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1376582400
    assert parsed_news.reporter is None
    assert parsed_news.title == '女童睡趴行李箱 老爸一路拖著走'
    assert parsed_news.url_pattern == '2013-08-16-950720'
