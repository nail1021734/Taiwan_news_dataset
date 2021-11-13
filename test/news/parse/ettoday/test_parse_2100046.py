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
    url = r'https://star.ettoday.net/news/2100046'
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
            2022年縣市長大選時間逐漸接近,民進黨高雄市長陳其邁準備尋求連任,在外界點名的
            挑戰者中,包括國民黨籍的前高雄市副市長李四川、孫文學校總校長張亞中,以及
            台北市長柯文哲,根據《ETtoday東森新媒體》最新民調顯示,陳其邁的支持度目前
            仍處於領先的優勢,即使面對傳聞中的參選人,陳其邁都以超過五成的支持率,狠甩國民黨的
            張亞中、李四川。 本次民調由《ETtoday東森新媒體》民調中心,負責問卷設計、調查執行
            、資料處理、統計分析及報告撰寫。調查期間於2021年10月5日至7日進行,調查方法為EDM
            網路調查,以高雄市年滿19歲以上民眾為調查範圍及對象;調查回收有效樣本數為2,317份,
            抽樣誤差在95%信心水準下,為正負2.04%。 《ETtoday東森新媒體》民調中心表示,在
            進行統計分析之前,原始資料先依高雄市政府民政局最新人口統計資料(110年9月底)進行
            性別、年齡、地區、教育程度樣本加權,以符合高雄市19歲以上人口之母體結構,使調查具有
            代表性。 根據《ETtoday東森新媒體》民調中心調查顯示,如果陳其邁與李四川、張亞中、
            柯文哲兩兩PK,陳其邁均處於領先的優勢,三組PK對戰的結果為陳其邁54.0%:李四川32.5%,
            支持度差距21.5%;陳其邁56.2%:張亞中23.7%,支持度差距32.5%;陳其邁50.7%:柯文哲
            31.0%,支持度差距19.7%。 進一步交叉分析後發現,在三人戰局下,國民黨李四川以年齡
            40歲及以上、政黨傾向為國民黨、泛藍之族群支持度較高;台灣民眾黨柯文哲支持度較高
            之族群則以年齡39歲及以下、政黨傾向為台灣民眾黨、不支持任何政黨之中間選民為主
            。 值得注意的是,在今年九月底的國民黨主席選舉中,受到矚目的張亞中雖然未能擊敗
            朱立倫,但已在各地囊括3成以上選票。根據開票結果顯示,高雄市部分,朱立倫得9992票,
            得票率41.7%;張亞中得9221票,得票率38.48%。張亞中的得票率只輸給朱立倫3.22%
            。有藍營人士分析,以張亞中的得票率,有望續攻6都地方縣市首長,有機會成為一名活棋
            。 不過,根據《ETtoday東森新媒體》民調中心調查結果顯示指出,國民黨若派出張亞中,
            對上民進黨陳其邁、民眾黨柯文哲競爭2022高雄市長,陳其邁仍獲48.7%支持度領先,
            柯文哲24.5%、張亞中15.5%;其中張亞中下滑幅度最大,支持度由23.7%下滑至15.5%,
            減少8.2%;柯文哲支持度由31.0%下滑至24.5%,減少6.5%;陳其邁下滑幅度最小。 若
            國民黨派出李四川,對上台灣民眾黨柯文哲與民進黨陳其邁三人競逐2022高雄市長,陳其邁
            以48%的支持度領先,李四川24.2%、柯文哲19.1%;其中柯文哲下滑幅度最大,支持度
            由31.0%下滑至19.1%,減少11.9%;李四川支持度由32.5%下滑至24.2%,減少8.3%;陳其邁
            下滑幅度最小。 在進一步交叉分析後發現,在三人戰局下,台灣民眾黨柯文哲支持度較高
            之族群以年齡49歲及以下、政黨傾向台灣民眾黨、泛藍、不支持任何政黨之中間選民為主;
            國民黨張亞中則以年齡50歲及以上、政黨傾向為國民黨的族群支持度較高。
            '''
        ),
    )
    assert parsed_news.category == '政治'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634099640
    assert parsed_news.reporter is None
    assert parsed_news.title == '2022高雄市長 陳其邁56.2%狠甩張亞中、領先李四川21.5%'
    assert parsed_news.url_pattern == '2100046'
