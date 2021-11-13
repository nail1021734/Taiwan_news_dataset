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
    url = r'https://star.ettoday.net/news/2100081'
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
            在9月於自家主場-德國舉行的
            2021 IAA MOBILITY(International Motor Show Germany)車展上,
            BMW Motorrad向世人介紹旗下全新的電動摩托車概念車款「Concept CE 02」。
            根據消息指出,這是一輛有著約15ps最大馬力、最高時速90km/h,續航里程達90km的
            電動摩托車,同時具備智慧型操控系統,相當適合都市間的電動通勤代步使用。 歐洲最入門
            的A1駕照就能騎乘! 來自BMW Motorrad德式思考思維的俏皮概念車款到貨了!
            Concept CE 02的設計概念,就是希望能提供宛如兩輪滑板般的自由、無拘無束,因此
            每個零件都採用BMW Motorrad的創新技術。 CE 02的車身設計扁平且低重心,馬達
            安裝在車身後方而非後輪,動力則由皮帶傳遞至後輪。兩顆電池模組被塗黑、跟驅動相關的
            零件則集中安裝在銀色區域,搭配上平板式座椅與車架、單搖臂、倒立式前叉、側置單槍後
            避震等,組合出有點像檔車,卻又帶點滑板元素的新穎想法。 頭燈由四顆LED組合成正方形
            造型、車尾則由坐墊 兩側邊緣的半透明鏡片搭配LED燈組作為尾燈使用。把手底座安裝
            有一個彩色儀表板,可以顯示電量、速度,根據圖片中的顯示推測,應該也有能與智慧型手機
            連接的功能。 由於BMW Motorrad對其規格細節僅透漏最大馬力約15ps、車重約120kg、
            最高時速90km/h、WMTC續航距離約90km,至於硬體規格僅確定採用15吋輪框,其餘包含
            車架、懸吊系統等皆無過多解釋。 話說,雖然仔細觀察細節會覺得不像,但整體的俏皮感、
            玩樂氛圍與車身尺寸,都會讓人聯想到HONDA的GROM或MONKEY,看的出來BMW Motorrad
            也對入手門檻低、改裝空間大的小型車市場,逐漸展現出興趣與企圖心。
            '''
        ),
    )
    assert parsed_news.category == '車'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634223240
    assert parsed_news.reporter is None
    assert parsed_news.title == 'BMW「都市代步電動機車」擁15匹馬力 外型像MONKEY、改裝潛力大'
    assert parsed_news.url_pattern == '2100081'
