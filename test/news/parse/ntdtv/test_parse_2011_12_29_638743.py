import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.ntdtv
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/12/29/a638743.html'
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
            日前,中國奶製品大生產廠商蒙牛的液體乳產品被檢出強烈致癌物質黃麴黴毒素M1超標140%。
            有關消息傳來,使中國食品安全問題再蒙上一層陰影。 用來調侃的笑料 蒙牛的官方網站的
            口號是:「蒙牛——致力於人類健康的牛奶製造服務商。」在蒙牛最新的醜聞傳來之際,這一
            口號對蒙牛構成刺眼又刺耳的反諷。蒙牛由此自然而然地成為中國網民用來調侃的
            笑料。 或許是受到中國網民的感染,或許是心同此理,英國《金融時報》記者西蒙•拉賓諾維奇
            在28日​​發表的博文,也是明顯的調侃口氣: 「就飲料而言,普通的牛奶是有益健康的,也是
            無聊乏味的。那些對普通牛奶感到厭倦的人不妨品嚐一下中國的牛奶。中國牛奶摻有可以
            摧毀腎臟的毒素,有害的細菌和致癌物質,因此絕對不是平淡無奇。喝中國牛奶是一種高風險
            活動。」 毒奶與社會、經濟和政治 《華爾街日報》網站28日發表記者勞裡•伯基特的
            博文,對蒙牛最新的危機所引起的中國社會、經濟和政治動態進行了一番如此這般的
            解說: 「中國最時興的詛咒人的話是什麼?是’我希望你全家喝蒙牛。這句話如今在中國
            網際網路上四處流傳。大批消費者在中國的新浪微博上批評蒙牛。最近中國政府產品質量
            安全檢查部門發現蒙牛的一些奶製品含有致癌物質。」 「儘管蒙牛對消費者表示了道歉,
            並聲明有毒產品已經銷毀,沒有上市,但蒙牛面臨嚴重的公關危機。在中國這個大眾沒有
            多少表達渠道的國家,對蒙牛的批評傳播速度之快,批評聲音之猛烈,讓人再次看到新浪
            微博以及其他社交媒體對產品品牌的生死影響力。」 澳大利亞主要報紙《悉尼先驅晨報》
            28日有關蒙牛最新醜聞的報導,則給讀者提供了另一種中國政治經濟學素描,讓人無法笑
            起來: 「中國人對食品安全醜聞,尤其是涉及牛奶的醜聞憂心忡忡。在2008年,中國奶製品
            摻有有毒化學物三聚氰胺,導致6名兒童死亡,30多萬生病。中國共產黨對那些要求進行調查
            的受害兒童家長進行了鎮壓。」 法新社26日發表的報導,提供了中國出產蒙牛毒牛奶的
            大背景: 「中國常常出現重大的食品安全醜聞。近幾個月來披露出來的有地溝油,有害物質
            染色的雞蛋,致癌黴菌,違禁的豆醬,假酒。招致最強烈反響的是三聚氰胺奶粉在2008年導致
            6名兒童死亡,30萬受害。」 「鄭重致歉」的公信力 蒙牛最新的醜聞也使它在股市上遭受
            重大損失。美國彭博通訊社12月28日發表報導說: 「中國最大的奶製品生產廠商蒙牛在
            香港股市股價下跌,跌幅為三年來最大。早些時候,該公司承認用霉變的飼料餵奶牛,導致
            生產的牛奶中含有過量的毒素。在28日收市的時候,蒙牛股價在香港下跌百分之二十四,
            跌至20港元。其跌幅是2008年以來最大的。」 「股價下跌,導致蒙牛市值蒸發110億港元。
            這反映出投資者對中國食品安全醜聞的擔心。這類醜聞包括摻有三聚氰胺嬰兒奶粉在2008年
            導致至少6名嬰兒死亡,以及今年豬肉摻非法的添加劑。蒙牛28日表示,將加強質量控制措施,
            有毒素的奶製品已經銷毀。」 在其產品黃麴黴毒素M1檢測結果超標的消息披露之後,蒙牛
            集團迅速通過其官方網站向全國消費者表示「鄭重致歉」,並強調「產品未流入市場」、
            「立即對該批次全部產品進行了封存和銷毀」。 在2008年中國全國性的三聚氰胺毒奶粉
            醜聞中,蒙牛也有牽連。蒙牛當時也跟其他奶製品廠家一樣做出了鄭重的道歉,並表示要加強
            產品質量安全檢查措施。現在不清楚蒙牛這次「鄭重致歉」到底會有多少公信力。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325088000
    assert parsed_news.reporter is None
    assert parsed_news.title == '世界媒體看中國:特色奶製品'
    assert parsed_news.url_pattern == '2011-12-29-638743'
