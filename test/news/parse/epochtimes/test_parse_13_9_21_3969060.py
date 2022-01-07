import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/13/9/21/n3969060.htm'
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

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            從2013年5月4日開始,加拿大聯邦技術移民開始接受新的申請。今年確定了24個優先職業
            類別,從2013年5月4日到2014年4月30日,聯邦將接收5,000份申請(不包括有僱主安排的
            申請和加拿大境內博士生的申請),每類職業限300個配額。申請人需是24個優先職業類別的
            從業人員,在過去10年的工作經歷中需要至少1年以上該優先職業類別的工作經驗才有資格
            申請。 新政開始之後,「加拿大庫先生移民事務所」就接到很多諮詢電話,很多申請人認為
            5,000個配額,會馬上一搶而光。而實際情況並非如此。截至到2013年9月12日為止,移民局
            官方公佈的收到的符合要求的完全申請是1,600個左右。即便考慮有些申請處理滯後的因素,
            與很多人剛開始的估計也相去甚遠。 在24類優先職業類別中,財務和投資分析員
            (Financial and investment analysts)以及計算機程序員和互動媒體開發員
            (Computer programmers and interactive media developers)是最早滿員的
            類別,也是截至到9月12日為止,唯一已經滿員的兩個類別。毋庸置疑,這兩個類別屬於特別
            火爆的職業類別,很多申請人從去年就開始磨刀霍霍,早早做了準備,今年5月4日一開閘,就抓
            緊時間投遞,所以這兩個類別立刻滿員屬於正常。 今年增設了很多工程師類別,原來以為
            這些工程師類別是熱點,但預期和真實的數據有較大差異。到9月12日,土木工程師
            (Civil engineers)的接收數額是108個,機械工程師(Mechanical engineers)的
            接收數額是120個,化學工程師(Chemical engineers)的接收數額是49個,計算機和
            通信工程師(Computer engineers)的接收數額是210個,採礦工程師
            (Mining engineers)的接收數額只有2個,地質工程師(Geological engineers)的
            接收數額只有16個,石油業工程師(Petroleum engineers)的接收數額竟然只有1個。
            採礦,地質和石油工程師這都是原來老38類緊缺職業中的熱點,現在竟淪落至此。航天工程師
            (Aerospace engineers)的接收數額只有6個。 今年和醫學相關的上榜專業仍然很多,
            但申請較去年冷落。到9月12日,物理治療師(Physiotherapists)接收了103個,這是
            屬於一個「常青樹」的專業,無論是38類,29類還是目前的緊缺職業,該類別總是榜上有名。
            職業治療師(Occupational Therapists)接收了14個,醫學實驗室技術專家
            (Medical laboratory technologists)接收了79個,醫學實驗室技術員或病理學助理
            (Medical laboratory technicians and pathologists’ assistants)接收了
            23個,呼吸診斷師,臨床機器操作師,心肺技術專家(Respiratory therapists, clini
            cal perfusionists and cardiopulmonary technologists)接收了4個,放射醫療
            儀器專家(Medical radiation technologists)接收了15個,這又是一個屬於「常青
            樹」的專業。醫療超聲檢查技師(Medical sonographers)接收了8個;心臟病儀器操作
            技工和電生理診斷專家(Cardiology technicians and electrophy
            siological diagnostic technologists, n.e.c. (not else
            where classified)接收了6個;聽覺和語言類病患矯治專家
            (Audiologists and speech-language pathologists)接收了3個。 是甚麼原因
            造成初期的預計和實際情況的差異呢?「加拿大庫先生移民事務所」分析應該是以下三個
            原因: (1)很多申請人英語能力不平衡而導致無資格申請。今年設定的最低英語標準是雅思
            成績聽說讀寫這四個單項都必須高於6.0分,有些申請人聽說讀寫這四個單項能力不均衡。
            比如:有的申請人,雅思綜合評分能達到6.5分,但總有一個單項低於6.0分,這樣就沒有資格
            遞交申請; (2)申請要求的文件更加繁瑣,使有些申請人放棄申請。今年要求所有學歷必須
            通過加拿大認證機構的認證,這一認證程序相當複雜。比如:有些在美國的申請人,在國內讀
            的本科,那麼國內本科學位認證首先必須在國內通過清華認證後,再到加拿大指定的認證機構
            認證,很多申請人因為人在境外,認為認證程序太過繁瑣而放棄申請; (3)申請人對個人職業
            定位不太清晰,而放棄申請。比如:有位申請人是從事塑料材料開發的工程師,他一直對自己的
            職業定位比較模糊,自己是屬於材料工程師呢,還是化學工程師呢?後來他到我們事務所諮詢,
            我們對照加拿大職業大典關於化學工程師的描述,同時職業大典上也明確指明塑料工程師
            (Plastic Engineer)是屬於化學工程師這個大類的一個小的分類,這樣他才決定以化學
            工程師來申請。這樣的例子還有很多,比如:很多從事醫學臨床或者研究的申請人,在他們
            真正從事臨床或者研究工作之前,或多或少從事過醫學實驗室的工作,以他們過去在醫學
            實驗室的工作經歷就完全可以考慮以醫學實驗室技術專家或者醫學實驗室技術員這兩個類別
            來申請。 對符合申請條件的申請人來說,即便現在開始準備申請也為時未晚。但當務之急
            要做的三件事情是: (I) 盡早報名參加最近的雅思考試並獲得必要的成績; (II) 盡早
            開始準備申請文件(建議在獲得雅思考試成績之前就開始準備文件); (III) 在雅思成績
            出來後,其他文件已經準備好,儘快在第一時間遞交完整的移民申請文件到移民局。退一步說,
            即便今年的配額趕不上,明年還有機會。其實很多今年趕上配額的申請人,也都是去年甚至
            前年錯失機會後,提前做了準備,而趕上今年的配額的。 如果您希望瞭解加拿大最新移民
            政策,請隨時瀏覽「加拿大庫先生移民事務所」的專業移民網站,
            如果您有移民的想法希望得到我們的幫助,請隨時撥打諮詢電話:1-519-9678017,或者將
            您的個人簡歷和要求發至Email郵箱: info@ku-immigration.com,我們將及時幫助您
            圓加拿大移民之夢。
            '''
        ),
    )
    assert parsed_news.category == '北美新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1379692800
    assert parsed_news.reporter is None
    assert parsed_news.title == '加拿大2013~14年度聯邦技術移民 配額使用之分析'
    assert parsed_news.url_pattern == '13-9-21-3969060'
