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
    url = r'https://www.epochtimes.com/b5/13/12/13/n4033178.htm'
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
            中共新華網援引朝中社13日報導,朝鮮12日以從事顛覆國家陰
            謀活動依照朝鮮刑法第60條對張成澤判處死刑,並已於當天執行。近日,關於北韓「攝政王
            」張成澤遭革職整肅的消息,引發國際關注,其真實原因眾說紛紜,港媒昨日更報出驚人消息
            ,傳張成澤跟第一夫人李雪主鬧不倫戀,讓金正恩疑戴綠帽。 張成澤承認企圖政變 中共官
            媒報導,朝鮮國家安全保衛部特別軍事法庭12日對張成澤的罪行進行了審理,認為張成澤作
            為現代版宗派的頭目,長期糾集不純勢力形成派別,企圖篡奪黨和國家的最高權力,以各種方
            法和卑劣手段實施顛覆國家的陰謀犯罪。張成澤本人也對罪行供認不諱。特別軍事法庭在
            公開審判後宣讀了判決書。 聯想到中共的文革 據港媒蘋果日報報導,德國駐北韓大使薩佛
            (Thomas Schafer)週二表示,他認為北韓軍方是因張成澤推動和中共的經濟合作計劃,威脅
            到軍方地位,決定剷除。 日本防衛大臣小野寺五也表示,張成澤在勞動黨政治局會上被公開
            帶走的畫面,讓他聯想到中國文化大革命的場面,擔心北韓未來可能會發生動盪。 南韓高麗
            大學教授趙榮基分析:「金正恩的權力基礎比父親金正日薄弱,這種情況下除掉張成澤這個
            重量級人物後,權力格局會出現空白,加重不穩定因素。」 張成澤遭革職處死 原因眾說紛
            紜 蘋果報導,有分析稱金正恩是為了收回張管理的約1184億元台幣海外秘密資金,張及其親
            信可能貪污了部份秘密資金且被發現,才遭肅清。張遭整肅後,北韓副總理盧斗哲與李武榮
            已逃往中國,現由中共當局提供庇護。南韓KBS電視台引消息稱,北韓當局要求全民參與批判
            張成澤運動,顯然是要鞏固金正恩的領導權威。 也有傳張下台原因,是與親外甥、北韓最高
            領導人金正恩的妻子李雪主有染。 李雪主涉色情錄影帶 傳與張成澤有染 早先就已盛傳金
            正恩手中握有李雪主當年在樂團時所拍攝的色情錄影帶。今年南韓《朝鮮日報》曾報導,北
            韓「銀河水管絃樂團」成員,因拍攝性愛影片,其中9名團員,包括北韓領導人的前度女友玄
            松月,被當局處決。當時北韓人民保安部在調查時竊聽到,團員曾提及「李雪主以前也和我
            們玩在一起」的對話內容。專門報導北韓新聞的媒體《Daily NK》稱,北韓當局對此也下了
            封口令,嚴禁打聽金正恩和李雪主的家庭狀況。 蘋果日報報導說,張與李雪主有染,且秘密
            資助金正恩的大哥金正男,傳金正男成了下一個肅清目標,法國警方已對留學巴黎的金正男
            之子金韓松加強保護。 今天最新的消息,網絡盛傳錄影帶中的男主角竟然就是張成澤,這頂
            綠帽讓金正恩吞不下去,才會下重手清算二人,解除一手培植自己的姑丈所有實權。南韓媒
            體更說,金正恩現在已經在物色新的第一夫人,但這個消息未經證實。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1386864000
    assert parsed_news.reporter == '岳青,孫芸'
    assert parsed_news.title == '金正恩疑戴綠帽 傳李雪主色情錄像上有張成澤'
    assert parsed_news.url_pattern == '13-12-13-4033178'
