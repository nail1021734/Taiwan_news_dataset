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
    url = r'https://star.ettoday.net/news/2096935'
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
            響應政府各類振興券齊發,奇美博物館同步推出回饋方案,凡來館使用五倍券或藝FUN券,
            可享「雙人看特展600元」、「禮品全面9折」的超值優惠。 奇美博物館表示,為了推廣藝文
            並配合政府振興經濟,館方以近期最受歡迎的特展《蒂姆.沃克:美妙事物》
            (Tim Walker: Wonderful Things)為回饋項目;《蒂姆.沃克:美妙事物》為英國V&A
            博物館的重量級世界巡迴展,展出時尚攝影大師蒂姆.沃克的奇幻之作,不但有沃克的職涯作品
            精華回顧、從V&A獲取靈感的全新創作,還有V&A稀珍藏品等一併登場;該展的展場設計更結合
            視覺與聽覺,打造魔幻多變的沉浸式體驗。為鼓勵民眾前來欣賞這場難得一見的國際級展覽,
            館方特別針對振興五倍券、藝FUN券祭出「雙人看特展」原價900元、特價600元,相當於
            6.7折的優惠,這也是該展開展至今最超值的回饋,歡迎民眾把握機會前來看展。 此外,遊客
            最喜愛的文創禮品、特展紀念品等也有振興折扣,凡持五倍券或藝FUN券於奇美博物館禮品店
            消費即享9折優惠(特價品除外)。相關振興券優惠無論數位或紙本券皆可使用,活動期效:
            五倍券自10/8起至明年2/6,藝FUN券自11/10起至明年2/6。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1633663080
    assert parsed_news.reporter == '林悅'
    assert parsed_news.title == '奇美博物館振興券優惠來了! 雙人看特展回饋價6.7折'
    assert parsed_news.url_pattern == '2096935'
