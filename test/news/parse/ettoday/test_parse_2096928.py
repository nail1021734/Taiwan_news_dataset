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
    url = r'https://star.ettoday.net/news/2096928'
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
            在經過偽裝車的預告釋出炒熱話題後,Triumph終於正式發表了旗下中量級冒險車款新作
            「TIGER SPORT 660」!由於引擎與車架基礎皆取自Trident 660,因此推測
            TIGER SPORT 660將會有相同的易操控性而廣受歡迎。 車重僅206kg的中量級冒險車款
            ! Triumph正式發表全新的中量級冒險車款TIGER SPORT 660,它是600c.c.級距冒險
            風格中,首款搭載並列三缸引擎的車款,81ps最大馬力與6.53kg的最大扭力,在同級距車款中
            可是名列前茅。 這具並列三缸引擎不管是缸徑、行程還是性能等數據,皆與有著新古典風格
            的街車車款Trident 660相同,並採用輔助滑動式離合器來減輕操作壓力,而車架雖然也是以
            Trident 660為基礎,但有考慮到冒險風格與用途進行改良,軸距也從1,400mm小幅增加到
            1,418mm。 為了迎合更多消費者,TIGER SPORT 660的座墊高度被控制在不算高的835mm
            ,整備重量也僅只有206kg,容量擴大到17.2L的油箱,在WMTC模式測試下的油耗達4.5L/
            100km=22.22km/L,推估單次續航里程超過380km。 作為全新車款,TIGER SPORT 660
            當然配備LED頭燈、定位燈及尾燈,就連方向燈也是LED燈組;至於做為冒險車款不可或缺的
            風鏡自然也是標準配備,且能透過手動調整高度。 底盤結構部分,TIGER SPORT 660前後
            懸吊皆採用SHOWA製避震器,前方為φ41mm倒立式前叉、後面則是帶有預載可調的中置單槍
            避震器,前後懸吊行程皆為150mm。 至於煞車系統則似乎與Trident 660的規格相同,皆為
            前φ310mm雙固定碟盤+單向雙活塞卡鉗,搭配後φ255mm固定碟盤+單活塞卡鉗輔以ABS系統
            的配置,制動性能絕對算不上出眾,但也可說是中規中矩。 TIGER SPORT 660標準配備可
            與APP「My Triumph」連接的TFT彩色多功能儀表板,可實現在儀表查看導航、連接智慧型
            手機、操作GoPro等功能。 電控系統除了ABS以外,TIGER SPORT 660還有ROAD/RAIN兩
            種騎乘模式可調、根據路面狀況切換油門反應以及循跡控制系統。 2022年式
            TIGER SPORT 660共推出LUCERNE BLUE/SAPPHIRE BLACK(琉森藍/藍寶石黑)、
            KOROSI RED/GRAPHITE(科羅西紅/石墨黑)以及GRAPHITE/SAPPHIRE BLACK
            (石墨黑/藍寶石黑)等三色車身塗裝,在日本的建議售價為1,125,000日圓
            (折合新台幣約28.6萬),預計會在2022年開始推出販售。
            '''
        ),
    )
    assert parsed_news.category == '車'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634050560
    assert parsed_news.reporter is None
    assert parsed_news.title == '凱旋「入門版重機」30萬有找!坐擁兩大特性 同級車裡名列前茅'
    assert parsed_news.url_pattern == '2096928'
