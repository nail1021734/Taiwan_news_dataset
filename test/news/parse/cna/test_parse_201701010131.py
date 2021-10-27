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
    url = r'https://www.cna.com.tw/news/aipl/201701010131.aspx'
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
            機場捷運去年底完成履勘,預計農曆年前後可通車。桃園大眾捷運公司今天發表首支機捷VR版
            的車頭攝影,在滅火器樂團的歌聲中,帶民眾欣賞沿線風光。 桃捷第一支VR版的車頭攝影
            ,配著滅火器樂團活力十足的音樂節奏,可以看到360度的全景,帶民眾用眼睛和科技「坐上
            駕駛座」,欣賞機捷沿線風光。 機捷全線長約51.03公里,有許多高架路段,一路可以看到
            青翠的樹林小丘、埤塘、工業聚落和現代的商場outlet,及經常歡聲雷動的棒球場。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1483200000
    assert parsed_news.reporter == '汪淑芬台北'
    assert parsed_news.title == '機捷首支VR影片 滅火器歌聲中賞風光'
    assert parsed_news.url_pattern == '201701010131'
