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
    url = r'https://star.ettoday.net/news/1200584'
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
            被許多選手稱為「最硬賽事之一」的馬祖鐵人三項將於 9 月 16 日登場,這次邀請香港馬
            祖鐵人三項國手司徒兆殷來台參賽,還有國內亞運培訓隊選手張綺文、林威志以及郭家齊共
            襄盛舉,要一起挑戰「地獄鯨鯊」自行車路線! 第二屆馬祖鐵人三項將於 9 月 16 日登場,
            中華民國鐵人三項協會表示,馬祖鐵人三項因為有許多丘陵地形,被許多選手稱作是「最硬
            賽事之一」,其中自行車項目為最嚴峻的考驗,延續兩公里的連續爬坡考驗著選手肌肉組織,
            總爬升高達 1600 至 1800 公尺之間。 自行車完賽之後,緊接著就是路跑,高低起伏的地形
            和高溫,也考驗著選手們的意志力,這次大會邀請到司徒兆殷來台參賽,同時有邀請了張綺文
            、林威志以及郭家齊參賽,讓一般選手可以有機會和國家級的選手同場較勁,有興趣的民眾
            可別錯過。 大會這次除了有「地獄鯨鯊」自行車路線的完賽獎牌以及賽事紀念酒之外,更
            祭出總獎金超過 25 萬獎金與等值商品等商品,本次馬祖鐵人報名截止日為 6 月 30 日,有
            興趣的民眾趕緊上伊貝特報名網報名!
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530092400
    assert parsed_news.reporter is None
    assert parsed_news.title == '馬祖三鐵9月16日登場!亞運培訓隊參賽 挑戰「地獄鯨鯊」賽道'
    assert parsed_news.url_pattern == '1200584'
