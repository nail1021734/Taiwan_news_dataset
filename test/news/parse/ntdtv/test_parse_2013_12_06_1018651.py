import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2013/12/06/a1018651.html'
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
            美國副總統拜登到中國訪問,同習近平主席談到了中國設立的防空識別區問題。從美國
            到日本再到中國都對此問題有若干表述的拜登,也同習近平談到了這個數方都非常關心
            的問題,但是,中方的回應只有一句話。 拜登重申:美國不承認中國空識區 當地時間星期三
            早些時候抵達北京的拜登,晚些時候在人民大會堂同習近平會談了五個半小時
            (包括晚餐時間)。拜登隨行官員後來説,雙方談到了防空識別區問題。該官員
            説:「副總統詳盡談到我方在此問題上的立場,並表明:美方不承認該空識區
            (He indicated that we don’t recognize the zone)。」 中國在上周宣佈設立
            東海防空識別區,引起日、韓等周邊國家和太平洋相關國家的嚴重關注。 拜登副總統訪華
            隨行官員説,拜登對習近平説:「我們希望中國能採取步驟減輕地區緊張局勢。」隨團訪華
            的記者援引這位沒透露姓名的官員的話説:習近平主席聽取了拜登的意見。他還説,現在
            球在中方一邊,「我們拭目以待,看未來幾天或一段時期內事情將如何發展。」 中媒:習近平
            對拜登「重申」在識別區的「原則立場」 拜登和習近平會談幾個小時後,中國新華社發出
            「通稿」,人民日報、中新社、環球時報等各媒體紛紛「轉載」。這篇新華社記者「錢彤、
            郝亞琳」合寫的總共7段的報道,談到這個問題只有一句話:「習近平重申了中方在台灣問題
            、涉藏問題及劃設東海防空識別區等問題上的原則立場。」 星期四,外交部發言人洪磊在
            記者會上談到這個問題時,也只説了一句話:「中方在會談中重申了原則立場,強調中國此舉
            符合國際法和國際慣例,美方應採取客觀、公允的態度予以尊重。」 星期四,拜登同中國
            總理李克強舉行會談。此前,有美國媒體報道説,預計空識區「將是主要議題」。但是,
            新華社在拜登/李克強會談後發出的相關報道有五段,其中前三段是李克強的講話,後兩段
            是拜登的講話,報道沒有提到雙方談到了東海空識區的問題。 中國日報:拜登有關識別區
            講話錯誤多多 星期三,中國最大的英文報紙中國日報發表一篇社評説:拜登在日本一些
            有關釣魚島爭議的講話,偏袒一方,錯誤多多。社評説,中國只是對日本的挑釁加以回應
            。 該社評還説,拜登星期二在日本説,有必要就空識區問題建立危機管理機制。該報還援引
            拜登話説:誤判和犯錯誤的機率非常高。社評説:拜登此話「非常正確」。 中國日報社評
            還説:拜登來中國,應認真聽取中方的説法。「我國領導人應切實做到,讓美國客人離開中國
            時,已經對東海爭端的『因果關係』有了更加清晰的了解。」 拜登訪華會見習近平,有歐洲
            電臺説:拜登訪華碰壁 中國無意讓步。這個電臺的網站説,「在引起爭議的東海防空識別區
            問題上,美國副總統拜登在中國之行中顯然碰了壁。北京在此問題上不願有絲毫讓步
            。」 沈丁立:中美之間有比識別區更重要的事 不過,有中國學者對此判斷並不認同。上海
            復旦大學國際問題研究院副院長沈丁立教授説,中美有比識別區更重要的事情。沈丁立在
            星期四的人民日報海外版頭版發表評論文章(望海樓隨筆)説,中美鬥則兩傷,和則兩利
            。「中國作為負有重要責任的大國,還有廣泛的地區和全球穩定的合作需要深化,有遠比
            識別區更重要的事。」 12月5日,環球時報發表社評題目是:拜登知道不能為日本毀了
            中國行。社評説,拜登在日本時,「圍著他轉的關鍵詞幾乎只有『中國東海防空識別區』
            這一個。但他一到中國,『大概馬上』感到談話空間一下子擴大了很多。『東海訪問區自然
            是焦點之一』,但它只能是『之一』。」 環球時報這篇社評説:雖然美國在中國設防空識別區
            問題上與中國有較大分歧,但「中美大體駕馭了這一分歧,防空識別區的事並未扭轉中美關係
            的基本注意力。」
            '''
        ),
    )
    assert parsed_news.category == '大陸,時政'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1386259200
    assert parsed_news.reporter == '海濤'
    assert parsed_news.title == '拜登一片心 中共只有一句話'
    assert parsed_news.url_pattern == '2013-12-06-1018651'
