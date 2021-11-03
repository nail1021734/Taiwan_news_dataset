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
    url = r'https://star.ettoday.net/news/1200362'
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
            「ETtoday看電影」直播主持人膝關節本周依然還在歐洲蜜月中,節目依然由Youtuber界的
            古天樂「部長」代班主持,本周夯電影,將介紹睽違14年,再度回歸的「超人特攻隊2」,另外
            還將加碼介紹2018下半年受到高度期待的動畫電影!收看直播並跟主持人互動,還有機會獲
            得「名偵探柯南:零的執行人」電影周邊商品喔! 皮克斯動畫電影《超人特攻隊》14年前在
            全球叫好叫座,不僅締造了6.3億多萬美金(約190億台幣)的票房成績,還獲得了奧斯卡殊榮,
            但續集卻讓粉絲苦等了14年,這種焦躁等待的心情,直接反應在市場上。上周末《超人特攻
            隊2》在北美上映,勢如破竹橫掃1.8億美金(約54億台幣)的票房,直接刷新《海底總動員2》
            的1億3千萬美金的成績,成為首周最賣座的動畫電影。
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530077460
    assert parsed_news.reporter is None
    assert parsed_news.title == '2018下半年動畫電影總整理 「看電影」直播部長陪你聊動畫'
    assert parsed_news.url_pattern == '1200362'
