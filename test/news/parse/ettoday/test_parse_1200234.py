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
    url = r'https://star.ettoday.net/news/1200234'
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
            你是不是曾經在巷弄裡,看過翻找垃圾袋的狗狗?也是不是看過瘦弱的小貓咪渴望食物的眼
            神,只要我們願意伸出援手,浪浪的命運就會大大不同!ETtoday寵物雲邀請各位愛心爸媽分
            享您和毛小孩相遇、相惜的經過,投稿到「2018浪愛回家公益年曆徵選活動」,一起做公益
            關懷流浪動物。 ETtoday寵物雲長期推廣領養代替購買的觀念,報導許多感人的救援故事,
            讓更多人重視流浪動物的議題,這次和PetTalk愛寵團隊及各大寵物品牌合作,製作浪愛回家
            公益年曆,扣除成本的收入將轉為「物資」,全數捐給動保團體Mary`s doggie社團法人台灣
            瑪莉愛狗協會、亞洲動物救援協會、巴克救援協會與行政院農業委員會動保處收容所。
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530252180
    assert parsed_news.reporter is None
    assert parsed_news.title == '想為流浪動物盡一份心力嗎? ETtoday邀你分享「領養故事」拯救浪浪'
    assert parsed_news.url_pattern == '1200234'
