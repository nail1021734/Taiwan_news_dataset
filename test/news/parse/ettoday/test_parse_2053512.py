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
    url = r'https://star.ettoday.net/news/2053512'
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
            在八德廣福路上有兩家蚵嗲專賣店,印象以來經營好長一段時間,兩家可都是別具特色,
            各有自己死忠愛好者,個人偏好這家「阿琴蚵嗲」,外觀只有簡陋的鐵皮屋,但門口總是充滿
            排隊人潮,滿滿真材實料用料大方,銅板價格就可以享用到,買個來作為點心吃。 位在廣福路
            大馬路邊,是由簡單的鐵皮屋搭成,把車子停好在路邊,就可以加入排隊行列。 蚵嗲都是現點
            現炸,所以都要等候點時間,不過看到滿滿鮮蚵與韭菜末,一副好吃模樣讓人肚子更餓
            。 現炸出爐或許會較油膩,但店家都會盡量將油滴乾,吃起來清脆沒什麼油膩感。 除了招
            牌蚵嗲與炸物以外,可別忘記來杯楊桃湯,搭配上可以解炸物油膩,楊桃帶出獨特自然清香
            ,真材實料喝過就能感受到,超解渴真是透心涼。 店內招牌蚵嗲不少人都為這而來,完整外觀
            滿滿好料都包在裡面,正常是裝在袋子裡面,通常買好上車就會開始咬,剛炸好的口感最酥脆
            。 對切開酥脆外表之後,立刻看到大量翠綠色韭菜,鮮蚵又大又肥美。記得要打包點蒜蓉醬,
            可是重口味醬料,鹹甜滋味淋在炸物上真是絕配。 阿琴蚵嗲特別包入肉塊,咬下後會爆出
            滿滿肉汁香,更多了份鹹香味在其中。 除了蚵嗲外還會順道買點炸物,同樣現點現炸的美食,
            尤其從油鍋裡剛炸出爐時,這份香酥味會讓人口水直流。 不同於一般蘿蔔糕,這裡可是又厚
            又大塊,外表有這金黃酥脆,古早味純米漿無粉無添加,會讓人越吃越涮嘴。 炸米血糕也深受
            不少喜愛,油鍋將外表炸到Q彈有咬勁,裡面依舊維持著軟Q,大火炸出的美味,真會讓人越吃越
            上癮。 經過阿琴蚵嗲多會停下來購買,特別將常買的菜單介紹一下,份量多料好實在可是一大
            特色,現點現炸的美食可最吸引人,這份傳統美食介紹給大家。
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1630116000
    assert parsed_news.reporter is None
    assert parsed_news.title == '塞滿肥蚵韭菜末!桃園鐵皮屋「炸蚵嗲」 酥脆不油還有解膩楊桃湯'
    assert parsed_news.url_pattern == '2053512'
