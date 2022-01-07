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
    url = r'https://www.epochtimes.com/b5/12/6/25/n3620245.htm'
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
            美國政府的一項研究指出,美國東岸一段長將近一千公里的海岸線,海平面上升的速度
            ,是全世界最快的,範圍從北卡羅萊納(哈特拉斯角)到波士頓北邊。 美國地質研究所
            形容,那段長965公里的海岸線,是全球暖化導致海平面上升的熱點,上升的趨勢,從
            1990年開始,上升幅度是全球平均的三到四倍。 過去22年,維吉尼亞諾福克的海平面
            ,上升了13公分,費城沿海升高10公分,紐約升高8公分,同一期間,全球海平面平均上升
            了5公分。 這項研究刊登在昨天出刊的(自然氣候變遷)期刊上。
            '''
        ),
    )
    assert parsed_news.category == '科技新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1340553600
    assert parsed_news.reporter == None
    assert parsed_news.title == '美國東岸某段海平面上升速度全球最快'
    assert parsed_news.url_pattern == '12-6-25-3620245'
