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
    url = r'https://www.ntdtv.com/b5/2011/12/20/a634431.html'
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
            在日本大阪,一名從中國大陸來的婚紗影樓老闆劉先生說,“現在應該是大陸婚紗攝影業最
            紅火最旺的時候,但是他的影樓根本不敢再往下開了”,這背后有怎樣的遭遇,他為何赴海外
            求生?我們一起來走進他的故事。 劉志貴,現居日本,原哈爾濱市方正縣的一家婚紗影樓
            老闆,家庭和睦,經濟條件也很好。40年的人生拚搏,他心中時常在找尋著人生的
            意義。 1997年5月劉志貴開始修煉法輪大法,按照法輪功“真、善、忍”的準則做一個好人,
            漸漸的煉功後丟掉了多年的藥罐。巨大的身心變化,使他堅信法輪功是平和的修煉功法。
            2000年6月喜得貴子,一家其樂融融。 法輪功這個古老的修生養性之道,使全世界50多個
            國家的億萬人受益。由於在中國修煉法輪功的人越來越多,江澤民感到惶恐不安,1999年7月
            20日起,他發起了一場殘酷無情鎮壓法輪功的運動。2001年2月11日劉志貴到北京上訪,得知
            掛著招牌的北京政府信訪辦不接受學員上訪後,直接在天安門廣場喊出:法輪大法好!迅速
            圍上十幾個便衣將其按倒,並抬到警車上進行毒打。方正縣警察聞訊火速趕至北京將他
            押回。 劉志貴先後被關押到方正縣第二看守所、東城區看守所、方正縣第一看守所、方正縣
            洗腦班、哈爾濱市新建集訓隊和呼蘭集訓隊。2004年2月19日起他被非法關押在臭名昭著的
            哈爾濱呼蘭監獄三年。 劉志貴:“方正縣那些煉法輪功的,有很多被長時間刑訊逼供。有的
            被打的眼睛失明,有的被腰部打的錯位。而且有的被迫害致死。” 在這裡他目睹了中共對
            善良的法輪功學員的殘酷迫害。 劉志貴:“五大隊一分隊有個叫孫紹民的,犯人頭把唾液
            唾到地下,讓他當場舔起來。用各種方法折磨他。七天七夜不讓睡覺,而且七天七夜站著。
            ” 長期在嚴酷環境中,他選擇了堅持信仰,拒絕在轉化書上簽字,但心裡的煎熬使他精神幾乎
            崩潰。 劉志貴:“問我說,你還煉不煉了?我說煉。當時王濱就打我的前胸,打我的臉。” 惡警
            折磨法輪功學員的酷刑手段極其殘忍,包括:綁在老虎凳上用老牛錘(二尺長的三角帶,用鐵線
            纏繞在二尺長的木棍上做的鞭子)用針扎手指尖、腳趾尖、胳膊、背部、雙腿等部位,用手指
            用力彈眼球等。 劉志貴的妹妹談到了中共迫害使家人遭受的巨大痛苦。 劉志穎:“我哥哥是
            我們家的頂樑柱嘛,所以說頂樑柱折了之後真的是家裏挺苦惱的。我父母年齡也大了,孩子
            還小。那時我父母也是因為我哥哥進去了之後,身體非常不好。我父親犯起心臟病了,然後
            幾次叫救護車到醫院搶救。我哥哥他修真善忍沒有錯嘛,也知道我哥哥非常好。” 呼蘭監獄
            的殘酷迫害沒有動搖劉志貴對信仰的堅持,他最後不得不以長期絕食來要求人權。 劉志貴:
            “在搶救我的時候,隊長王濱惡狠狠的說死了才好。在我醒來之後,他們還繼續對我
            迫害。” 劉志貴很幸運,他來到了海外自由社會,家庭團圓。每逢天氣不好時他的頭腦中就會
            翻起那段刻骨銘心的遭遇。 劉志貴:“我今天把這個事實講出來,是讓全世界的人都看到中國
            (共)在迫害法輪功的真正的事實,讓所有的人都伸出一雙援助之手,馬上停止這場
            迫害。” 劉志貴給我們講述的是一個堅持信仰的故事,他相信千千萬萬的中國人會認識到
            中共的邪惡,不再協同它,從而退出中共。
            '''
        ),
    )
    assert parsed_news.category == '法輪功,法輪功人權'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1324310400
    assert parsed_news.reporter is None
    assert parsed_news.title == '海外求生 記影樓老闆劉志貴'
    assert parsed_news.url_pattern == '2011-12-20-634431'
