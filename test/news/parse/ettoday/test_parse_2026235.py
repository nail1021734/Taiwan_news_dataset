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
    url = r'https://star.ettoday.net/news/2026235'
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
            半導體產業具有免疫抗體 根據彭博資訊,今年第二季外資從泰國、菲律賓及
            馬來西亞股市共流出27億美元,創去年第三季以來最大金額,主因就是印尼、菲律賓及泰國
            完整接種完疫苗的比率不到10%,馬來西亞也僅有11%。同樣的情況也出現在台灣,外資六月
            賣超台股510億元,同時也淨匯出達到19.15億美元(約台幣530億元),顯示外資操作邏輯
            具有一致性。一旦外資態度轉變成趨勢,對東南亞股市的大型權值股及指數表現就較為不利
            。 不過,從去年疫情爆發以來就可發現全球各國的封鎖停工等防疫措施,對身為戰略資源的
            半導體多會網開一面,成為少數運作不受疫情影響的產業。以半導體封裝測試及被動元件
            供應為重的馬來西亞,在六月實施的全面行動管制中也是讓當地封測相關企業或產線正常運作
            ,可預期半導體產業有機會成為東南亞股市在疫情威脅預期高漲時的資金避風港,半導體
            為重的台股受影響程度也會相對較輕。 iPhone完整拉貨期為營運掛保證 半導體下半年
            推進營運維持高檔的力量將來自蘋果的新品拉貨潮,相較去年iPhone 12因疫情缺料,延後
            一個月至10月23日才正式上市,實際鋪貨量也低於以往,不少消費者購買需求被迫遞延,導致
            蘋果去年第四季iPhone的銷售額年減高達21%。 預期今年少了斷鏈問題且恢復過去上市
            時程後,蘋果供應鏈出貨成長就是大概率的事,對於半導體產能消化絕對有一定的貢獻。根據
            Wedbush報告顯示,iPhone 13可能於九月第三週亮相,依照蘋果過去於週二舉辦發表會的
            規則推算,iPhone 13應於美國時間9月14日亮相,並在下週的週五(9月24日)正式上市,
            較去年iPhone 12提前整整一個月。 凱基投顧預估今年iPhone整體出貨量將年增
            一四%至二.二八億支,其中iPhone 13出貨量約為8500萬支,較去年iPhone 12出貨量
            8000萬支成長,下半年零組件端備貨量則達9000萬至1億支。儘管iPhone 13的規格
            升級有限,但毫米波機種將大幅增加,下半年出貨量約為5000~6000萬支,較去年同期為
            2000~2500萬支成長逾二倍,同時也會進一步推升因應毫米波用量增加的射頻元件、
            石英元件及電源管理晶片等等元件需求量。預期在第二季的產品過渡期後,七月起供應鏈營
            收動能將恢復。 蘋果產品滲透率持續提高 蘋果晶片代工廠台積電(2330)已開始生產
            iPhone 13用的A15晶片,A15量產將反應在六月營收中,數字高低可視為蘋果供應鏈接下來
            營運動能強弱的先行指標。根據台積電先前所釋出的財測估算,六月營收需達到1360~1440
            億元才能達標,若最終數字落在此區間或以上都代表六月營收將創歷史新高,七月進入
            拉貨旺季再創新高的機會就更大。進入拉貨旺季再創新高的機會就更大了。 緊接在
            iPhone 13之後的蘋果新品還有新款MacBook Pro,市場預估在10月底或11月初發表,
            處理器將搭載M1升級版的M1X。此次共有兩款不同的M1X晶片,均會搭配10核心CPU
            (M1的GPU則為八核心),其中八個核心專注在執行高效能應用,另二個核心專注在節能上,
            不同之處在於GPU核心,一個會採用16核心,另一個則採用32核心,都是交給台積電五
            奈米產線代工生產。市場不排除第四季發表的Mac mini升級版,也會改採用M1X處理器
            取代英特爾處理器,加快台積電在蘋果筆電及桌機產品的滲透率。
            '''
        ),
    )
    assert parsed_news.category == '財經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1625750520
    assert parsed_news.reporter == '高適'
    assert parsed_news.title == '台積電先進製程霸主確立'
    assert parsed_news.url_pattern == '2026235'
