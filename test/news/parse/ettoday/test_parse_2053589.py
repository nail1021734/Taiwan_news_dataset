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
    url = r'https://star.ettoday.net/news/2053589'
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
            全聯《料理之王2》團體合作賽火熱上菜,由愛下廚的千田愛紗與「最嚴飛行導師」五星
            主廚王輔立坐鎮。選手端出超強料理,連帝王蟹都拿了出來,讓愛紗吃到發出「WOW」
            驚呼聲;連對料理吹毛求疵的王輔立與阿發師都買單,滿滿海味征服所有導師,拿到全票過關
            。 雙人合作指定料理賽中,選手要做出麵食、湯、小菜套餐組,且要輪流換手,難度相當高
            。選手胡劉柏佑與黃文祈用盡心機使出「犯規絕招」,套餐取名「Sex on the beach」,
            使用帝王蟹、海膽、干貝、九孔、蛤蜊、番紅花等高檔食材,成功擄獲所有導師味蕾。王輔立
            對選手說「你們打安全牌」,好的食材只要不煮得過熟,很難失敗;愛紗也非常稱讚,說出
            「我非常非常喜歡」,更誇讚海味上加入跳跳糖讓她有前所未有的感受。最後,這套由高檔
            食材製作而成的麵食料理獲得全票通過。 雙人合作賽另一組由選手張晉逸和甜點師高仲彣
            組成,相較於其他兩組的忙碌,他們顯得非常淡定,甚至不斷放閃,左一句「你真的好棒」,
            右一句「(菜)跟妳一樣美」,讓主持人Lulu聽了都尷尬,制止說「夠了喔」;廚佛瑞德Fred
            也看不下去說:「你們那組蠻討人厭的,別組那麼忙,你們在那邊談情說愛...」。兩人用甜
            點的方式來製作鹹食,也讓導師相當讚賞。 這次最有看頭的組合之一就是學長姊合作賽,
            第一季學長姊阮紹榮、呂政緯、黃晶晶帶領學弟妹復刻他們上季的經典料理。阮紹榮和吳貞蓁
            搭配製作代代相傳炸子雞,兩人在學校本就是學長學妹,這次「大師兄」阮紹榮傳授這道菜
            難度超高,要在三十分鐘內去骨、油炸到外皮酥脆,很考驗廚師的火候掌控。阿發師吃到
            吳貞蓁的料理後大讚,表示可以在三十分鐘內做到這種火候「簡直是不可能的任務」,其他如
            愛紗和王輔立也都非常佩服這一道菜的呈現。而黃晶晶與蔡至梵合作的「泰泰性感便當」
            結合兩人泰式與日料的專業,也獲得導師一致好評。 共計六回合的團體合作賽,最高積分
            隊伍全數晉級,第二、三名隊伍需要淘汰各三名隊員,究竟誰能挺進最後六強,敬請鎖定
            《料理之王2》節目。 《料理之王2》首席家電贊助商美善品,是讓所有選手和導師都
            讚不絕口的夢幻逸品,在本次比賽當中,廚師們運用它強大的22種調理功能完成任務、
            過關斬將。入圍前六強的選手,就可以將美善品一台帶回家。
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1628913600
    assert parsed_news.reporter is None
    assert parsed_news.title == '雙人合作賽 別隊忙亂這「對」狂放閃! Lulu:夠了喔!'
    assert parsed_news.url_pattern == '2053589'
