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
    url = r'https://star.ettoday.net/news/379'
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
            台北市警察難當!根據內政部統計,99年申請調出台北市警察高達1057名,申請調入卻只有
            216名,在北市服勤的警察們大都希望調到南部,但南部警察卻鮮少願意轉調台北,凸顯台北市
            警力問題。內政部長江宜樺已行文替北市警察申請加給,最多每月可有8435元。 台北市為
            台灣政治經濟中心,同時也是警務最繁重地區。撇開一般例行勤務不談,光是各種抗議,突發
            狀況,都較其他縣市多出不少;加上身在首都,民眾對警察都有高規格要求,一言一行都用
            放大鏡檢視,對比之下,其他縣市警察勤務顯得較為輕鬆,因此北市警察申請外調幾乎連年
            不斷。 台北市除了有國家元首外,各級部會首長全都聚集在此,根據資料顯示,從96年到
            今年8月,台北市特勤職務共3萬445件,佔全國45%。因此99年申請外調者高達1057名,卻
            只有216名申請調入北市,一來一回相差4倍多,北市警察人力吃緊可見一斑。 有鑑於此
            ,內政部長江宜樺已經函文行政院,替北市服勤的警察們申請額外津貼,做為「首都警察勤務
            加給」,只要通過,在北市負責外勤的警察每個月最多可領8435元,內勤最多每月可領
            3373元,等於一年最多可增加3到10萬元的收入,希望藉此留住北市警察,避免人力流動
            造成的困擾。
            '''
        ),
    )
    assert parsed_news.category == '政治'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1317915300
    assert parsed_news.reporter is None
    assert parsed_news.title == '北市警察難當紛外調 將調加給每月多8435元'
    assert parsed_news.url_pattern == '379'
