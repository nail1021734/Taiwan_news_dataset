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
    url = r'https://star.ettoday.net/news/2031751'
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
            本特輯除了介紹車輛本身的基本規格配備外,也將透過影片比較各車款的特徵、在迷你賽道
            上的騎乘感及試乘狀況等,為大家送上試乘報告;這次要為大家送上的是「入門級距街車車款
            」,進行試乘比較的是YAMAHA MT-25和HONDA CB250R。 1 MT-25/CB250R在車架及
            底盤結構等皆分別與MT-03/CB300R幾乎相同,僅引擎排氣量有所差異以符合日本的分級
            制度。 試乘車輛1 YAMAHA MT-25 MT-25是專為日本推出的車款 (其他地區皆為排氣量
            稍大的MT-03),同時也被視為全罩式運動車款YZF-R25的街車版本,搭載排氣量249cc的
            水冷式四行程DOHC 4汽門並列雙缸引擎,最早問世於2015年。 MT-25/MT-03在去年
            (2020)進行大改款,不僅採用倒立式前叉、LED頭燈、危險警示燈,車頭造型也進行大改造,
            但被暱稱為”口球”的頭燈造型喜好因人而異,並在推出改款後,舊款MT-25的中古售價也更
            平易近人。 試乘車輛2 HONDA CB250R 現行款CB250R最早於2018年5月發表推出,搭載
            的249cc水冷式四行程DOHC 4汽門單缸引擎繼承自CB250F,是一款有著強大扭力的單缸
            街車。 雖然引擎沿用自CB250F,但CB250R的原廠配胎為子午線輪胎、前叉也採用
            倒立式結構等,在規格配備上有所改良,甫推出時還有標配ABS與無ABS等兩種版本,但在
            2019年式改款後全部標配ABS,並改良了後懸吊結構,不僅讓座墊高度下降5mm、操控感也
            更加優化。 至於最早於2017年與CB1000R首次在米蘭車展亮相的CB300R,歷經數年的販售
            後,在車身結構與配備上皆無改動。
            '''
        ),
    )
    assert parsed_news.category == '車'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1626361500
    assert parsed_news.reporter is None
    assert parsed_news.title == '中古「入門黃牌重機」怎麼挑?喜歡強大扭力單缸街車就選它'
    assert parsed_news.url_pattern == '2031751'
