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
    url = r'https://www.cna.com.tw/news/aipl/201812310105.aspx'
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
            2019年即將到來,全球各地將在今年最後一天狂歡慶祝,從東京澀谷街頭到倫敦耀眼的煙火秀、
            紐約時報廣場跨年,都將吸引巨量人潮。 日本跨年有些民眾一邊吃年夜飯、蕎麥麵,一邊收看
            日本放送協會(NHK)跨年節目「紅白歌唱大賽」,快跨年時,有些人會前往寺院參拜,聆聽寺院
            108聲鐘響。東京淺草寺、增上寺與明治神宮等有多遊客前往新年第一次參拜。 近年來,號稱
            「全球最繁忙的十字路口」的澀谷十字路口成了年輕人跨年「名所」。日本年輕人過節慶像
            萬聖節,也愛到澀谷十字路口一帶表達歡慶心情,警方嚴防熱情民眾嗨到脫序,動員大批警力、
            警車戒備。 澀谷跨年執行委員會今年除夕第3度舉辦
            YOU MAKE SHIBUYA COUNTDOWN2018-2019活動,去年有逾6萬5000人參加。今年澀谷
            車站前十字路口、道玄坂、文化村通、井頭通等一帶從12月31日晚上9時(台灣時間8時)起
            到2019年1月1日凌晨2時之間實施交通管制,車輛、機車等禁止通行。 中國民眾跨年相約
            撞鐘,知名古剎都有活動,但和台灣不同的是多數寺廟需收費。上海一寺廟的撞鐘票曾飆到
            人民幣318元,新年鐘響徹魔都時,就是寺廟盆滿缽滿時。 泰國觀光局今年在曼谷湄南河畔
            與商場合辦跨年倒數晚會,將施放號稱泰國史上最長與最盛大的煙火秀,預計吸引百萬人觀賞,
            在湄南河(昭披耶河)畔施放。 除了煙火秀,北部的清萊(Chiang Rai)、東北部的
            那空帕儂(Nakhon Phanom)、中部的叻丕(Ratchaburi)和南部的沙敦(Satun)等地都有
            跨年傳統音樂和舞蹈等表演。 新加坡濱海灣慶跨年預估50萬人參與,欣賞7分鐘煙火
            表演。此外,從26日到31日在富麗敦酒店、魚尾獅公園與藝術科學博物館等遊客聚集地點,
            都有以「築夢未來」為主題的投影燈光秀。 在柏林市中心,從
            布蘭登堡門(Brandenburger Tor)到勝利女神柱(Siegessaeule)、全長2公里的廣場,
            每年都會舉辦跨年狂歡晚會,現場有樂團助興,吸引數十萬人參加,是德國規模最大的跨年
            活動。 「黃背心」運動在12月初掀起法國數十年來罕見的嚴重街頭暴力,雖然抗議人數
            已減少,政府對維安仍不敢大意。 香榭大道、凱旋門、
            托卡德洛廣場(Trocadero)、艾菲爾鐵塔及戰神廣場(Champ-de-Mars)在31日周邊
            都要管制,行人進入香榭大道前要接受隨身行李檢查,也可能搜身,禁止攜帶武器,假的
            也不允許。另外,煙火等爆裂物、酒精飲料、玻璃瓶飲料也在禁止攜帶之列,但管制區內的
            酒吧或餐廳會提供酒精飲料助興。 巴黎警署建議民眾多使用大眾運輸系統,跨年夜的
            巴黎地鐵、郊區火車(RER)和公車徹夜運行,31日傍晚5時起到元旦中午免費搭乘。 跨年聖地
            英國倫敦將在泰晤士河畔倫敦眼(London Eye)的炫目煙火秀中迎接2019,煙火秀9月底
            開放售票,數萬張票搶購一空。 泰晤士河畔及河面上31日晚間都將擠滿來自世界各地的遊客,
            欣賞萬發煙火照亮夜空。英國廣播公司(BBC)實況轉播。去年煙火秀達12分鐘,發射約萬發
            煙火。 倫敦另一景點大笨鐘目前在維修期,平時消音,但跨年會特別敲響報時,迎接2019年
            到來。 紐約時報廣場跨年活動今年將頌揚新聞與言論自由,邀請
            華盛頓郵報(Washington Post)、紐約時報(New York Times)等媒體高層與記者擔任
            特別嘉賓,接近午夜時登台,一同按下跨年倒數60秒的水晶球降落按鈕。 主辦單位表示,
            希望新聞業前途更光明,記者面臨的攻擊減少,避免新聞從業人員處境日益危險。 今年水晶球
            設計主題為「和諧之禮」,鑲有192片全新三角水晶玻璃,玫瑰花狀雕刻看起來協調地
            相互流動。水晶球直徑3.6公尺,重約5400公斤,表面覆蓋2688片大小不一的
            三角水晶玻璃。 今年時報廣場跨年夜恐降雨,官方預估仍會湧進大批民眾。紐約警方基於
            維安考量,今年將首次出動無人機監控。 加拿大多倫多跨年活動少不了煙火,鄰近的
            尼加拉大瀑布煙火秀吸引各地人士,堪稱全加最盛大的免費跨年活動。 多倫多市府前
            廣場(Nathan Philips Square)是人潮最多也最盛大的跨年晚會地點。今年跨年除了
            煙火與冰上派對,還有DJ及現場音樂表演。 多倫多全市公車及地鐵連續6年在跨年夜晚
            7時至元旦早晨7時免費搭乘,今年還有業者提供免費汽水和酒類飲料,讓乘客
            共飲迎接2019年。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1546185600
    assert parsed_news.reporter is None
    assert parsed_news.title == '煙火秀加午夜派對 迎接2019全球瘋跨年'
    assert parsed_news.url_pattern == '201812310105'
