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
    url = r'https://star.ettoday.net/news/1200335'
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
            韓劇《金祕書為何那樣》中帥氣傲嬌的副會長朴敘俊是不是也撩動你的心?還記得在第三集
            中金秘書背著副會長前往相親的劇情嗎?TiffyWu韓國美好計畫就在《旅遊超爽的!》社團分
            享劇中相親男帶著金秘書排隊享用的知名豬排店! Himesiya日式食堂就位於年輕人的逛街
            聖地「弘大」,搭乘地鐵、從弘大8號出口前往,很方便!一路上還會經過《舉重妖精金福珠
            》愛吃的烤肉店、Running Man拜訪過的便宜炸豬排,這一條街的餐廳可都是有明星光環加
            持呢! 這一家日式食堂除了販售豬排,還有招牌丼飯、壽司、烏龍麵及咖哩系列,菜單上附
            有圖片,就算不懂韓文,用手指一比,也能輕鬆點餐。 Tiffy親自到訪也揭開了韓劇的「真實
            面」!為配合劇情效果,金秘書享用的炸豬排是沒有販售的,於是Tiffy點了最相近的「咖哩
            豬排飯」,與劇中有落差的還有相親男貼心將切好的塊狀豬排遞給金秘書,卻讓她頓時想起
            副會長朴敘俊的劇情,劇中角色是使用刀叉食用,但實際上店家提供的餐具是筷子跟湯匙,雖
            然無法百分之百複製場景,但是豬排的美味卻是不打折! 受到注目的金黃豬排果然沒讓
            Tiffy失望!她分享「剛起鍋的厚實豬排熱呼呼的還在冒煙,皮薄酥脆,肉質不乾硬,是在韓國
            吃過最好吃的豬排」,濃稠的咖哩帶點辣勁很下飯,忍不住一口接著一口,吃不夠還能續飯
            續醬呢!
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530320460
    assert parsed_news.reporter is None
    assert parsed_news.title == '韓劇《金秘書》相親的豬排店!搭濃稠咖哩可續飯續醬'
    assert parsed_news.url_pattern == '1200335'
