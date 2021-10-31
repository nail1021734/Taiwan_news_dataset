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
    url = r'https://www.epochtimes.com/b5/13/2/10/n3798072.htm'
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
            2013 Santa Fe是Hyundai旗下中型SUV的第三代產品。這個有著熱銷歷史的經典車型,在
            設計上卻不斷地進行大膽的改變。除了車標那個詼諧的「H」以外,在新 Santa Fe身上已經
            很難找到前兩代Santa Fe的蹤影,顯示出Hyundai快速發展的活力與面對市場的強大
            自信。 2013 Santa Fe 外觀設計成功引申了Hyundai獨特的設計語言。在流體雕
            塑概念中又添加了「風暴邊沿」的設計元素,使原本飄逸流動的線條變得鋒利敏銳。顯示了
            SUV區別於轎車的強悍和堅韌。整個外觀造型,就好像偶然抓住的一個瞬間即逝的完美閃現,
            這種動態的美只有當時間完全靜止下來後我們才能靜靜的欣賞。前大燈的設計令人印象深
            刻,如日光燈一樣的白色燈眉像兩道閃電。由於光的顏色的變化,使前燈看上去醒目而又新
            穎。 此次試駕的車型是5座標準型(Hyundai還將推出7座加長型),車身長度較之前的型號略
            有增加。由於新型高強度材料的成功應用,新一代Santa Fe在結構和安全指標提高的同時,
            重量較上一代減輕121公斤。這樣的重量變化對整車性能特別是經濟性的貢獻不言而寓。事
            實上,在試駕期間該車的平均油耗約為百公里11升,就如此一款承擔家庭重任的四驅車來說,
            這樣的經濟性表現給我留下了相當清晰的良好印象。 2013 Hyundai Santa Fe的內飾在視
            覺上很超前,中控台採用多邊形的組合,恍若翱翔星際的太空船。裝飾材料的質感與這款車
            的定位非常匹配,做工精細。採用三輻式方向盤,兩側的功能鍵幾乎囊括了除空調系統以外
            的大部份功能。雙筒形儀錶盤採用悠藍的背光照明,散發著太空深邃的神秘感。此外,陡坡
            緩降系統、車身穩定系統、電子手剎、一鍵啟動系統、ECO節能模式、柔性轉向系統等多項
            功能,使這款車跟上了當今汽車新技術應用的潮流。 第三代Santa Fe,可裝載兩款汽油發動
            機,即2.4升直列4缸和2.0升直列4缸渦輪增壓發動機。此次的試駕車裝載2.4升GDi發動機,
            最大輸出功率為189匹馬力,最大扭矩為181磅呎。配備6段手自一體變速箱。作為一款家庭
            用車,人們不會對其動力性能過於苛求。而這台2.4升的引擎所產生的動力足以驅動4個車輪
            跨越市郊任何可能的泥濘路面,不會有絲毫的猶豫。特別是穿越顛簸路面時優異的通過性,
            會使駕駛者面對任何陌生道路無所畏懼。 作為一款城市SUV,2013 Santa Fe華麗的內外裝
            飾已經充分到位。但是當你有膽開著這部車離開柏油路面的時候,你就會知道這不僅僅是一
            部好看的車。
            '''
        ),
    )
    assert parsed_news.category == '科技新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1360425600
    assert parsed_news.reporter == '夏又容'
    assert parsed_news.title == '秀外慧中 Hyundai Santa Fe AWD'
    assert parsed_news.url_pattern == '13-2-10-3798072'
