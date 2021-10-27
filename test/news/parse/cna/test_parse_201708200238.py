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
    url = r'https://www.cna.com.tw/news/aipl/201708200238.aspx'
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
            今年第13號颱風天鴿今天形成,中央氣象局晚間11時30分發布天鴿颱風海上颱風警報
            。 根據中央氣象局觀測,天鴿颱風目前中心位置在鵝鑾鼻東南東方約570公里的海面上
            ,以每小時16公里向西轉西北西前進。暴風圈對台灣東南部海面及巴士海峽構成威脅
            。 21日下午起,台灣東半部、恆春半島及西南部沿海地區有長浪,氣象局提醒民眾,前往
            海邊活動須注意安全。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1503158400
    assert parsed_news.reporter == "陳葦庭台北"
    assert parsed_news.title == '颱風天鴿海警 晚間11時30分發布'
    assert parsed_news.url_pattern == '201708200238'
