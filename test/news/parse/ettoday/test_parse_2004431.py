import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ettoday


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='東森')
    url = r'https://star.ettoday.net/news/2004431'
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

    parsed_news = news.parse.ettoday.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            日本火腿隊王柏融連2次對阪神火球終結者蘇亞雷斯(Robert Suarez)都很有話題,
            10日從他手中敲安,讓阪神球迷嚇一跳。 王柏融8日9局下二出局一壘有人,面對蘇亞雷斯,
            共打了11球,只有投2球變化球都是壞球,其餘9球都是快速球,最慢158公里起跳,有4顆
            159公里、3顆160公里,王柏融最後將160公里的速球打成左外野小飛球出局,太平洋聯盟
            TV更將二人的纏鬥剪成精彩影片。 10日雙方再度對決,王柏融9局下碰上蘇亞雷斯,一出局
            二壘有人,鎖定第2球155公里速球,王柏融出棒打穿二、游中線安打,打進1分,中斷蘇亞雷斯
            連續24場無責失分紀錄。 蘇亞雷斯比賽前出賽26場僅失1分,被王柏融敲安後,防禦率從
            0.35上升至0.67,讓阪神球迷驚嘆,「王柏融專打各隊強投欸!」、「很久沒有看到
            蘇亞雷斯掉分了」,而今天交流賽由橫濱與日本火腿交手,阪神球迷提醒要注意王柏融,
            「勝利關鍵是大王」、「一定要注意他啊!」
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1623376320
    assert parsed_news.reporter == '賴冠文'
    assert parsed_news.title == '王柏融重擊終結者!震撼阪神球迷 還提醒橫濱球迷「注意大王」'
    assert parsed_news.url_pattern == '2004431'
