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
    url = r'https://www.epochtimes.com/b5/13/12/31/n4046950.htm'
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
            要求匿名的黎巴嫩官員稱,敘利亞戰機30日轟炸了靠近黎巴嫩貝卡谷地(Bekaa Valley)的
            東部城鎮阿薩爾(Arsal)邊境地區後,該國軍隊動用防空火力向兩架敘利亞戰機開火。 這是
            3年前敘利亞國內衝突爆發以來,黎巴嫩軍隊首次利用防空系統,反擊敘利亞戰機對其領空的
            侵犯。隨著內戰持續蔓延,敘利亞四鄰都遭受暴力波及。 阿薩爾是敘利亞反抗軍的大本營,
            也是數千敘利亞難民的避難地。 敘利亞爆發內戰以來,敘戰機經常越境追擊戰敗、逃入黎境的
            反抗軍,有時也轟炸黎境領土,黎巴嫩政府抗議,也未獲敘軍回應。這次戰機向山區發射4枚
            導彈後,黎軍首次反擊。 近期,黎前財政部長沙塔(Mohamad Chatah)被汽車炸彈炸死後,
            遜尼派的沙特有感敘利亞什葉派勢力逐潮擴大,威脅沙特國土安全,沙特承諾資助黎巴嫩軍隊
            30億美元,以維持區域安全。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388419200
    assert parsed_news.reporter == '萬平'
    assert parsed_news.title == '黎巴嫩砲轟越境敘利亞戰機'
    assert parsed_news.url_pattern == '13-12-31-4046950'
