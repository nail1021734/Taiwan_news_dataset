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
    url = r'https://www.epochtimes.com/b5/19/10/16/n11592972.htm'
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
            移民體檢(Immigration Medical Examination)是移民美國必須經過的一道程序。根據
            美國移民法,要申請綠卡,必須通過移民體檢,而且做移民體檢的醫生(civil surgeons)
            必須是移民局批准認證的醫生,移民局才會承認體檢結果。 移民體檢都要檢查哪些內容?哪些
            類型的疾病會影響移民申請?紐約家庭醫生郭曉軍就移民體檢相關問題作了詳細解答。 Q:
            移民體檢檢查哪些疾病? 郭曉軍:移民體檢的主要目的是從公共健康角度,篩查不符合移民條件
            的申請人。體檢內容包括「疾病」和「預防接種」兩個部分。 疾病包括對公共健康有危害的
            傳染病,比如結核病、梅毒、淋病、麻風病、可能造成傷害的生理或精神行為疾病,以及毒品
            濫用或成癮。 預防接種是根據不同年齡段,檢查是否已經接受過所需的疫苗。 Q:做結核病
            測試,應該選哪種方法? 郭曉軍:在需要檢查的傳染病中,結核病目前有幾種不同的測試方法
            。我們一般做的抽血試驗有兩種。以前要想做傳統的PPD也可以,但是自2018年起已不再接受
            PPD皮試。 抽血檢驗的方法有很多優點,相對來說更準確,敏感性和特異性比較好。敏感性
            就是病人如果有病是否能夠檢測出來,特異性就是病人如果沒病就會呈陰性。 如果抽血結果
            呈陽性,那麼患者就要接受X光檢查,如果有活動性病灶就要接受治療。如果沒有活動性病灶就
            按潛伏性結核處理就可以了。 Q:不同年齡的人,體檢項目不同? 郭曉軍:移民局對不同年齡
            申請人的體檢內容有不同的要求。比如前面提到的結核病檢測適用於2歲以上的移民,2歲以下
            的一般不要求,不過如果有證據顯示孩子接觸過患者或其它原因也會測試。 另外,小孩子感染
            梅毒的機會比較少,一般15歲以上才需要檢測,淋病也是針對15歲以上的人群。當然,如果有
            證據或其它原因,需要的話醫生也會檢測。 Q:需要哪些疫苗記錄? 郭曉軍:移民體檢還要看
            你的免疫狀態。移民法要求申請人需要有十幾個疫苗記錄,包括:百日咳、破傷風和白喉、脊髓
            灰質炎、風疹、麻疹、腮腺炎、流行性腦炎、流感嗜血桿菌、乙肝、甲肝、水痘、肺炎、輪狀
            病毒、流感疫苗等等。這些疫苗在某些年齡段要求有所不同,並不是所有的疫苗都要接種
            。 如果你在出國之前已經把疫苗打完了(有免疫記錄為證),或者抽血檢查發現你已經有足夠
            的免疫力,這兩種情況都可以證明自己不需要再打多餘的疫苗了。比如麻疹、風疹、腮腺炎、
            水痘、乙肝等,通過驗血都能證明抗體的存在,只要抗體有足夠數量,符合要求就行了。 如果
            患者對某些疫苗過敏,可以不打。在打之前醫生會介紹打的疫苗都是預防哪些疾病的。如果
            打出什麼問題,每支疫苗上都有索賠電話。從統計學看,注射疫苗的好處大於壞處。 Q:移民局
            對體檢表有何要求? 郭曉軍:體檢表(Form I-693)填好後,醫生會把表格用信封封好,由申請
            人轉交移民局。如果移民局收到的信封沒有封好,或被打開了,或有修改的痕跡,將被視為無效
            證明。體檢表要在表格填好後的60天之內遞交給移民局,有效期是兩年。 Q:健康記錄作假會
            怎樣? 郭曉軍:申請人需要如實回答健康情況。比如體檢詢問是否有精神類疾病(如精神
            分裂症),患者一定要如實提供個人的健康狀況,如果不如實提供,有了不良記錄會影響移民
            。 大多數人或多或少會有一些健康問題,但都在可接受的範圍,有病去治療就可以了,所以
            不必過分擔心、故意隱瞞。 有一點要說明,即使移民申請人有身體或精神上的疾病,移民局
            不會因此判斷你是否適合移民,因此拒絕你的移民請求。移民局會根據體檢結果判斷這些疾病
            會不會對你自己或別人及其財務造成傷害。如果有潛在傷害的話,有可能會被認為不適合移民
            。 如果檢查結果說明你有某些方面的問題,醫生會提出合適的治療或轉診計劃,另外,移民局
            也會通知你是否需要申請一個豁免,移民局有具體的豁免條例。
            '''
        ),
    )
    assert parsed_news.category == '生活,健康1+1,醫療熱點'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1571155200
    assert parsed_news.reporter is None
    assert parsed_news.title == '哪些疾病影響移民美國?6QA看懂移民體檢'
    assert parsed_news.url_pattern == '19-10-16-11592972'
