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
    url = r'https://www.cna.com.tw/news/aipl/202104110048.aspx'
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
            北市衛生局制定「新興菸品管理自治條例」草案,擬率先全國全面禁售電子菸等類菸品,
            並將加熱式菸品納管。衛生局表示,草案已送入議會審議,最快下半年可公告
            實施。 「台北市新興菸品管理自治條例」制定草案規範,任何人不得
            製造、輸入、販賣、供應、展示、廣告招牌電子菸等類菸品或其組合元件,違者可處新台幣
            1萬元以上5萬元以下罰鍰,並令其限期改正;屆期未改正者,得按次連續處罰。 草案中
            規定,若未滿18歲民眾使用電子菸、加熱式菸品等新興菸品,須接受戒新興菸品相關
            教育,無正當理由未參加則處2000元至1萬元罰款,並可按次處罰。 此外,電子菸、加熱式
            菸品等新興菸品將禁止在學校、醫療院所、政府機關室內場所、大眾運輸工具、公眾休閒
            娛樂場所、老人福利機構的室外場所、衛生局公告指定場所等處使用,違者可處2000元
            至1萬元罰款。 「台北市新興菸品管理自治條例」已在3月23日送交議會審議,衛生局
            健康管理科科長林夢蕙表示,草案內容皆是比照「菸害防制法」修正草案訂定,若此次會期經
            三讀審議通過,再送行政院核備,期望下半年就能公告實施。 衛生局說明,電子菸是全球新興
            健康危害議題,對於眼部、肺部健康都有嚴重危害,且國外曾查出含有安非他命、大麻等毒品
            案例,還有爆炸的風險,高度危害使用者及周遭人員健康,顯示此類產品有嚴加管制的必要。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1618070400
    assert parsed_news.reporter == '陳昱婷台北'
    assert parsed_news.title == '北市新興菸品自治條例 擬禁售電子菸納管加熱菸'
    assert parsed_news.url_pattern == '202104110048'
