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
    url = r'https://www.epochtimes.com/b5/12/12/28/n3763175.htm'
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
            我們中的大多數人都不大可能持續開一部車達到一百萬公里,因為我們大多數人駕駛
            汽車每年行駛約25000公里,。但專家一致認為,持續進行基本保養能幫助你延長汽車
            行駛里程達320,000公里,甚至更多。 閱讀您的用戶手冊 – 遵守它的指導 Joe 馬利
            茲,貝爾航空快速潤滑油公司在馬里蘭州的所有者,告誡說一旦買了新車,你可以做的
            最好的事情就是認真閱讀車主手冊,找到汽車維修時間表,因為根據建議的維修時間表
            保養汽車可以大大延長汽車的使用壽命。就像是需要每隔幾個月訪問您的機械師一
            樣,有的人會感歎為建議的汽油價格都較高。但這些簡單的方法,可以防止不必要的
            問題,導致你的車過早報廢。 NPR的汽車講座的技術顧問——約翰‧勞勒同意以上觀點,
            他說:「世界上至少應該讀的書就是使用說明書。」他補充說,不光保持機油和水很重
            要,保持輪胎適當充氣以達到使用說明書要求的規格,是保持你的車在路上正常行駛的
            另一個重要因素。雖然定期找技師保養汽車的費用看起來可能會增加很多,但你能省
            下很多在道路上支付的昂貴維修費。像勞勒說的,「誰花錢最多誰最能省錢。」 關
            注你的車 除非你是個修理工,你可能不會知道如何改變你的火花塞,或者是使你的
            電子穩定控制系統出毛病的原因,但掌握如何檢查機油位置的基本知識,並重視體察
            開車時的非正常現象,可以節省您在路上可能的大修理費,馬利茲和勞勒都這樣
            說。 馬利茲也說,注意你的警示燈也是非常重要的。車輛監控系統的設置是有原因
            的,它可以
            更好地扼殺在萌芽狀態的問題,而不是讓它升級到災難性的地步,從而保證你的車可以
            達到20萬公里大關。 勞勒說,最重要的事情之一是保持車內清潔。簡單的東西,如
            鳥糞,酸雨或SAP都會損壞汽車的塗料。給你的汽車塗上了一層蠟會防止損壞油漆,
            因為它可以防止金屬生銹。此外,應該確保車內清潔。座位或設備上的污垢可以像
            砂紙一樣,每次你觸摸它時都會造成表面磨損。 尋找可信任的汽車技師 馬利茲說,找到
            一個您信賴的技師是確保你的車能長途運行的最佳途徑之一。我們都聽到過有關為
            虛構的「信號燈液」向不知情的客戶收費,或去解決一個問題時卻找到了15個問題的
            恐怖故事。但是,大多數技術人員是誠實可靠的,跟你信任的技師建立良好的關係將幫
            助你的車衝過行駛20萬英里的大關。 勞勒建議去經銷商處保養最新款的車,尤其是
            如果它們還在保修期內。汽車的車型越新,結構更複雜,很可能的情況是,經銷商技術
            人員進行過具體的培訓,他們會非常了解你的車。雖然經銷商很可能更值得你為新款
            車支付保養費,但勞勒說,如果你的車款是十年前的,你最好送到當地傳統的維修店去
            保養。他們會更了解車的基本情況,可以進行基本的保養如更換剎車片,而且大多數
            不會向您收取像經銷商那麼多的錢。 無論你如何精心照顧你的車,事故是必然要發生
            的,機械故障可能超出你的控制。妥善維護你的車能使它行駛的公里數更多,並在你
            出售時會得到更高的價格。例如喬馬利茲的車:「在他的店裡看到的最高里程車是他
            自己的1993年的福特金牛SHO,在跑了19年,238,000英里後依然性能優越。
            '''
        ),
    )
    assert parsed_news.category == '科技新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1356624000
    assert parsed_news.reporter == '馮閱多伦多'
    assert parsed_news.title == '如何讓車運行超過30萬公里'
    assert parsed_news.url_pattern == '12-12-28-3763175'
