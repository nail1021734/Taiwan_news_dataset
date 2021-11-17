import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.storm


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='風傳媒')
    url = r'https://www.storm.mg/article/601348?mode=whole'
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

    parsed_news = news.parse.storm.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            近年來,跑步成為日漸受歡迎的運動選項,從路跑活動的層出不窮便能深刻感受到;但時常跑步
            就等於健康嗎?隨著近年運動風氣日盛,運動傷害門診的求診人數也逐步增加... 為什麼
            常常受了傷卻不自知?旁人無法協助找出異狀嗎?有時候,身體呈現出來的異狀往往太過
            不明顯,對於人的肉眼或感覺而言不容易察覺;但倘若應用科技於其中,也許能有不同的
            發現。 【昨日科幻今日日常】:2018台灣醫療科技展專題 體適能的評估,對所有人來說也許
            都不陌生,以跑步為例,從小我們便不斷反覆接受100公尺跑步...等項目的測驗,不過除了
            速度之外,我們還能看出什麼資訊?當今天跑步狀態發生異常時,我們能在跑步過程之中察覺
            到什麼呢? 時至今日,隨著科技的演進,我們事實上能知道更多資訊。 在運動訓練監控及體
            姿體態檢測的領域中,宇康醫電便十分關注科技在其中能扮演的角色。宇康醫電康博銓
            副總經理表示,「以前的體適能評估用人工來計算,按碼錶、在旁邊看,很多細微的變化是
            看不出來的,例如前後速度的變化等等,記錄也往往不準確。」 結合影像辨識、動作偵測
            和運動醫學常態模型分析技術,在體適能狀態判讀的精確性上,比起過往有很大的進步,
            可以對動作、時間做更精準的計算判斷,減少人工判斷的誤差。 除此之外,由於能結合運動
            醫學常態模型,因此新的體適能評估方式可以提供改善建議及協助專業人員開立運動處方,
            對體適能及體姿體態進行有效回饋,在運動輔助上更有效率。康副總表示,宇康所提供的
            電腦化體健宜系統,可以讓專業人士更有效率為更多受測者提供有價值的服務。 「傳統的
            體適能評估,往往會運用到機械式器材,因此對於老人和小孩而言會有安全性的風險。」
            康副總表示,透過影像辨識與動作偵測來進行體適能評估,另一大優勢便在於安全性,今日的
            體適能評估方式,即便是銀髮族及小孩子也能放心進行使用。 針對銀髮族的身體狀態,
            在影像辨識的過程中也能發現更多端倪。「老人家的折返過程,透過影像來判斷,平衡感好
            不好?走路會不會晃動?是不是容易走過頭?」 康副總以宇康的銀髮族平衡控制測驗為例,
            分享測驗過程中所能了解的資訊。在評測以後,受測者可以得到詳細的報告,報告上記載著
            每項項目與常模星等相比的等級、體適能年齡及改善建議。再配合醫療院所專業人員的
            各項指示,能夠讓受測者得到更多的指示。 與體適能評估的概念相同,透過科技來輔助健身,
            在最近幾年來也是備受關注的領域。康副總分享,「智慧健身可透過各種穿戴裝置,及時
            了解使用者的運動狀況,配合專業教練的指示,增加或減少運動的強度,達到更好的
            運動效率。」 針對運動健身領域,宇康便設計了3D Biking及3D Rowing兩種軟體,
            前者為飛輪車訓練軟體,後者為划船機訓練軟體。此兩個軟體透過競賽,可減少使用者
            對於運動的乏味感,增加對於運動的積極性;同時,此兩樣軟體能搭配感測器將運動的使用者
            的各項運動數據投射到電視上,讓教練們可以得知使用者狀況,給予適時的幫助。 在今年度
            的2018台灣醫療科技展中,宇康將同時展出成人體適能的平衡力檢測以及銀髮族的肌耐力
            檢測。在測驗結束後,宇康也將展示常模星等以及該項測驗的體適能年齡,提供民眾做參考,
            了解自己的身體狀況;同時民眾也可近距離體驗3D Biking及3D Rowing,即時認識自己
            運動過程中的各項運動數據! 除了宇康所提供的體適能評估及智慧健身外,2018台灣醫療
            科技展也將展出更多最新醫療科技應用,幫助民眾運用最新科技掌握身體狀況,維持健康的
            生活。
            '''
        ),
    )
    assert parsed_news.category == '風生活,品味生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1541446080
    assert parsed_news.reporter == '林斯涵'
    assert parsed_news.title == '以為跑步就能健康?利用3D體感攝影機察覺細微變化,從姿態判斷出身體問題!'
    assert parsed_news.url_pattern == '601348'
