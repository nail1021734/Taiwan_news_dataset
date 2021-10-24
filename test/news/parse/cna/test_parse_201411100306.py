import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201411100306.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            陳姓男子日前涉毒遭逮,向檢警哀求他將結婚,婚宴不能沒新郎,檢方諭令限制住居。沒想到
            他開車南下又攜毒被逮,警將他送辦。
            '''
        ),
    )
    assert parsed_news.category == '社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1415548800
    assert parsed_news.reporter == '陳淑芬台中'
    assert parsed_news.title == '毒蟲以結婚求釋放 攜毒再被逮'
    assert parsed_news.url_pattern == '201411100306'
