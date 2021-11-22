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
    url = r'https://www.storm.mg/article/4028800?mode=whole'
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
            「苦讀了6個月、有些人更久。」做足準備參加科技公司面試是谷歌工程師簡嘉良分享的
            求職心法。疫後科技人才荒,他說,遠距上班主雇雙贏,辦公室將蛻變為社交與合作
            空間。 FAANG這組英文縮寫,代表當今科技業最火紅的跨國大型企業,臉書(Facebook)、
            蘋果(Apple)、亞馬遜(Amazon)、網飛(Netflix)、谷歌(Google),且是許多年輕世代
            軟體科技人才嚮往歷練的職場。 COVID-19(2019冠狀病毒疾病)之後,人們更集中在網路
            活動。調查發現,因為居家辦公的彈性,Youtube和電商龍頭亞馬遜在上班時間的
            流量增大。另外,華爾街日報報導,谷歌、臉書和亞馬遜的廣告收入成長約3成,去年3大平台
            囊括美國一半的廣告業績。 相關趨勢帶動科技業對軟體人才的需求倍增,薪資福利跟著水漲
            船高。薪水分析平台levels.fyi指出,以臉書為例,產品經理平均年薪高達35萬美元
            (約合新台幣974萬元),成為轉職首選。 簡嘉良(Johnny Chien)是谷歌工程師暨舊金山
            灣區台灣青商會會長,他在受訪時告訴中央社記者,遠距工作的彈性讓企業主可以雇用到以往
            無法雇用的人,也讓更多人不用舉家遷移就能為矽谷的科技公司工作。 簡嘉良在台灣出生,
            12歲時隨父母移居加拿大,英屬哥倫比亞大學(UBC)畢業前在電商龍頭亞馬遜實習,接著轉入
            正職,從溫哥華搬到西雅圖。又因妻子覓得矽谷的工作,他轉職到谷歌。在舊金山灣區台灣
            青商會的服務中,他希望幫助更多人自信地找到理想工作,並連結有心創業者更多
            資源。 簡嘉良說,很多人對於進軍科技業有迷思,認為企業面試「考問」工程師的
            題目很難。他的經驗談是,「有方法針對面試做足準備,愈多的練習會變得更
            熟能生巧」。 以亞馬遜和谷歌為例,履歷表進入企業的人資手上進行第一輪的面試後,
            正職職缺約有5至6關的面試。各家企業每年在面試的方式上會進行微調。 「每份履歷表
            只獲得幾秒的瀏覽時間,寫得好,事半功倍。」他說,履歷表的重點要放入人資部門在乎的
            內容,不要「落落長」浪費紙上空間。 在科技公司多關的面試中,會從內部系統隨機
            「抽籤找內部員工面試新人」。應徵者遇到誰不一定,簡嘉良強調做足準備的重要性,
            他以身邊親友的經驗,「找人對談、模擬練習,一百次也不嫌多」。 麥道威
            (Gayle Laakmann McDowell)著作的「破解工程師面試」
            (Cracking the Coding Interview,暫譯)是科技業面試聖經;
            另外,LeetCode等網站也找得到面試題庫的資源。 簡嘉良告訴記者:「許多谷歌同事
            至少都苦讀了6個月、有些人更久,不是你認識誰就能進公司,而是讀得多用力
            才能進得去。」 他分享,「思考模式、邏輯思維、解決問題的能力和表達能力」是科技
            工作看重、也是面試者對求職者評分之所在。 疫情無聲地捲動科技業的職場革新。
            除了用人與工作模式的彈性,簡嘉良看到辦公室空間的新趨勢,「辦公室面積不會用到緊繃,
            提供面對面與視訊連線的會議室變多了」。
            '''
        ),
    )
    assert parsed_news.category == '風生活,財經,科技,下班經濟學,商業'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1635984600
    assert parsed_news.reporter == '中央社'
    assert parsed_news.title == '科技人才荒,矽谷出現千萬年薪職缺!Google工程師:這些能力很重要,很多人練半年才錄取'
    assert parsed_news.url_pattern == '4028800'
