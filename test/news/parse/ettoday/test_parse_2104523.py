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
    url = r'https://star.ettoday.net/news/2104523'
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
    print(parsed_news.article)
    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            日本東京國際展示場(Tokyo Bigsight)舉辦的「危機管理產業展
            (RISCON TOKYO)2021」上,以展覽主題「PLAY SURVIVE在玩樂中為生存做準備」
            為主題,推出一系列的概念產品。 PLAY SURVIVE在玩樂中為生存做準備 這次危機管理
            產業展(RISCON TOKYO)2021的策展主題「PLAY SURVIVE在玩樂中為生存做準備」,意旨
            透過普及防災工具(機械材料)在日常的接觸機會,讓一般民眾能藉由” 平時休閒玩樂、災變
            救難援助”的做法,提升民眾在面對災變時的應變能力。 在人們擔心災害風險增加的情況下,
            ”自保”和”日常互助網路建設”,以及政府及公部門機關的緊急援助和救助範圍的重要性日益
            凸顯,而在現階段的防災概念裡,一般民眾僅能準備防災物品、緊急生存食品等相對被動的
            方法對應。 而為了提升民眾在災害發生時不僅能自救、還有餘力可以救人的目標,將
            救助器材、救護知識等融入日常生活中,讓民眾能藉由日常就可碰觸的物品,學習正確的
            機械操作知識與技能,這點就相當重要。因此,YAMAHA這次就以展覽主題「PLAY SURVIVE
            在玩樂中為生存做準備」為發想,推出摩托車、洪水救援船、發電機、LED緊急照明燈具等
            多種產品,提供小至個人、大至社區全體皆適用的防災器械。 危機管理產業展
            (RISCON TOKYO)2021展出內容 TRICITY 125/155是搭載LMW※技術的三輪車款,具有
            車身穩定性高、騎乘視野寬闊等多項優點,且有大平台能搭載急難救助設備,面對災害現場的
            各種路面條件都能輕易騎乘跨越,平時能當作巡邏車、災害發生初期就可作為快速收集災害
            現場資訊及搬運救援物資的工具,能夠發揮極大作用。 LMW是Leaning Multi Wheel的
            縮寫,泛指有三顆輪胎以上,並且能夠和摩托車一樣傾斜轉彎的車輛統稱
            。 Tenere 700 (市售車款) Tenere 700是在優異越野性能與旅行實用機能之間,
            取得高度平衡的冒險車款,充分體現「PLAY SURVIVE在玩樂中為生存做準備」的防災風格,
            YAMAHA將在展覽現場推出一輛以Tenere 700為基礎改良的防災概念款。 RS-13洪水
            救援艇(概念模型)製作目的是在發生水災時進行救援活動的船隻。考量到收集災害現場資訊
            、符合救援及疏散等目標後,YAMAHA設計出一艘設計緊湊、總長僅約四公尺,但最多能同時
            容納六人的救援艇,同時它還有著追求高度機動性的性能,以及允許人員快速上下船的高度
            易用性。 MJ-FX HO救難型水上摩托車(概念模型)以在休閒領域獲得眾多客戶支持、
            日本東京消防廳等水上救援組織也採用的產品MJ-FX HO 水上摩托車為基礎,利用其獨特的
            超高機動性能,能在水域發生災害時第一時間趕赴現場,YAMAHA將在現場展示配備各種特殊
            救援器材的救難型概念款。 EF1800iS/EF900iSGB2發電機(概念模型)YAMAHA將展示以
            ”任何人都可以隨時使用的發電機”為目標的產品。YAMAHA強化了對應災難的獨特性,例如
            更容易啟動,以及即使沒有任何光線的地方,也易於使用者操作的螢光塗料等
            。 X-BUSTER LED 移動式照明燈(消防型)用於消防活動的LED移動式照明燈,在煙霧中具
            有出色的透光性,配備聚焦、擴散等兩種模式,支持各種需要照明的情況,且體積雖輕巧緊湊,
            但卻集合了方便且易於操作的先進功能與設計。
            '''
        ),
    )
    assert parsed_news.category == '車'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634741520
    assert parsed_news.reporter is None
    assert parsed_news.title == 'YAMAHA「三輪車」成防災專武!裝載急難救助設備 迅速支援現場'
    assert parsed_news.url_pattern == '2104523'
