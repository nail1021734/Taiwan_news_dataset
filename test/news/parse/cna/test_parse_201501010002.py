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
    url = r'https://www.cna.com.tw/news/aipl/201501010002.aspx'
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
            告別2014、歡迎2015,全台瘋跨年。好天氣讓台北101、台中、劍湖山、義大世界四大
            煙火秀照亮全台星空。各縣市跨年晚會群星獻藝,聚集人潮,全台嗨翻天。 高雄夢時代跨年
            晚會全台最早開場,「姐姐」謝金燕熱舞開場,以一襲閃亮的籃球裝造型現身,一連演唱
            「傷心的人別聽慢歌」、「The Fox」等動感歌曲,還換上狐狸扮相,接著唱「要發達」
            時,還在現場發送發財金。 最後以招牌歌曲「姐姐」壓軸,謝金燕再度使出「巨型安全帽」
            的梗,將安全帽加裝在類似沙灘車上,原本帥氣出場,沒想到安全帽竟然意外裂掉,姐姐
            尷尬地卡在車上,最後舞群衝上前護駕,將姐姐推回主舞台。謝金燕國、台、粵、英四語
            連續演唱28分鐘,萬人齊High。 2015紫耀義大跨年晚會,藝人輪番接力上台載歌載舞,
            安心亞打頭陣,在義大球隊犀睛女孩熱舞相伴下,High翻全場;「鐵肺女王」李佳薇接著
            獻唱,高亢嗓音令人如癡如醉。高雄市長陳菊偕議長康裕成到場與民眾同樂。壓軸蔡依林
            登場,新歌「吥」走2014,跨年夜掀高潮。 「2015領航臺中跨年晚會」今晚以雙主場形式
            登場,北區的國立台灣體育運動大學體育場及豐原區的市立體育場一連串精彩節目讓
            台中high起來。 「電音女王姐姐」謝金燕、「甜新教主」王心凌聯手壓軸演出,搭配
            兩主場共將施放一萬多發焰火。新任台中市長林佳龍也與民眾跨年同歡,先豐原場開幕
            與大家見面,再轉往臺中場陪民眾倒數計時,共同迎接嶄新希望的2015年。 2015台南
            喜洋羊跨年晚會今晚在高鐵台南站旁廣場登場,藝人熱力開唱,吸引大批紛絲湧入。藝人
            劉香慈與舞群的開場熱舞就引來尖叫歡呼不斷,隨後接力上台的黃小琥、八三夭賣力
            演出,現場氣氛熱烈。包括「宅男女神」安心亞、「台語小天后」曹雅雯、戴愛玲、ALIN
            等人也陸續帶動高潮,跨年倒數時刻,吳克羣壓軸演唱。 升格直轄市的桃園市今天晚間在
            多功能藝文廣場前舉行跨年晚會,數萬人擠爆現場。包括藝人家家、李佳薇、倪安東、
            曾沛慈、林凡、陳零九、孫盛希、官靈芝、宇宙人樂團等陸續登場,炒熱氣氛。羅志祥與
            盧廣仲擔任壓軸跨年演出,11時30分過後登場演出,一起從2014年12月31日跨年演出到
            2015年1月1日。 台北市政府前廣場「台北最High新年城2015跨年晚會」由亞洲舞王
            羅志祥、林俊傑等眾星跨年倒數。首先由6歲雙胞胎左左右右率先活力開場,大跳「打氣歌」
            ,可愛指數破表。羅志祥駕著價值200萬元的野馬跑車出場,一身黑色勁裝連唱「獨一無二」
            等6首歌,載歌載舞,台下觀眾尖叫聲不斷。 「新竹向前行 感恩再出發」新竹縣跨年晚會
            熱鬧登場,近萬民眾陸續湧縣府廣場前「逗熱鬧」,藝人羅美玲擔任開唱嘉賓,現場帶來
            「我在你身旁」、「勇者的浪漫」以及「愛一直閃亮」三首歌,讓台下不少民眾手拿加油棒
            隨韻律搖擺,LED燈光在黑夜中與台上相互呼應,羅美玲還為此走下台與民眾互動、簽名,場面
            相當熱鬧。 樂團五月天今晚在高雄世運主場館跨年開唱,以「星空」開場,全場5萬支互動式
            螢光棒點亮變5萬盞螢光,溫暖高雄跨年夜。五月天連續3年在高雄世運主場館舉行
            跨年演唱會,「Light Up The Hope螢火晚會」為與全場5萬名粉絲「跨年大圍爐」,特別
            打造直徑達50公尺的同心圓舞台,並首次運用吊掛塔系統喇叭,讓歌迷享受聽覺震撼。 音樂
            老頑童陳昇連續21年舉辦跨年演唱會,今晚他在台北國際會中心,穿上藍底白點襯衫
            開唱,打上可愛的領結,牽著3隻小狗氣球出場模樣逗趣,今晚昇哥的太太、兒子坐在觀眾席
            陪他一起度過第21跨年演唱會,一連演唱10首歌曲,直到演唱「福爾摩沙」才擠出
            一句話:「台灣要加油啦!」
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1420041600
    assert parsed_news.reporter == '台北'
    assert parsed_news.title == '蔡依林跨年壓軸 新歌「呸」走2014'
    assert parsed_news.url_pattern == '201501010002'
