import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/04/11/a517450.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            二零一一年四月七日,馬來西亞的雪蘭莪舉行了一次關於多元文化主題的活動,多個團體的
            精彩表演和孩子們優美的舞蹈、合唱等,吸引了眾多馬來民眾,大家都沈浸在一片歡樂的
            氣氛中,他們同時也收到了一份天國樂團帶來的特別小禮物。 早上八點半,由法輪功學員
            組成的天國樂團演奏著優美的樂曲拉開了活動的序幕。他們邁著整齊的步伐,行進到現場,
            隊員們個個精神抖擻,一進場便吸引了現場的每一個人。天國樂團為觀眾們帶來了
            《法輪大法好》、《歡樂頌》、《法鼓法號震十方》等五、六首歌曲,並希望把法輪大法的
            美好帶給每一個人。 當天的演奏震撼了在場每一位觀眾的心靈。大家紛紛走近圍觀:有的
            興高采烈地欣賞演奏;有的用手機、相機爭相拍照留念,記錄下這精彩的表演;許多小孩子也
            開心地尾隨著隊伍,邊跑邊拍手;有的向法輪功學員要取手中的法輪功資料。 當天上午九點半,
            天國樂團的隊員們還演示了法輪功五套優美的功法。美妙的音樂,優美柔和的動作,學員們
            祥和的表情,整個場上一片祥和。在場的許多觀眾自發地模仿功法,許多小孩子席地而坐,盤上
            腿在法輪功學員的指導下認真地學起了第五套功法。
            '''
        ),
    )
    assert parsed_news.category == '法輪功,法輪功人權'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1302451200
    assert parsed_news.reporter is None
    assert parsed_news.title == '马来西亚天国乐团洪法传福音受欢迎'
    assert parsed_news.url_pattern == '2011-04-11-517450'
