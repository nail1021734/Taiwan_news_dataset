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
    url = r'https://star.ettoday.net/news/2096796'
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
            UNIQLO TAIPEI全球旗艦店於今日(8日)早上10點開幕,雖然是選在平日的週五早上時間,
            開門時間還未到,現場就已聚集了非常多客人,截至10點為止,大約有近三百人,排在第一個的
            張小姐表示:「我8點半吃完早餐來的,至少會花個五千塊跑不掉。」也有客人逗趣坦承自己
            是「蹺班」來的,因今天現場釋出先前搶到爆的藝術家聯名杯盤系列,一開門迅速一掃而空,
            場面頗為激烈,預估明天雙十連假首日也將會有眾多人潮。 第一位排隊的民眾張小姐表示
            :「我今天早上八點半吃完早餐就來了。」時間沒有到特別早,經現場觀察,大部分民眾約在
            開門前快速聚集,九點左右只有約三十組客人。今天來到旗艦店張小姐主要想買的是UNIQLO
            的羅浮宮聯名系列,以及藝術家合作系列,「我覺得(花費)大概五千塊跑不掉,至少啦,他
            們幾乎每一季出的我都會買。」 10點一到,UNIQLO全球旗艦店準時營業,許多民眾一進店
            就衝往四樓聯名區,瘋搶先前網路上搶到爆的
            Andy Warhol,Jean-Michel Basquiat,Keith Haring聯名杯盤組;另外,今日開賣
            的「UNIQLO and White Mountaineering」白山聯名系列,也馬上排起人龍。 由原先
            明曜百貨店面改裝而成的「UNIQLO TAIPEI全球旗艦店」,擁有四層樓面,總坪數達到
            1,065坪,開幕亮點包括一樓增設首度引進台灣的「UNIQLO FLOWER」專區,種類多樣化的
            鮮花、植栽99元起;首四日每天不限消費金額前150名,還可憑發票到門口兌換熱騰騰的免費
            雞蛋糕。 樓面配置為1樓部分女裝、UNIQLO FLOWER專區;2樓女裝、童裝與嬰幼兒服裝,
            並設置KIDS LIBRARY童書遊憩區;3樓以男裝為主;4樓為設計師聯名專區,以及UTme!
            客製化UT專區。
            '''
        ),
    )
    assert parsed_news.category == 'fashion'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1633660200
    assert parsed_news.reporter == '王則絲'
    assert parsed_news.title == '有人蹺班排隊!UNIQLO旗艦店開幕近300人聚集 一進門搶「這個」'
    assert parsed_news.url_pattern == '2096796'
