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
    url = r'https://star.ettoday.net/news/1200075'
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
            便宜日圓即將成為過去式,有「日圓先生」之稱的榊原英資(Eisuke Sakakibara)預測,
            美國經濟攀上高峰後會逐步下滑,今(2018)年日圓兌美元匯率將介在110至105之間震盪,
            明(2019)年有機會挑戰100大關。 前日本財長榊原英資27日出席活動時表示,美國經濟成長
            優於市場預期,使得美元指數走強,而非美元貨幣相對走貶,今年日圓匯率可能在110至105
            之間徘徊。 不過榊原英資認為,美國經濟很快就會攻頂,隨後會從高點開始回檔,屆時美元
            匯率也會跟著表現疲軟,日圓有望向100日圓兌1美元挺進。因此,一旦他的預測準確,明年
            日圓將會轉強,有換匯需求的民眾手腳要快。 美中貿易衝突越演越烈,全球金融市場陷入
            動盪。路透社引述摩根大通日本市場研究部門主管佐佐木融(Tohru Sasaki)報導指出,
            「白宮內部目前對擬限制外資的問題仍呈現意見分歧的狀態」。此外,7月6日正是川普政府
            宣布對大陸進行下一步的動作的日子,屆時將會牽動股、匯市,就連日圓也不例外。 美中
            兩個互祭高額關稅,市場觀望氣氛較為濃厚,身為避險貨幣的日圓表現強勢,近期在109至110
            大關附近徘徊,加上新台幣匯率持續貶值,從今年高點29.069元下滑至30.4價位,使得日圓
            兌新台幣匯價持續彈升,台銀牌告價格再度出現0.28字頭,創下近3個月新高水準,讓不少
            哈日族哭暈在廁所。
            '''
        ),
    )
    assert parsed_news.category == '財經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530133740
    assert parsed_news.reporter is None
    assert parsed_news.title == '換匯手腳要快! 日圓先生:2019年日圓看升挺向100大關'
    assert parsed_news.url_pattern == '1200075'
