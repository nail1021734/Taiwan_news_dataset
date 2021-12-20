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
    url = r'https://www.epochtimes.com/b5/19/12/27/n11748178.htm'
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
            新唐人電視台特別企劃《2020跨年繽紛夜》直播節目,在2019年的最後一個夜晚,12月31日
            (週二),陪您盤點年度大事件,歡歡喜喜迎新年。大紀元網站將進行網絡直播, 直播預告影片
            : 玩遍各國跨年景點 讓您目不轉睛 廚藝隨堂考 當家主播能否成為
            好廚娘 西遊慶新年 恭喜發財錢幣史 網紅齊聚秀才藝 新年第一夜 品嚐醫聖神奇的禦寒
            妙方 各國煙火跨國接力 一起倒數迎接2020新時代 新唐人電視台將在美東頻道、美中頻道
            、美西頻道、歐洲頻道、大陸頻道播出。
            '''
        ),
    )
    assert parsed_news.category == '北美新聞,美國華人'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577376000
    assert parsed_news.reporter is None
    assert parsed_news.title == '新唐人電視台2020跨年繽紛夜'
    assert parsed_news.url_pattern == '19-12-27-11748178'
