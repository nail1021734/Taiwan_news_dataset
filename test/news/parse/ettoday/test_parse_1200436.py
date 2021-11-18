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
    url = r'https://star.ettoday.net/news/1200436'
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
            弘大三巨里肉舖(三叉口肉舖)是YG娛樂開的烤肉店,喜歡BigBang或者
            旗下藝人例如2NE1、PSY、Epik High等的朋友,都可以到這裡碰碰運氣,說不定可以碰到他
            們在這裡吃飯。他們有一個照片打卡牆,上面就是滿滿明星自拍照! 然後話說,其實在韓國
            吃燒肉的選擇實在多到爆炸,各家都有不同的支持群,也有很多吃到飽的超多人推薦,總之多
            去幾次就都吃過一輪囉! 其實我一直對於有明星光環加持的店不會說特別感興趣就是了,但,
            有的時候還是要嘗試下啊! 我們平日中午用餐,人不多。店員也不多就是了。 肉肉放在很
            明顯看得到的外面,在冰箱內。這樣感覺比較值得被信賴。 由於是YG娛樂,所以有播放音樂
            MV 兩人份的話現在就特價40000韓元有找。有肉肉三種,泡菜鍋,炒飯跟汽水,以這樣的份量
            兩人吃就很夠了喔 先看一下小菜,認真來說就一樣小菜,青蔥,生菜跟蒜頭辣椒等等算是配
            烤肉的,不過我覺得這比吃到飽的品質好,尤其生菜,芝麻葉,小白菜我覺得不錯。 先來鍋
            泡菜鍋,這湯蠻好喝的! 三種肉,兩個人一起吃我覺得差不多算剛好。 整體來說,我覺得
            還不錯,畢竟肉是有一定品質,但服務上我覺得很冷淡啊~不知道為啥就是一種面表情的服務
            態度。我還是比較喜歡有大媽服務的烤肉店,那感覺有差啊。
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530158400
    assert parsed_news.reporter is None
    assert parsed_news.title == '快朝聖!只營業到六月底 YG娛樂開的韓國烤肉店'
    assert parsed_news.url_pattern == '1200436'
