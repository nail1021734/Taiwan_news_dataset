import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/04/08/a516206.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            強烈的餘震重擊日本東北部之後,宮城縣女川核電廠的反應爐廢燃料池出現漏水,引起短暫的
            恐慌。 日本原子能安全保安院(Nuclear and Industrial Safety Agency)出面
            澄清情況。 副主任西山英彥(Hidehiko Nishiyama):「根據女川傳來的最新消息,餘震
            發生後,2號和3號反應爐附近出現反常的現象。關於2號反應爐,我們已經確定是回收燃料池
            的搖晃造成水灑在地板上。」 女川核能發電廠(Onagawa)的營運公司東北電力說,強震過後,
            核電廠出現漏水情況,但廠外輻射值沒有改變。 地震曾造成冷卻系統關閉,現在已經重新
            啟動。 餘震造成日本東北地區很大範圍電力中斷。日本政府呼籲企業和家庭節約用電,以
            避免限制用電。 日本內閣官房長官枝野幸男(Yukio Edano):「我們希望避免計劃停電。
            計劃停電會對公民生活和經濟帶來巨大的影響,所以我們希望能在不依靠計劃停電的情況下,
            平衡好電力的供應和需求。我們計劃在這個月內找出電力供應的替代方案。」 一名購物的
            民眾表示:「電也停了、水也停了,所以我來買一些不用煮就能吃的食物。」 奧州市
            (Oshu City)的員工在商店外面搭建臨時的架子販售食物和飲料。 強震和海嘯重擊日本
            不到一個月內,7.4級的餘震中至少4人死亡。 日本宮城縣再次發生強烈地震,據日本放送
            協會(NHK)報導,目前至少造成四人死亡,140多人受傷。日本女川核能發電廠(Onagawa)
            的營運公司說,今天凌晨強震過後,核電廠出現漏水情況,但廠外輻射值沒有改變。表明漏水
            量不大。目前還沒有輻射水平的具體資料。 負責營運的公司說,第1及第2核子反應爐的廢料
            槽及電廠其他地方都出現漏水情況。 此外,經濟產業大臣海江田萬里說,日本將尋求減少企業
            與家用電力使用,以避免限電。他說,基本上,受到311地震影響最嚴重的東京電力公司與
            東北電力公司不會實施輪流停電。 經濟產業省說,政府希望仰賴這兩家公司的大用戶能夠在
            夏季尖峰時間將用電量減少25%。 小型工業用戶減少20%,家用電則希望每戶減少15至20的
            用電量。 據美國地質局(USGS)網站稱,星期四,日本東北部發生裡氏7.4級地震,隨即宣佈
            海嘯預警。不過90分鐘以後預警被取消。地震發生在當地時間23點32分,震中距離仙台市
            東部98公里、東京東北部345公里處。震源距離在地下40公里處。 这次地震是東日本
            大地震發生以來最強烈的一次餘震。當局最初報告強度為裡氏7.4級,後來下調至
            7.1級。 據家住在仙台市太白區的一位男性白領描述,餘震發生時,突然整個房子在上下顫抖,
            緊接著開始左右搖擺將近20秒鐘。他說:「由於家住在17層的公寓,餘震來時臥室的電視開始
            猛烈左右搖擺,櫥櫃也倒了,部分碗和盤子都摔的粉碎。」 據該男子介紹說,餘震發生後,
            仙台市大街上到處都是警笛聲,緊接著看到大量警察上街維持秩序。手機一時間也無法正常
            使用,很多人都紛紛跑出家門,多數民眾家裡的燈仍然是開著的,但人都聚集到了樓下。 他
            還說:「這種情景讓我感覺到,好像有回到了3月11日當天。」 據日本當局星期五公佈,截至
            星期五早上為止,3月11日大地震的死亡人數為12731人,14706人仍然失蹤。
            '''
        ),
    )
    assert parsed_news.category == '天災人禍,各國地震,日本地震'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1302192000
    assert parsed_news.reporter == '史考特'
    assert parsed_news.title == '日強震致四死 女川核電廠廢料槽少量漏水'
    assert parsed_news.url_pattern == '2011-04-08-516206'
