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
    url = r'https://www.storm.mg/article/4020745?mode=whole'
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
            加油泵一直是德國人的風向標。在這個國家,沒有什麼事情比汽油和柴油價格高企更讓人
            不安。目前,柴油價格創下了歷史新高(平均每升1.56歐元),汽油價格也在難以阻擋地
            飆升。 綠黨的一個夙願終於可以實現了。在1998年的競選宣言中,綠黨要求將每升汽油的
            價格提高到5馬克(按今天的匯率計算為2.55歐元)。這個主張是為了提高駕車成本,從而
            減少排放,改善環境。大多數德國人不以為然。 如今,盡管時局不利,綠黨即將再次進入
            內閣。新冠疫情遠未結束,但其經濟影響已經十分巨大,能源價格高漲是其中之一。
            不僅德國如此,全球亦然。 此番情形不難解釋。全球經濟的復蘇速度超過了所有人的預期,
            引發了對能源的巨大需求,從而推動價格上漲。但是,目前的經濟陷入了史無前例的困境。
            今年以來,僅天然氣的批發價格就令人難以置信地飆升了440%。 石油的價格也接近歷史
            最高點,在一年之內翻了一番。不過,可能有點違揹人們的常態反應的是,這實際上是個
            好消息--也許不是對車主,而是對走向氣候中和的經濟轉型而言。 這正是能源轉型應該
            做的事情:化石燃料必須變得如此昂貴,從而讓可再生能源受到青睞。如果風能、
            太陽能和水力發電是更便宜的選擇,那麼煤炭和天然氣就會自動隱退。至少計劃應當
            如此。但是,眼下困難重重,因為我們離這種轉變還有很遠的距離。 不僅德國面臨困境,
            絕大多數國家也左支右絀。目前,人們仍然主要用內燃機駕駛汽車,用石油或天然氣取暖,
            並用燃煤電力作為日常供電。中國剛剛宣佈讓150個已被關閉的煤礦重新投入
            運營。 與此同時,德國還厚顏無恥地好為人師,自稱榜樣。真希望沒有人來模仿我們所謂的
            能源轉型。到目前為止,德國除了花費了大把金錢,別的一無所獲--仍然沒有跡象顯示,
            將會建設一條從北海向南輸送風能的電纜;全國可再生能源在總能源消耗中的比例僅為17%
            (瑞典已經達到56%)。每一個新的風力渦輪機都要通過法庭來爭取。只有將公眾行為納入
            過程之中,能源轉型才會成功。未來幾年,任何人駕車前都要先摸摸自己的錢包,除非他們
            購買(國家補貼的)電動汽車。大眾公司的老闆迪斯(Herbert Diess)計算過,駕駛內燃機
            的成本要比電動汽車高出50%。 冬天為你的公寓取暖也將花費更多,這將給那些經濟困窘者
            帶來更大的壓力。要想讓能源價格不成為社會中的一個分裂因素,就必須對弱勢群體進行
            補貼。 "使氣候保護成為社會公正 "的競選承諾決不能成為一個空洞的口號。 如此一來,
            在德國明年全面棄核的同時,提前淘汰煤炭發電是否明智,引發爭議。除非德國從法國購買
            核電,否則填補此項電力缺口將產生5000萬至7000萬噸的額外排放--這不應該成為解決
            之道。 德國新政府在組閣談判中,不要忘記加速擴大可再生能源生產的目標。從長遠來看,
            這將是控制能源價格危機的關鍵。否則,能源將變得難以負擔,並帶來難以預料的
            後果。 德國之聲致力於為您提供客觀中和的新聞報道,以及展現多種角度的評論分析。文中
            評論及分析僅代表作者或專家個人立場。 © 2020年德國之聲版權聲明:本文所有內容受到
            著作權法保護,如無德國之聲特別授權,不得擅自使用。任何不當行為都將導致追償,並受到
            刑事追究。
            '''
        ),
    )
    assert parsed_news.category == '國際,財經,德國之聲,下班經濟學,財經頭條,商業,經濟'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1635710400
    assert parsed_news.reporter == '德國之聲'
    assert parsed_news.title == '德國之聲評論:能源價格飆升其實是個好消息!'
    assert parsed_news.url_pattern == '4020745'
