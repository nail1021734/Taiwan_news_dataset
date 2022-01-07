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
    url = r'https://www.epochtimes.com/b5/13/8/12/n3938760.htm'
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
            澳大利亞悉尼一年一度的「市區至海濱」馬拉松長跑在8月11日舉行,今年有9萬人參加了
            這個世界最大的趣味賽跑,每一個參加長跑的市民會佩帶參加賽跑標號,筆者看到參加的人數
            已經超過9萬號,比去年的8萬5千還要多出5千多人。今日的悉尼陽光燦爛,參加長跑的市民
            有各族裔的人、有老人、孩子、學生、推幼兒車的父母、揹負行軍包的軍人、藝人和高級
            政府官員,人們穿著夏日的運動衣,還有身著化裝馬戲的服飾,像是度過一個盛大的
            體育節日,人們從跑起到後來徒步走,經過了城市市區到海邊,里程7到14公里不等,這是世界
            最大的馬拉松長跑運動。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1376236800
    assert parsed_news.reporter is None
    assert parsed_news.title == '世界之最悉尼9萬人城市馬拉松 2'
    assert parsed_news.url_pattern == '13-8-12-3938760'
