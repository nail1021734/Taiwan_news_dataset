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
    url = r'https://star.ettoday.net/news/1200098'
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
            《北京》掃平核航母研發阻礙 大陸開工3萬噸核動力破冰船 中國核工業集團網站近日發布
            公告稱,上海中核浦原有限公司接受中核海洋核動力發展有限公司的委託,針對「核動力破
            冰綜合保障船示範工程技術諮詢」一案進行公開招標,而且目前資金來源已經落實。據了解
            ,這將是中國大陸首艘核動力水面艦艇,具有著里程碑的意義。 《江西》江西設
            立海峽兩岸青年就業創業基地 江西省獲批的2家海峽兩岸青年就業創業基地分別位於吉安
            國家井岡山經濟技術開發區、景德鎮陶溪川文創街區。據了解,國台辦先後在北京、天津、
            遼寧等省市設立75個海峽兩岸青年就業創業基地和示範點,截至2017年底,提供1900家台資
            企業入駐,近9000位台青就業創業。 《北京》2020年將建成700個國​​家重點實驗室 《關於
            加強國家重點實驗室建設發展的若干意見》指出,到2020年,形成定位準確、目標清晰、佈局
            合理、引領發展的國家重點實驗室體系,管理體制、運行機制和評價激勵制度基本
            完善,實驗室經優化調整和新建,數量穩中有增,總量保持在700個左右。 《廈門》廈門老舊
            社區改造 從社區管走向自制共管 廈門市老舊社區在改造工作中,「共同」二字
            是關鍵和核心,自行成立自治小組,開門納諫徵集「金點子」,多方聽取居民的意見,評議改
            造項目,確定建設方案。改造前問需於民,形成共識;改造中問計於民,達成共建;改造後問效
            於民、實現共評,做到群眾滿意才通過。 《陝西》西北大學研發「仿真間諜鳥」 不只
            「突破雷達」還吸引真鳥 西北工業大學從2011年開始著手研發
            「仿真間諜鳥」,可能足以突破雷達辨識,順利潛入敵後或重要據點收集情報,仿生的程度還
            足以吸引真鳥伴飛。據了解,「信鴿」重約200克、翼展約50公分,最大飛行時速可達40
            公里,最長續航時間為30分鐘,機上搭載高清攝影鏡頭、GPS、飛行控制系統和衛星通信
            數據鏈,特製的防震顫軟體,可以保證載機攝像頭的成像清晰度。 《甘肅》甘肅展開
            「紅旗河」考察 「藏水入甘」年調600億立方米 通過青藏高原邊緣繞行的調水路線
            「紅旗河」工程,近日已經有團隊在川滇藏進行實地勘察。該團隊由甘肅省社科院和中鐵
            集團研究院西北分院聯合組成的考察隊,目的是想了解「藏水入甘」的可行性。 《北京》
            雜交小麥豐產優勢明顯 比常規小麥增產20% 北京市農林科學院等科研團隊1992年發現
            小麥光溫敏雄性不育現象和材料,歷時20餘年堅持自主創新,創造出一批強優勢雜交小麥
            新組合,在國際上創立了「中國二系雜交小麥技術體系」。實驗證實,雜交小麥在豐產、節水、
            抗旱、耐貧脊等方面明顯優勢,與常規小麥相比,可增產20%以上,節水30%至50%,用種量減少
            30%以上。 《上海》比002航母廠房長200米! 江南造船廠「4號船塢」曝光 江南造船廠
            近日曝光了一組「4號船塢」外觀照,可以清楚看見搭配的大型龍門吊與部分施工的設備。值得
            注意的是,這個船塢除了是大陸第二艘自製航母的預定建造地之外,它的長度也十分驚人,來到
            了565公尺長,而作為參考,之前承建002航母的大連造船廠船塢長度僅有370公尺,兩者之間
            差了足足近兩百公尺。
            '''
        ),
    )
    assert parsed_news.category == '大陸'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530067260
    assert parsed_news.reporter is None
    assert parsed_news.title == '掃平核航母研發阻礙 開工3萬噸核動力破冰船'
    assert parsed_news.url_pattern == '1200098'
