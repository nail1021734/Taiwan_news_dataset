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
    url = r'https://www.cna.com.tw/news/aipl/202012300309.aspx'
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
            12月21日晚間,新航一架波音747-400貨機,載著新加坡首批疫苗降落在樟宜機場,
            轟隆隆引擎聲劃破天際。近一年來,疫情重創航空業,新加坡力拚轉型,如同田螺含水過冬,
            只要有一滴水就有希望。 隨著疫苗研發成功,新加坡作為全球航空樞紐,正摩拳擦掌、
            做好準備,要在世界疫苗配送上扮演要角。 首批抵達新加坡的COVID-19疫苗是由美國
            輝瑞藥廠(Pfizer)和德國生技公司BioNTech研發,疫苗於運送途中必須保存在約
            攝氏-70度的低溫。為確保能順利完成任務,新航事先在同一條飛行路線上進行演練,
            因為這趟運送任務,不僅攸關新加坡人健康,更是新加坡突破經濟困境的希望。 2019
            冠狀病毒疾病(COVID-19,俗稱武漢肺炎)疫情自年初以來肆虐全球,各國為防疫所需紛紛
            採取嚴格邊境管制措施,全球航空業飽受衝擊。新加坡身為區域航空樞紐,受到的影響更為
            明顯,樟宜機場大廳以往的人潮不復見,如今只剩下零星旅客。 秋冬來臨之際,許多國家
            又出現新一波疫情,為嚴防疫情擴大,部分國家甚至再度祭出鎖國措施。相較之下,新加坡
            疫情維持穩定,當局採取安全、逐步開放邊界的策略,目前已單向對台灣、澳洲、紐西蘭、
            中國、越南等開放邊境。 隨著星國疫情趨緩,不少行業已露出復甦跡象,但新加坡交通部長
            王乙康坦言,「航空業的寒冬仍持續中」。樟宜機場目前旅客量仍只有疫情前的2%。 他在
            樟宜機場正式營運39週年的回顧影片中指出,眼前最重要的任務是恢復安全航空旅行,
            以及恢復新加坡航空樞紐的地位。在安全前提下,「我們會儘可能多載一點旅客,若沒有旅客
            可載的話,就載貨物」。 事實上,在人員流動受到限制下,貨運已成為各航空公司求生存的
            主力。樟宜機場網站資料顯示,機場今年11月客運量較去年同期減少98.1%,相較之下,
            貨運減幅和緩許多,11月貨運量只比去年同期少了21.1%。 隨著疫苗研發成功,各國
            陸續採購之際,如何安全、有效地運輸疫苗成為各國當務之急。新加坡看準這波未來趨勢,
            早已著手準備。 新加坡總理李顯龍14日發表全國演說時表示,「作為全球航空樞紐,
            我們在全球疫苗運送上扮演關鍵角色」。星國已有健全的貨物處理系統,像是DHL等全球
            主要物流公司在新加坡都有據點。 另外,樟宜機場、新加坡航空更是不可或缺的角色。
            作為新加坡國籍航空,新航於5月就在公司內部成立COVID-19工作小組,以確保公司在貨運
            及安全載運疫苗方面等工作,做足準備。 新航表示,它在空運藥品上扮演重要角色,
            特別是從歐洲、印度到東南亞、澳洲、紐西蘭的生物藥物運送。新航也持續擴大
            它的冷鏈服務THRUCOOL,並於今年9月將網絡擴及至澳洲布里斯本、墨爾本。 終於,
            12月21日晚間,新航一架波音747-400貨機載著星國首批COVID-19疫苗從比利時飛抵
            樟宜機場。新航指出,這批疫苗成功運抵新加坡證明,「新航與樟宜機場已做好準備,
            能執行全球疫苗運輸及配送的重要工作」。 新加坡採購的疫苗預計未來幾個月將陸續抵達。
            新航表示,未來貨運能量將優先用於載運疫苗,這包括新航7架波音747-400貨機待命,
            有需要的話,也會調派新航客機執行載運疫苗的任務。 星國媒體社論指出,在國際疫苗
            輸送上,新加坡與鄰近的馬來西亞、印尼等國有很大的合作空間,支持航空運輸轉型。
            雖然航空業寒冬尚未遠去,但新加坡已滿懷信心,有能力成為亞洲運送及分配疫苗樞紐。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1609257600
    assert parsed_news.reporter == '侯姿瑩'
    assert parsed_news.title == '田螺含水過冬 新加坡力拚轉型全球疫苗配送中心'
    assert parsed_news.url_pattern == '202012300309'
