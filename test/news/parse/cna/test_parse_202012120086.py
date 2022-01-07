import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/202012120086.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            主計總處預估台灣今年經濟成長率2.54%,專家指出,台灣出口、投資與消費三大力道站穩,
            明年經濟成長率3.83%有望達標,但仍須留意疫情、匯率與資金滿溢造成的市場過熱等3項
            隱憂。 太平洋經濟合作理事會中華民國委員會秘書長邱達生分析,今年雖然爆發疫情,
            但台灣在出口、投資與消費3股力道都有所支撐。 以出口而言,半導體產業得天獨厚,
            受惠於兩大因素:美中科技戰導致中國供應鏈去美化,中國大陸今年對台灣零組件需求強勁;
            再者是遠距商機,資通訊產品出口高幅度成長,美國市場尤為明顯,預期台灣積體電路、
            半導體產業在中長期5到10年仍能維持領先優勢。 邱達生指出,投資部分,因為貿易戰與
            疫情衝擊,很多廠商配合政府的台商回流政策,產線移回台灣後,也支撐固定投資。
            台商產線移回後,台灣未來訂單量會跟出口走勢趨近一致,也提高供應鏈自主性。 另外,
            在消費面,邱達生表示,台灣就業市場表現相較其他國家好很多,民間消費也逐漸走出今年
            3、4月最嚴峻時期的陰霾,主計總處最近上修今年經濟成長率為2.54%,「這個成長率
            完全看不出有任何外部衝擊」,預期未來台灣經濟好轉時,經濟成長率可能由3%或3.5%
            起跳。 不過,在出口訂單一片暢旺、台股屢創新高的同時,專家仍點出3大隱憂。 邱達生
            表示,第一個隱憂是疫情發展,由於台灣半導體零組件、傳產生產產品多為中間財,深受
            國際市場影響,如果疫情沒掌控好,不僅影響全球供應鏈布局,也會影響歐美市場終端
            經濟需求。 第二個因素為匯率,根據中央銀行統計,新台幣今年以來對美元升值幅度約
            5.61%。邱達生表示,雖然新台幣升勢對高科技產品出口沒有太大影響,但是其他產業廠商
            還是會擔心匯率走勢,以及匯損因素影響獲利。 台灣利率來到歷史低點,資金滿溢造成的
            金融市場過熱現象,則是第三個隱憂。中研院經濟所研究員周雨田分析,台灣雖有基本面支撐,
            但是股市漲幅已經與實體經濟脫鉤,房價也有逐漸上漲的趨勢,必須留意市場資金過多帶來的
            後續問題。 周雨田指出,資金過度流向房市與股市可能加劇貧富不均,因為有錢人更有錢,
            窮困階級則難以參與資本市場、賺取資本利得;另一潛在影響則為金融市場泡沫持續擴大,
            都是必須留意的警訊。 考量低利率、資金滿溢的狀況短期不會改變,引導資金流向成了政府
            重要課題,周雨田建議,政府在財政政策的手段應該大膽一點,除了現有的公共建設計畫,
            可以盤點更多建設項目,續推擴張性財政政策,一方面讓資金有去處、一方面也能增加就業
            機會。 展望明年,邱達生表示,以出口訂單來看,高科技產業仍舊需求強勁,訂單甚至已經
            排到明、後年,傳產則逐漸有谷底反彈的趨勢,雖然還不明顯;政府離岸風電等大型基礎建設、
            產業創新相關領域,也拉抬投資力道;加上台商回流創造就業機會、台股近期屢創新高,
            也都能帶動消費力道。整體而言,明年很有機會達到主計總處經濟成長率3.83%的預測。
            '''
        ),
    )
    assert parsed_news.category == '產經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1607702400
    assert parsed_news.reporter == '蘇思云台北'
    assert parsed_news.title == '台灣錢潮滾滾/專家把脈台灣經濟 正向發展中有隱憂'
    assert parsed_news.url_pattern == '202012120086'
