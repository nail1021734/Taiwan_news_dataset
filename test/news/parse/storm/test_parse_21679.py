import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.storm


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='風傳媒')
    url = r'https://www.storm.mg/article/21679?mode=whole'
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

    parsed_news = news.parse.storm.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            網路科學期刊《公共科學圖書館》(PLOS One)最新論文指出,中學學科成績,基因遺傳因素
            佔58%,物理、化學、生物等理科表現尤其如此;藝術、音樂等人文學科,遺傳影響較低,
            家庭與學校的影響僅佔36%。不過,該研究也強調,基因影響並非絕對,即使同卵雙胞胎,
            成績也會有落差。 英國12年義務教育從5到16歲,最後一年學生通常會報考「普通中學教育
            文憑測驗」(GCSE),根據成績申請兩年制的大學先修課程A-Level。研究人員為了找出中學
            成績表現與基因的關聯性,搜集全國1萬1117名16歲雙胞胎考生成績,包括同卵雙胞胎與
            異卵雙胞胎。 研究對象來自相同的家庭,也接受相同學校教育,對照其性別因素後,得到
            前述結果。參與研究的基因行為學專家普洛明(Robert Plomin)說:「研究結果顯示,
            孩子覺得容易的學科,興趣跟資質影響同樣重要,學習動機可能來自擅長那門學科的
            感覺。」 普洛明認為:「基因促使人們創造、選擇並調整環境,天生條件驅動後天發展,
            進而強化天賦能力,數學好的孩子會跟喜歡數學的人交朋友,喜歡讀書的人會加入讀書會,
            在家也會讀完書架上每本書。」 倫敦大學教育學院科學教育教授瑞斯(Michael Reiss),
            雖然同意天生條件影響學習,卻不認同上述結論研究,他說:「就像有人戴眼鏡是因為
            天生視力不佳,有的卻沒有遺傳問題,結果不都一樣,跟基因一點關係都沒有。」
            幫助學業落後的孩子改善閱讀技巧,同樣能改善學業成績。 瑞斯批評:「不管是數學、
            划船或伸縮喇叭,好老師對於學生的個別學習需求,都會有一定敏感度,這跟基因應該
            沒多大關係.......這研究可能讓家長、老師與學生開始擔心,『天生不是那塊料,
            努力也沒有用』,這種邏輯錯誤的基因宿命論,誤導性很強又很難改變。」
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1386902880
    assert parsed_news.reporter == '楊芬瑩'
    assert parsed_news.title == '兒少學業成績差距 遺傳因素佔58%'
    assert parsed_news.url_pattern == '21679'
