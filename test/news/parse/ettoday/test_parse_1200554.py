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
    url = r'https://star.ettoday.net/news/1200554'
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
            位於新北市永和區有家人氣排隊店家,店名就叫做「北蘭阿姨商行」,懂的人總是會
            在心底笑笑,餐點很簡單,招牌主食就是嘎拋豬肉飯、蒜味香腸飯、嘎拋炒泡麵,雖然創業的
            三個年輕人沒有餐飲背景,但因為愛吃而研發出的嘎拋豬肉飯卻很受歡迎。 在台灣各地都有
            泰式料理店,打拋豬肉更是常見的菜色,不過北蘭阿姨的嘎拋豬肉飯用淋膜食用紙來裝盛,然後
            再放上半熟蛋與幾片香腸,感覺就不一樣,而且還輕輕劃過半熟蛋,蛋液流出超邪惡。北蘭阿姨
            商行合夥人之一的石馥慈表示,他們用得是香里活力豬肉,蛋則是有機蛋,因此才敢讓客人吃
            半熟蛋。 提到創業,石馥慈說他們三人都是在服務業多年,總覺得不能這樣一直下去,於是
            有了創業的念頭,因此他們都愛玩又愛吃,最後決定開家餐館。不過有了創業念頭,他們準備
            了2-3年才真正開了這家「北蘭阿姨」,而負責研發菜單的石馥慈,更是每天下班後就是做菜
            試菜,有空大家相約出國玩順便找靈感。 為何會以嘎拋豬肉飯、蒜味香腸飯為主打招牌?
            石馥慈當初沒有設定要開什麼類型的餐廳,但她很愛泰式料理,其中包括打拋豬肉,她覺得
            打拋豬肉很適合台灣人口味,她用了大量的九層塔與番茄、大蒜、魚露及泰式香料。至於
            蒜味香腸飯則是因為她們找到到豬肉供應商香里,發現他們家的香腸很好吃,所以就拿來做成
            香腸飯。嘎拋炒泡麵則是最近的新菜單,因為北蘭阿姨開到半夜,有人想吃宵夜、但又不想
            吃飯,所以她們就推出很適合當成宵夜的嘎拋炒泡麵。 除了主食之外,這裡也有現點現做的
            厚片與烤餅,及泰式奶茶,不想吃飯也可以點這些餐點來吃 。 至於為何把店名取為
            「北蘭阿姨商行」呢?石馥慈說,因為有次大家相約到南機場夜市逛逛,結果她把美蘭阿姨
            新鮮果汁吧的「美蘭」念成「北蘭」,當時讓大家笑翻,準備開店時就想到這用這個KUSO的
            名字來命名。雖然叫北蘭阿姨,石馥慈跟她的夥伴與員工都很年輕,店裡沒有一個是「阿姨」。
            而營業時間從下午5點到凌晨1點,純粹因為習慣晚睡了,早上起不來。不過也因為,讓永和
            地區朋友多了一個宵夜選擇。
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530100800
    assert parsed_news.reporter == '黃士原'
    assert parsed_news.title == '店名「北蘭阿姨」有點惡搞 招牌嘎拋豬肉飯的半熟蛋卻很邪惡'
    assert parsed_news.url_pattern == '1200554'
