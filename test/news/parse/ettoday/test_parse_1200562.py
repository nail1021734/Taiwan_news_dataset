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
    url = r'https://star.ettoday.net/news/1200562'
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
            今年全球最注目的IPO(首次公開募股)案來了!今年初,小米傳出上市消息以來,估值一度喊
            到近千億美元,最後下調到550億美元到700億美元(約合新台幣2兆元)間。但上看61億美元
            的募資規模,已成為近兩年全球最大規模上市案。 受注目還有另一個原因:兩年的逆轉勝傳
            奇。「浴火重生的中國鳳凰。」《金融時報》評價。2015年,小米手機出貨量逾7千萬台,但
            隔年就跌到4100多萬台。在一片看衰聲中,2017年出貨量卻又重返9千萬台以上。「這在全
            球手機產業極為罕見,沒有一家手機大公司下滑以後,可以成功turn around!」雷軍說。 大
            勢難擋。手機市場的成長飽和,已讓宏達電三年虧掉5個股本。若小米只懂得靠抄襲與打低
            價戰,為何其營業利潤率還能維持4.7%以上,甚至比宏碁、華碩與聯想等品牌還高? 雷軍說,
            最低潮時,小米進行了一堂「補課」。「一家優秀的公司首先考慮利潤,偉大公司往往考慮
            人心,是用戶怎麼想,」深入人心後,他看到,用戶其實根本不在乎線上還是線下,而是希冀輕
            鬆買到「高性價比」,即好用但不貴的商品。 然而,原本在線上銷售的小米,若要進軍線下,
            以新零售模式去服務用戶,首要挑戰就是:傳統實體通路的高抽成結構,這將讓小米很難維持
            中低價位。 小米若自建實體門市,勢必要提高坪效。這代表,它不能讓消費者只有手機一種
            選擇。所以,小米從手機一路賣到兒童書包與電動牙刷。走進小米之家的消費者,購買者平
            均買2.7項商品,藉由提高坪效,小米才得以降低通路在成本結構中的比重。 小米賣電動牙
            刷,它會記錄你的刷牙軌跡,可建議你的刷牙姿勢。甚至,後續小米的電鍋,也可讓你在上面
            直接下單買米。當它賣給你更多硬體,就有機會賣出更多毛利率高達6成的服務,形同iPhone
            手機賣遊戲的邏輯。 然而,要打造新商業模式,何其不易!小米供應鏈負責人,創辦人之一的
            劉德算過,若公司要把產品項目從單純的手機,拓展到一百多項商品,不假手他人,至少需要
            養數萬名人力。 後來,小米的選擇如今日所見,它採取生態系的方式解決問題。小米提供大
            量新創公司開發協助,以強大供應鏈網絡,協助新公司縮短摸索期。現在,單小米生態系就有
            百間公司,有5家成為估值破10億美元的獨角獸。 雷軍非常執著高性價比。但他所指的並非
            絕對的低成本,而是以「高顏值」設計加上功能再除以合理價格的比率。他說,如此,消費者
            走入店內才會覺得厚道,「閉著眼睛都能買」。 從背負著抄襲罵名開始創業,在「活下來」
            的過程中,近2億小米粉絲,一直是該公司最鐵桿的靠山。小米透過粉絲口碑傳播,降低行銷
            費用,省掉通路成本,又藉著其大量人流,促成生態系的建立,解決原本的重資產投資
            問題。 現在,小米已進化到第三階段,預計將30%的募資金額,用於研發核心產品。今年,其
            推出的MIX系列手機憑著全螢幕設計,已被三家世界級博物館列入永久館藏。 中美貿易冷戰的
            爆發,讓中國經濟出現變數,也讓市場對於小米估值更嚴格的檢視。6月19日,小米宣布暫緩
            中國存託憑證(CDR)發行,目前甚至沒有重新啟動的計畫,讓投資人對其前景保守看待。 雷軍
            並未正面回應對估值的看法。但他對小米未來發展仍具信心。他說,過渡期間,來自生態系的股
            權投資,將成為其利益來源貢獻。目前,它也是愛奇藝的第二大股東。 雷軍意氣風發,但挑
            戰仍多。接下來,其若能從硬體跨越到互聯網服務商,開始靠後者賺錢,小米的商業模式才算
            真正圓滿,讓大家再度見證深耕用戶後的威力。
            '''
        ),
    )
    assert parsed_news.category == '財經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530090840
    assert parsed_news.reporter == '康育萍'
    assert parsed_news.title == '小米從被罵抄襲到IPO 雷軍:讓消費者閉眼都買'
    assert parsed_news.url_pattern == '1200562'
