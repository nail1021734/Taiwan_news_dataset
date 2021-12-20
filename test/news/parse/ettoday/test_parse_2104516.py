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
    url = r'https://star.ettoday.net/news/2104516'
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
            在演藝圈生存,一舉一動都可能被外界放大檢視;在YouTuber界也是,若有負評、負面舉動,
            都可能失去觀眾。最近YouTuber小玉(朱玉宸)爆出換臉賣謎片非法牟利,引發網路熱議,
            就有網友好奇,「負評最少的台灣YouTuber是誰?」貼文一出,立刻吸引大票網友熱烈討論
            。 有網友在PTT的Gossiping板上,以「負評最少的台灣YouTuber是誰」為題丟出討論,
            提到很多人都會討論誰是零負評美女、零負評藝人、零負評歌手等等,那眾多YouTuber之中
            ,大家覺得誰的負評最少呢? 貼文曝光後,網友紛紛留言回應,「反正我很閒」、「鐘佳播」
            、「一定是佳播哥」、「萍哥,萍嫂好會煮」、「唯一推薦萍哥,影片內容富有教育意義,
            又好吃,沒看過的快去看」、「好味小姐吧」、「好味小姐不可能有負評」、「洋蔥,
            他的影片幾乎圍繞理工魯蛇為主」、「HowHow吧」、「啾啾鞋」、「白痴公主」
            、「千千最高」。 其中,被最多人點名的則是鋼琴演奏YouTuber,「一定是Pan Piano,
            那邊沒有爭端」、「Pan紅到國外,有口皆碑」、「Pan,世界和平」、「Pan+1」
            、「Pan Piano吧,那邊世界和平」、「Pan,連外國人都讚美」。 據了解,「Pan Piano」
            是一位來自台灣的鋼琴演奏YouTuber,近年多穿上性感風格的服裝彈鋼琴,
            不只讓人耳朵懷孕,還能大飽眼福,擁有一票死忠粉絲。值得一提的是,她截至目前都
            尚未曝光真面目,堅持不露臉的風格,更讓她增添了不少神祕感。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634614500
    assert parsed_news.reporter == '曾筠淇'
    assert parsed_news.title == '外國人也讚美!「零負評YouTuber」鄉民一致點名她:沒有爭端'
    assert parsed_news.url_pattern == '2104516'
