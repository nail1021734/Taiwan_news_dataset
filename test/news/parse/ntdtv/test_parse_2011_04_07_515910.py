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
    url = r'https://www.ntdtv.com/b5/2011/04/07/a515910.html'
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
            英國廣播公司7日報導,利比亞東部的反對派武裝說,北約導彈又一次誤炸他們的部隊。 據
            利比亞東部城市艾季達比亞的醫療人員透露,北約戰機的轟炸至少造成13名反政府軍成員喪生,
            很多人受傷。 西方媒體根據軍人和醫護人員的消息報導,一批坦克、裝甲車和火箭發射車被
            四枚導彈擊毀。 據美聯社報導,北約駐布魯塞爾的代表表示,目前還沒有轟炸艾季達比亞地區
            的情況。 此前在港口城市卜雷加,曾發生利比亞反對派武裝「鳴槍慶祝」引來北約戰機誤炸
            事件,造成十多人死亡。反對派發言人當時表示此事件純屬「誤會」。 北約6日加強了在
            利比亞的空襲力度。 利國人肉盾牌 北約空襲棘手 北大西洋公約組織(NATO)昨天坦承,由於
            利比亞政府軍把平民當做人肉盾牌,北約執行空襲時必須「格外小心」,但誓言會竭盡所能
            保護米蘇拉塔(Misrata)居民。 聯合國秘書長潘基文(Ban Ki-moon)發言人說,潘基文
            緊急呼籲,立即停止濫肆動用武力對付平民百姓,法國也承諾,對遭圍困的米蘇拉塔,開闢1條
            海上走廊。 北約作戰副指揮官哈定(Russell Harding)少將告訴記者,「北約部隊格外
            小心謹慎,以避免傷及靠近激戰的平民,而這往往是利國政府軍的技倆。」 卡扎菲致信求
            停止空襲 美國駁回 據中央社報導,利比亞卡扎菲(Muammar Gaddafi)私函美國總統
            歐巴馬,懇求聯軍停止空襲,但遭美國務卿希拉里.柯林頓(HillaryClinton)斷然拒絕幷
            且要求他撤軍流亡。 歐巴馬收到卡扎菲一封多達3頁的信,拜託西方聯軍停止轟炸他的部隊。
            但是美國官員直接拒絕他的請求。 希拉里和意大利外長佛拉第尼(Franco Frattini)連袂
            召開記者會的時候說:「卡扎菲先生知道他必須做些甚麽。」 她說:「必須停火,他的部隊
            必須從各城市撤出,他的部隊以非常暴力與高昂的生命代價強力佔領的城市。他自己則必須
            決定是否下臺,離開利比亞。」 在利比亞反抗軍重新取得一處油港之際,卡扎菲寫信提出上述
            呼籲。 白宮發言人卡尼(Jay Carney)陪同歐巴馬到賓州時告訴隨行記者:「我們能證實的
            是的確有一封信,但這顯然不是(卡扎菲寫給歐巴馬的)第一封信。」 卡尼說:「總統提出的
            條件很清楚,需要的是行動,不是耍嘴皮子。」 他拒絕說明信中的詳細內容,不過根據美聯社
            (AP)取得的信件影本,卡扎菲還是在信中對歐巴馬的稱呼包括「我們的兒子」和「閣下」等
            稱謂,幷且懇求他阻止卡扎菲所謂「對小國寡民的開發中國家發動的不公義戰爭」。 美國
            官員說,華府這幾年來已經收到卡扎菲好多封信,華府對於最近這一封信的態度跟以前
            幷無二致。 歐巴馬已經力求避免在利比亞造成人道災難,也將動亂局限在這個北非石油
            輸出國內,以免周邊各國也同樣陷入混亂,同時又試圖局限美國在聯軍行動的參與程度。 歐巴馬
            已經呼籲卡扎菲下臺,但他也堅稱美國不會軍事推翻卡扎菲。 希拉里說:「對卡扎菲的期待
            不是秘密,他愈早下臺,愈早結束流血征戰,對每個人都更好。」 哈定說,卡扎菲
            (Moamer Kadhafi)部隊「越來越訴諸非傳統戰術,混合使用道路交通及平民的生命,作爲
            他們推進時的擋箭牌。」
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1302105600
    assert parsed_news.reporter is None
    assert parsed_news.title == '人肉盾牌 北約空襲棘手誤炸利比亞反對派武裝'
    assert parsed_news.url_pattern == '2011-04-07-515910'
