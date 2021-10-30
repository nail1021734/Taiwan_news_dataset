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
    url = r'https://star.ettoday.net/news/1200254'
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
            期待已久的苗栗舊山線「軌道自行車」將在7月1日試運轉,僅開放在地鄉親搶先試乘,預計8
            月中旬開始正式對外試營運,鐵路自行車Rail Bike是一項從韓國紅起來的人力小火車,苗栗
            山城擁有許多舊鐵道、老隧道與山巒美景,坐在小火車上可以將龍騰斷橋、內社川橋及舊山
            線連續隧道群美景一網打盡。 軌道自行車從勝興車站穿越2號隧道,串接8個隧道結合三義
            130沿線週邊景點,路線為路線為勝興車站→2號隧道→魚藤坪橋→6號隧道北口折返,來回往返約
            12公里,每趟大約需耗費1.5小時,兩車間距必須超過5公尺,除人力踩踏也有附設電動設備,
            不怕累了騎不動,另外還有衛星定位系統告訴遊客身在哪裡。 鐵路自行車為高爾夫球車、
            小火車與自行車功能,一台最多可乘坐4人全程須戴安全帽、繫安全帶,全車禁菸也不能中途
            停車及下車,日前Rail Bike還在測試當中終於要正式與大家見面了,預計今年暑假7至9月會
            先開放40輛、10月至年底開放至60輛,最終會增加到100輛,預計8月中旬正式通車,軌道自行
            車票價每人新台幣280元,孕婦、高血壓、未滿6歲孩童、飲酒後皆不能搭乘。
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530077160
    assert parsed_news.reporter == '陳涵茵'
    assert parsed_news.title == '苗栗鐵道自行車7月1日試運轉!隧道路線、票價搶先看'
    assert parsed_news.url_pattern == '1200254'
