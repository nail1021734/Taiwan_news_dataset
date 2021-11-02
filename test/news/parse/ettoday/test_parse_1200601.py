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
    url = r'https://star.ettoday.net/news/1200601'
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
            日本後衛還潛藏一名碰撞硬派植田直通,為了能在場上做出100%的
            表現他一直將自身狀態調整至最好,期待這次俄羅斯世界盃中他能夠出場展露頭角。 23歲
            的植田直通效力於鹿島鹿角,186公分體能絕佳,善於碰撞、不怕見血的硬漢個性,讓他十分
            期待自己能有上場拼輸贏的機會;「一對一的局面,是我的強項」充滿自信的他,每場都做好
            了萬全準備要上場,甚至塞內加爾戰前有不少人猜測是否會換上他來封鎖對方進攻,可惜西
            野朗教練最後仍不動後衛名單,讓這名小將又再次希望落空。 照理來說年輕又有體型優勢
            的他,是該有機會上場對抗,不過似乎成也年紀敗也年紀,在2016年里約奧運時,以代表日本
            國奧隊出賽,植田直通曾在門前發生漏球險失分的驚險瞬間,還有與烏克蘭友誼賽發生烏龍
            球情況讓日本1:2落敗的不良紀錄,無法掌控與不純熟的經驗似乎讓西野教練無法大膽做出
            替換決策。 日本小組最後一戰面對波蘭,仍未確定晉級的日本,也勢必要在比賽中取勝,植
            田直通也許還有機會上場。
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530092820
    assert parsed_news.reporter == 'Left-Emmy'
    assert parsed_news.title == '做好100%準備就等教練 23歲小將好想上場'
    assert parsed_news.url_pattern == '1200601'
