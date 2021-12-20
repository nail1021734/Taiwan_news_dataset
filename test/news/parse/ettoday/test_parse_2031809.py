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
    url = r'https://star.ettoday.net/news/2031809'
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
            波士頓紅襪@紐約洋基 比賽時間: 7/16 7:08 KS分析師推薦: 大分過盤
            (預測運彩盤:9.5大分) 紅襪在上半季末的最後5戰吞下4敗,對球隊士氣略有打擊,
            好在目前戰績仍暫居美聯東區霸主地位。本場預計推出羅德里格斯(Eduardo Rodriguez)
            先發,7月繳出本季最佳表現,雖然前場吞下敗仗,但最近5次先發出賽幫助球隊取得4勝1負,
            且最近5次先發對戰洋基時,球隊戰績3勝2負,生涯對戰洋基的防禦率夠水準的3.88,
            本場表現值得期待。 洋基目前打來相當掙扎,不過好消息是,連續2個客場系列賽都取得
            對戰優勢,勝率也再次站回5成,打線持續增溫,對洋基來說是好消息,回到主場出賽的進攻
            火力更值得期待,但值得留意的是,牛棚大將羅埃西賈(Jonathan Loaisiga)因疫情要
            缺陣一段時間,牛棚穩定度仍有疑慮。 兩隊近期交手由紅襪以7連勝姿態佔上風,但洋基
            打線持續增溫,本場在主場優勢的加持下,看好打線能夠予以反擊,故此戰看好大分格局。
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1626343620
    assert parsed_news.reporter == 'KS運彩分析師'
    assert parsed_news.title == '紅襪@洋基 看好大分過盤'
    assert parsed_news.url_pattern == '2031809'
