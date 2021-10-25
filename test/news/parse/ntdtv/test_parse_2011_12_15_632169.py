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
    url = r'https://www.ntdtv.com/b5/2011/12/15/a632169.html'
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
            中國正式加入世界貿易組織WTO今年邁入第十年,過去美中兩國貿易糾紛不斷,美國向世貿
            組織指控中國涉嫌違反世貿規則項目多達12項。12號,美國貿易代表辦公室提交給國會的
            年度報告說,中國到現在沒有完全遵守基本自由市場原則,不少國會議員甚至對中國入世的
            好處持懷疑態度。 中國花了15年的時間才正式加入世界貿易組織,25年來,北京政府雖然在
            市場准入、降低關稅、知識產權保護等方面作了一系列法規修訂和承諾。不過,美國貿易
            代表處在年度報告中指出,中國廣泛實施干預政策,使用歧視性的監管程序、和非正式的禁止
            入境等種種手段,嚴重影響美國企業的利益。 不過美國一些國會議員認為,美國對華貿易的
            巨額赤字,導致美國製造業數以百萬工人失業。 《新唐人》時事評論員文昭表示,由於中共
            政府是個集權專制國家,他能夠做一些民主國家做不到的事情,如壓低勞動力成本、原料成本,
            使產品出口具有廉價的優勢,然後傾銷到歐美國家。 文昭:「中國的廉價商品銷售到美國
            以後,使美國的消費者,北美的消費者買到了便宜貨,這看起來也許是有一些好處。但與此同時
            呢,它也使得製造業一些國家衰落,增加了失業率。」 中國「入世」後,出口規模迅速擴大,
            從2001年佔世界的4.3%,居全球第六位,到2010年的10.4%,位居世界第一位。美國貿易
            代表處的報告認為,只有中國在完全遵守世貿基本規則的前提下,才能保障全球經濟體系的
            平衡發展。 中國通過貿易賺到了大量的外匯,但他並有拿來購買別的國家商品,帶動歐美
            國家經濟復甦。 文昭:「那麼他是用這些儲備外匯去購買鉅額美債,當他成為美債主要持有人
            之後,他就利用這些法碼去要脅美國政府。」 美國「南卡羅萊納大學」艾肯商學院教授謝田
            表示,美國政府比較不滿的是:中國操縱匯率和知識產權問題。 謝田:「就我們現在看的
            報導,中共從來就沒有想說遵守他的承諾,對中國來說加入世貿組織以後呢,他的出口對西方
            美國出口大幅的增加,他用這辦法來帶動就業,推動經濟,創造就業機會,促進中國周圍都是增
            工廠的發展,賺取大量的外匯。」 謝田表示,中國大量的外匯儲備都是從美國貿易得到的,
            卻擊垮了美國的製造業,造成美國失業率上升,這是美國老百姓所不願接受的。中國在自由
            貿易中破壞了市場機制,受到西方國家的反彈也是必然的。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1323878400
    assert parsed_news.reporter == '易如,李庭,朱娣'
    assert parsed_news.title == '美報告:中共違反世貿規則'
    assert parsed_news.url_pattern == '2011-12-15-632169'
