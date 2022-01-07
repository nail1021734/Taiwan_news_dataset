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
    url = r'https://star.ettoday.net/news/1200503'
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
            行腳台灣奉獻已46年的美籍神父安德森,創立「圓的成長中心」,動員教友募集民生物資籌
            組物資銀行,協助北中南各地醫院教會社區,日前獲中央頒發「績優外籍宗教人士」。他27
            日順利拿到台灣身分證,成為台中市第2位殊勳歸化成為市民的外籍人士。他也開心地拿身
            分證說,「我是正港台灣人」。 現年75歲的美籍神父安德森,1972年僅29歲的他來台傳教,
            在台中先學會台語,接著到彰化、台北、台中、高雄等地教會服務教民眾英語。安德森在高
            雄五甲耶穌聖體堂定居服務長達32年,70歲到南投市天主教擔任神父3年多,2年前轉至沙鹿
            天主堂服務至今。 「我是正港台灣人!」安德森神父說,過去自己不太會說台語,很早之前
            有一次等公車,在地民眾即使語言不通,也還是熱情主動告訴他怎麼搭車,感覺台灣人就像自
            己家人一般親切友善 。現在有了身分證,做什麼事情都會讓他方便許多,十分開心。 安德
            森為了幫助弱勢,與教友創立「圓的成長中心」,動員教友收及民生物資籌組物資銀行,主動
            關心照顧包括台北、台中、嘉義、高雄等地醫院、教會及社區弱勢,曾獲內政部頒發「績優
            外籍宗教人士」表揚。 台中市政府參事郭振益今天代表市長林佳龍前往沙鹿天主堂,轉發
            中華民國身分證給他,藉此感謝他在台近半個世紀的奉獻,並歡迎取得我國國籍並入籍台中
            。 市府參事郭振益表示,安德森神父在台服務近46年,雖年歲已高,對台灣弱勢族群的奉獻
            仍不遺餘力,非常感謝神父對台灣這塊土地的長期付出,深根台灣,愛在台灣,是最道地的台
            灣人。 民政局表示,國籍法前年修法,外籍人士在我國有特殊功勳經行政院核准,無需放棄
            原有國籍,可直接辦理歸化取得我國國籍。台中市第1位因特殊功勳歸化國民的外國人為美
            籍神父曾顯道,其長期致力教育工作並關懷弱勢家庭、新住民及受刑人,經行政院核准歸化
            取得我國國籍,而天主教台中教區神父安德森今日獲得中華民國身分證,成為台中市第2位殊
            勳歸化成為市民的外籍人士。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530088080
    assert parsed_news.reporter == '李忠憲'
    assert parsed_news.title == '無私奉獻46年拿到身分證 美籍神父安德森:我是正港台灣人'
    assert parsed_news.url_pattern == '1200503'
