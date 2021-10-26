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
    url = r'https://www.cna.com.tw/news/aipl/201808210054.aspx'
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
            美食-KY旗下85度C遭兩岸議題波及,董事長吳政學受訪時說,大陸業績下滑約10%,不過,
            美食-KY取消原定今天召開的業績發表會,股價在平盤附近震盪,力守244元,仍保有
            觀光股王地位。
            '''
        ),
    )
    assert parsed_news.category == '產經'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1534780800
    assert parsed_news.reporter == '江明晏台北'
    assert parsed_news.title == '85度C董座喊話 美食-KY早盤震盪'
    assert parsed_news.url_pattern == '201808210054'
