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
    url = r'https://www.epochtimes.com/b5/13/3/11/n3819681.htm'
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
            在朝鮮這樣的獨裁國家,宣傳機器往往將國家領導人吹捧的像神一樣偉大,受到百姓的感恩
            戴德。朝鮮媒體近日公開的一段宣傳影片顯示,該國領導人金正恩在視察部隊後登船離去時,
            成批的官兵跳入海中揮手相送,場面驚人,堪稱其「造神運動」的又一項創舉。 宣傳影片
            塑造領導人的地位 3月7日,金正恩率親信視察了位於西海前線地區的長檯島防禦隊和舞島
            英雄防禦隊。從朝鮮中央電視台公佈的這段影片可以看到,在金正恩搭船抵達時,當地官兵與
            眷屬雙手同舉、歡呼跳躍,似乎十分興奮,有人甚至「喜極而泣」。 金正恩在島上視察設施
            與防務之後,準備搭船離去。此時,站在海邊歡送的大批官兵突然衝進冰冷的海水裡,不斷地
            揮舞著雙手並高呼「萬歲」,儘管金正恩揮手示意要官兵回到岸上,但他們還是堅持大半身泡
            在水裡,不停地揮手,一直目送金正恩離去。 對於民主國家的民眾而言,這種畫面可謂
            不可思議,難怪CNN女主播在播報這段新聞時,會口出「我的天啊!」這樣的感嘆詞,同時稱
            朝鮮官兵的這種舉動為「瘋狂」。 朝鮮核武威脅世界和平 朝鮮於2月12日進行第三次
            核試驗,遭國際社會強烈譴責。對此,聯合國安理會於3月7日一致通過對朝鮮採取新的制裁
            措施,包括進一步限制進出朝鮮的貨運、加強控制與武器相關的資金移轉等。 針對朝鮮的
            軍事威脅,美國與韓國定於3月11日至21日舉行代號為「關鍵決斷」(Key Resolve)的
            聯合軍演作為因應。朝鮮以此為藉口接連宣佈廢除停戰協定、南北互不侵犯協議和無核化
            聯合宣言等,聲稱已做好全面戰鬥的準備,同時對美韓兩國發出導彈威脅。 朝鮮於3月6日
            透過其黨營媒體《勞動新聞》揚言,將使用世界上無人知曉的精密核打擊手段,使首爾和
            華盛頓變成火海。韓國《朝鮮日報》引述一名軍方消息人士的話說,朝鮮所謂無人知曉的
            精密核打擊手段,可能是指採用小型核彈頭的電磁脈衝彈(EMP)或利用移動式發射架發射的
            洲際彈道導彈(ICBM)。 《朝鮮日報》報導說,電磁脈衝彈是利用強大的電磁波使特定地區
            電網、通信網和電子設備癱瘓的武器。這種武器是未來戰爭的主力,可使雷達、飛機、防空
            系統、使用電腦的指揮控制系統等發生癱瘓。 報導引述美國中央情報局(CIA)一名核
            專家說,開發電磁脈衝彈的俄羅斯科學家表示,這種武器的設計情報被洩露給朝鮮。俄羅斯
            科學家在2004年曾說,朝鮮可能在幾年內開發出超級電磁脈衝彈。 專家預測,如果電磁
            脈衝彈在電網密佈、電子設備眾多的韓國或美國上空爆炸,將會造成嚴重衝擊。 窮兵
            黷武 民不聊生 朝鮮將龐大金額用於發射火箭與核試爆等軍事方面,卻罔顧人民的生活。近有
            媒體披露,成千上萬朝鮮人飽受饑荒所苦,已出現人吃人的現象。 據英國《每日郵報》引述
            亞洲新聞社(Asia Press)的報導稱,在黄海南道(South Hwanghae)和黄海北道
            (Nouth Hwanghae)等農業省份,由於旱災導致食物短缺,而且農作物被官員沒收並轉交
            平壤居民,當地民眾沒有食物可吃,據信有高達1萬人餓死,還有父食子肉的悲劇發生。 報導
            說,朝鮮在90年代曾發生大饑荒,死亡人數介於24萬至350萬人之間。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1362931200
    assert parsed_news.reporter == '陳俊村,畢儒宗'
    assert parsed_news.title == '驚人畫面:朝鮮官兵跳海歡送金正恩'
    assert parsed_news.url_pattern == '13-3-11-3819681'
