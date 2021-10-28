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
    url = r'https://www.epochtimes.com/b5/14/1/1/n4048433.htm'
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
            在2014年新年來臨之際,日本東京的標誌性建築物的東京塔周圍擠滿了迎接新年瞬間的
            人群,隨著齊聲的倒計數,當2014年點亮的瞬間,興奮的人群齊聲歡呼、跳躍,相互祝福
            新年。 對於日本來說,迎接新年的最大的活動還是到寺院和神社去參拜。這是一項傳統性的
            全民活動,日語的漢字叫做「初詣」(HATUMODE)。到寺院和神社去祈求上天在新的一年中
            給予健康、事業、學業有成。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388505600
    assert parsed_news.reporter == '遊沛然日本東京'
    assert parsed_news.title == '日本民眾新年參拜祈福求勝運'
    assert parsed_news.url_pattern == '14-1-1-4048433'
