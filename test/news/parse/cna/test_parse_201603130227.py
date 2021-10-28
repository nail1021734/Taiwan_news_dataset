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
    url = r'https://www.cna.com.tw/news/aipl/201603130227.aspx'
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
            中國大陸雲南九河鄉龍應村由於地處偏遠,村民多出外打工
            ,壯年人口嚴重外移,村裡兒童及老人比例極高,長時間看不到自己爸媽的兒童,在
            幼兒發展期間衍生的問題比比皆是。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1457798400
    assert parsed_news.reporter == "吳欣紜台北"
    assert parsed_news.title == '留守兒童問題多 角落教學滿足需求'
    assert parsed_news.url_pattern == '201603130227'
