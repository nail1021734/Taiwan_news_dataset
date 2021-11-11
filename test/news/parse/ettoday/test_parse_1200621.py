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
    url = r'https://star.ettoday.net/news/1200621'
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
            2018台北國際食品展於今(6/27)盛大開幕,由中美洲經貿辦事處(CATO)
            規劃設立「中美洲館」,邀請尼加拉瓜、貝里斯、薩爾瓦多、瓜地馬拉及宏都拉斯等友邦5
            國,分享各國經典農特產品,如外銷全球的咖啡、海鮮、蔬果以及特色調味醬料、調理食品
            等,讓愛吃愛玩的台灣民眾一站即可周遊列國。活動期間也邀請專業國際創意料理主廚、甜
            點師及調酒師現場示範應用方法,6/27-6/29僅開放海外及本地業者入場,6/30開放一般民眾
            參訪,對中美洲飲食文化有興趣的饕客級吃貨,不妨趁此周末前往南港展覽館認識中美洲異
            國美食。 今年尼加拉瓜帶來豐富的農產品,橫跨糖、咖啡、可可、蜂蜜、蛋品等項目,而蝦
            子也是近幾年輸出全球的主力品項;特別的是,鎖定台灣近幾年烘焙糕點市場興起,尼加拉瓜
            最看好蛋品的潛力市場,自去年8月即由El Granjero集團投入大量資金興建雞蛋處理廠,每
            日可處理進40萬顆雞蛋,成為台灣烘焙業強力後援。 專注於精品咖啡市場的瓜地馬拉,長年
            致力產出高品質咖啡豆,並以外銷日本、韓國、台灣等趨向成熟的高端咖啡市場為主,其中
            阿拉比卡咖啡即是台灣人熟悉愛喝的豆種;近期瓜地馬拉看準全球健康食品市場,特別在展
            覽期間帶來奇亞籽、蜂蜜、夏威夷豆等營養價值高的「超級食物」,期待開拓全新的貿易商
            機。 貝里斯今年帶來風味濃郁的特色辣椒醬,無論作為餐飲佐料或是沾玉米餅食用皆相當
            美味,貝里斯大使對於這款平民佐醬,來到台灣竟在貴婦百貨被當作精品販售感到驚訝,殷切
            希望在台灣找到長期合作廠商直接對台輸出,讓貝里斯的優質醬料,以更合理的價格推廣至
            台灣餐桌;另外,主力農產品與台灣相似的貝里斯,卻更廣泛的製成椰子酒、芒果醬等,令人
            耳目一新。 有別於台灣咖啡多以義式濃縮的飲用方式,薩爾瓦多的咖啡適合純飲,口感猶如
            喝茶般順口、不酸不澀而聞名全球,是許多內行咖啡愛好者的最愛,近幾年台灣需求量也大
            幅提升;今年薩爾瓦多同樣看準健康風潮,力推諾麗果汁及多款特色蜂蜜,薩爾瓦多大使偷偷
            透露,自己最愛搭配燕麥、麵包食用,風味絕佳。 以高品質酪梨、哈密瓜、蝦類等海鮮外銷
            全球的宏都拉斯,今年力推「Granita」咖啡冰沙,這是一種添加牛奶調和的咖啡冰沙,沁涼
            猶如奶昔卻保有濃郁的咖啡風味,由於去年在台北食品展初登場即造成轟動,展期間天天大
            排長龍,因此今年延續這股熱潮持續力推,宏都拉斯大使表示,目前Granita也在美洲市場同
            步興起,希望藉此機會推廣給台灣咖啡業者,一同打造即將掀起的全球性咖啡冰沙旋風。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530169020
    assert parsed_news.reporter is None
    assert parsed_news.title == '吃貨注意!中美洲異國美食來襲 台北國際食品展一站環遊世界'
    assert parsed_news.url_pattern == '1200621'
