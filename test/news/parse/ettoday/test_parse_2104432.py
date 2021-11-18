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
    url = r'https://star.ettoday.net/news/2104432'
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
            隨著豪華露營逐漸成為熱門旅遊方式,選擇露營車的旅客同樣開始增加,像是花蓮就有民宿
            提供六星級露營車,配備夢幻天窗可以數星星,每台皆有獨立海景庭院和衛浴空間,公共設施
            包含泳池、沙坑、健身房都能使用,最讚的是一出門就能欣賞浪漫曙光,看完還能馬上
            睡回籠覺超方便。 離海很近的都鐸王朝露營車,除了擁有首排海景的壯闊視野,園內還有
            提供英格蘭風民宿空間可以入住,凡事房客都會另贈海景下午茶體驗,公共設施包括海景
            泳池、健身房、鞦韆、沙坑全部免費使用,園內目前只有5台露營車加上人氣很高,想入住
            的朋友要搶要快。 露營車提供兩種房型選擇,皆有獨立庭院和衛浴設施備、最多能容納4人,
            寬敞空間包含客廳、臥室與冷氣,若是喜歡大天窗的朋友建議選擇「極光」,躺沙發就能瞭望
            繁星璀璨,「銀河」則是提供上下舖空間,適合帶孩子出遊的小家庭。 此外,園區還有開放
            發呆亭和公共烤肉區,免費提供給房客使用,在地知名055龍蝦海鮮餐廳就在隔壁,吃飽喝足後
            可別急著睡覺,記得參考民宿提供的日出時間設定鬧鐘,才不會錯過最美的曙光美景。
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634696400
    assert parsed_news.reporter == '鍾奇峻'
    assert parsed_news.title == '離曙光超近!花蓮豪華露營車自備星空窗 入住即享免費海景下午茶'
    assert parsed_news.url_pattern == '2104432'
