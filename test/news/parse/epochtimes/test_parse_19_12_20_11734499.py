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
    url = r'https://www.epochtimes.com/b5/19/12/20/n11734499.htm'
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
            紐約州健保市場、大紀元新唐人電視台媒體集團為華人社區舉辦的第四場「紐約州健保市場
            註冊諮詢會」,將於1月11日蒞臨法拉盛啟揚社區中心。 活動內容包括: (1)紐約州健保市場
            官員陳敏敏將為華人社區民眾主講如何通過紐約州健保市場投保並為民眾解答問題。(2)
            安保健康保險營業經理吳偉傑主講「基本計畫知多少」(Emblem Health Plan)。(3)紐約
            坤德中醫養生軒馮羅小潔中醫師主講「十二時辰養生秘訣 」。(4)安保、第一保健和親情
            健保的專業人士現場提供保險諮詢和註冊服務。(5)「坤德中醫養生軒」專業團隊現場義診,
            把脈、推拿、按摩、艾灸。(6)法拉盛醫院提供戒菸服務及牙齒、血壓,肺功能和血氧飽和度
            檢查。(7)東方聽力中心提供聽力檢測與義診。 現場有傳統才藝,包括書法、楊龍飛老師
            武道養生講解和示範。 社區商家大力支持本次活動,提供了豐富禮品,包括價值288美元的
            Magic富氫水杯、200美元的TARGET禮品卡、168美元玄寶黑蔘口服液、45美元韓國精品
            不粘平底鍋,以及韓國一分鐘植物染髮劑、韓國炸雞券和歡迎毯。 歡迎廣大社區民眾前往諮詢。
            '''
        ),
    )
    assert parsed_news.category == '美國,紐約生活網,紐約新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576771200
    assert parsed_news.reporter is None
    assert parsed_news.title == '大紀元新唐人第四場健保註冊諮詢會 1/11蒞臨法拉盛'
    assert parsed_news.url_pattern == '19-12-20-11734499'
