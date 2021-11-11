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
    url = r'https://star.ettoday.net/news/8902'
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
            每次遇到緊急意外,大家第一個想法就是消防隊能趕快來,但您知道全台出勤速度最快的消防隊
            是哪裡嗎?答案就是新竹市,從報案到抵達現場,一年下來平均只要3分37秒,比紐約市消防隊
            還要快,而且他們自認是全世界最快的。 火警意外發生、人員受傷搶救,每碰到這時候
            ,消防隊搶救,分秒必爭,但在新竹市的民眾,大家幾乎可以放心,因為他們的速度真的有夠快
            ,警笛一響,人員用衝的,穿裝備幾秒鐘就搞定,隨時準備出勤,到了夜裡也一樣,睡覺還穿制服
            ,連襪子都沒脫,裝備放一旁,救護一來,立刻著裝。一邊還在接報案電話,另一邊就已經準備
            出勤,根本花不到一分鐘。 就因為這麼精實,所以紀錄會說話,整年度的成績和美國紐約
            消防隊一比,紐約消防出勤到現場時間平均4分38秒,新竹市只要4分27秒,火警救護,紐約
            只要4分19秒,新竹市更只要3分37秒,快了整整42秒,而且不是在臭屁,新竹市消防局自認
            這樣速度不只是全台最快,還是全世界最快,因為他們知道緊急救援黃金時間大概只有案發
            5至6分鐘,就是希望靠這樣速度,讓民眾更心安。
            '''
        ),
    )
    assert parsed_news.category == '地方'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1322189760
    assert parsed_news.reporter is None
    assert parsed_news.title == '第一名!竹市消防出勤 號稱世界最快'
    assert parsed_news.url_pattern == '8902'
