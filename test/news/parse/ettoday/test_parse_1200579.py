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
    url = r'https://star.ettoday.net/news/1200579'
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
            位於鳳商旁的施家蔥肉餅,經營三十幾的年頭是許多鳳山人認證的銅板下午茶,更是許多鳳商
            學子讀書時期的心頭好,銅板價蔥肉餅,美味又能飽足,尤其油炸蔥肉餅那股油香味可讓圍牆內
            的學生都受不了這個好滋味,除了平日下午在鳳商旁擺攤,周二晚上還會在開漳聖王夜市加碼
            擺攤,讓許多下午時段無法外出的在地人,也有一嚐好味的機會。 從排隊人潮就能窺知施家
            蔥肉餅的美味程度,老闆手不停地包入蔥花肉餡再將麵糰揉成圓餅狀並觀察一旁煎台有空味就
            丟下生蔥肉餅,特別使用自製豬油煎炸蔥肉餅,站在一旁就能聞到迷人油香味,加上施家蔥肉餅
            價格平實,總是加入排隊行列,目前蔥肉餅原味15元,加蛋20元,加蛋加菜25元,喜歡吃九重塔
            的朋友,推薦蔥肉餅加蛋加菜,跟老闆點好餐後,就等待蔥肉餅油炸到外皮呈現金黃酥脆時,
            立即夾起並瀝油後放入袋中,客人再依喜好自行添加醬料。 使用豬油半煎炸的蔥肉餅香氣真
            不同凡響,香氣層次就是不一樣,炸到蓬鬆有厚度的蔥肉餅夾上九重塔與雞蛋後,一口咬下,
            豬油香的麵皮有嚼勁Q彈,蛋的滑嫩與九重塔的塔香讓餅皮越吃越香、越吃越順口,難怪排隊
            人潮總沒少過。由於使用豬油,香味固然迷人,建議一定要趁熱吃才能吃到不油不膩的香氣,
            冷掉的餅皮就顯油味。 喜歡蔥肉餅的朋友,別錯過這篇討論,快把你的口袋名單留言給我們
            知道喔! 高雄美食地圖
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530169200
    assert parsed_news.reporter == '高雄美食地圖'
    assert parsed_news.title == '鳳山人認證的銅板下午茶!高雄施家蔥肉餅只要25元'
    assert parsed_news.url_pattern == '1200579'
