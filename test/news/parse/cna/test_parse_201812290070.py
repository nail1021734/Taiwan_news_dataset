r"""Positive case."""

import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201812290070.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            2018年印尼天災不斷,從觀光勝地龍目島兩次強震、蘇拉威西島強震引發海嘯,
            到巽他海峽海嘯,一次又一次地凸顯印尼在防災預警上的漏洞以及災後應變的不足。 印尼
            觀光勝地龍目島(Lombok)7月29日發生規模6.4淺層地震,這場地震造成17人死亡,
            500多名登山客受困在林賈尼火山(Rinjani)。緊接著在8月5日,龍目島又發生規模7地震,
            造成至少上百人死亡,摧毀上千棟建築。 龍目島經歷兩次強震,死亡人數共計達400人左右,
            也重創當地觀光業。 值得注意的是,龍目島強震過後,附近的旅遊熱區吉利群島也
            傳出災情。當地台商表示,災區已經不只是偷,自從地震停電開始,偷竊情況暴增之外,
            而且已有一段時間未聽到的搶劫也再次出現,軍警進駐後情況才獲得改善。 此外,
            印尼北部蘇拉威西島巴路市(Palu)9月底遭規模7.5強震襲擊,隨後引發海嘯,
            大量房屋遭摧毀。事後救災區發生170多次餘震,印尼政府花了數天才調動重型器具
            進行搜救。官方公布死亡人數逾2000人。 巴路市在災後也同樣出現劫掠情形。 記者在10月
            初深入巴路災區,棲身在庇難中心的民眾向記者表示,天災發生後,當地治安一度陷入混亂,
            商家被暴民劫掠一空,吃喝用的、能賣錢的東西,幾乎都被搶光,幾乎所有商家索性拉下鐵門
            暫停營業。 直到災後數日,大批荷槍實彈的軍警進駐後,治安才逐漸恢復。 一直到最近的
            巽他海峽因火山噴發引發海嘯,造成400多人罹難,接連的天災凸顯印尼海嘯預警系統
            完全失靈。 印尼科技評估與應用局(BPPT)的海嘯專家威喬(Widjo Kongko)日前分析,
            「巴路的潮汐監測站並未記錄到有關海嘯的資訊,因為它沒在運作。」 這座監測站持續檢查
            潮汐變化,理應偵測到是否有破壞性海浪朝巴路市襲來。規模7.5的主震發生後,印尼負責監測
            地震活動的氣象氣候暨地球物理局(BMKG)的確曾發布海嘯預警,但不久後就解除警報,因而
            被媒體質疑當地根本沒有海嘯測量儀器。 即使印尼全國的潮汐監測站均發揮作用,海嘯
            預警網絡的部署其實有限,不管在任何情況下,根本沒給民眾逃生時間,因為監測站只偵測
            接近海岸的浪潮。 印尼海嘯預警系統的開發機構—德國地球科學研究中心(GFZ)表示,
            蘇拉威西島的預警系統在「最後一里路」失敗,造成高達6公尺的海嘯令人
            措手不及。 印尼蘇門答臘島(Sumatra)2004年也曾遭遇強震引發大海嘯襲擊,
            共造成環印度洋地區22萬人喪生,其中大多在印尼。後來印尼在全國各地部署22套初期
            預警浮標系統,以偵測海嘯。 不過,印尼警報系統屢被指責未發揮效用。印尼國家災害應變
            總署發言人蘇托波(Sutopo Purwo Nugroho)近日表示,印尼的海嘯預警系統因人為破壞、
            預算不足及技術損壞等因素,自2012年起已不能正常運作。 災區民眾也感嘆,這些
            破壞海嘯預警設施的漁民或當地民眾,怎麼樣也不想到為了一己之私,卻造成日後生靈塗炭的
            悲慘後果,而當地政府卻坐視民眾肆意破壞海嘯預警浮標也不管。 印尼氣象氣候暨
            地球物理局(BMKG)指出,這次巽他海峽海嘯是由火山爆發引致,加上一個監測火山活動
            的機器損毀,造成一開始未能掌握準確數據,未能及時啟動發海嘯預警系統。 印尼總統
            佐科威已下令氣象氣候暨地球物理局購置新型地震及海嘯預警探測器,為民眾
            提供及時警報。 「天地不仁,以萬物為芻狗」,天災誠然非人力所能避免,但印尼政府部門
            及防災機構在災難預警的軟硬體建置、平日的防災教育訓練,乃至對破壞災難預警設施者的
            處罰,都還有許多努力改善的空間。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1546012800
    assert parsed_news.reporter == '周永捷雅加達'
    assert parsed_news.title == '2018年天災不斷 印尼政府防災應變漏洞大'
    assert parsed_news.url_pattern == '201812290070'
