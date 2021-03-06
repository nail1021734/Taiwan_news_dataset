import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/19/12/5/n11702000.htm'
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

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            古代朝鮮半島上新羅國,曾有個第一貴族叫金哥,他的遠祖名叫旁箎。話說當年旁箎和弟弟分
            了家,旁箎好心禮讓弟弟,家財分得少,地也都給了弟弟。結果過了一些日子之後,哥哥漸漸
            缺衣少食的,家裡也沒有土地可以拿來耕種,只得四處求乞過日子。旁箎的弟弟雖然有錢,但是
            心腸硬,從來不肯周濟哥哥。 有一年,村裡人看旁箎實在可憐,就送給他空地一畝,讓他也能
            耕種,耕種後能有收穫好度日。旁箎就去向弟弟借點蠶種和穀種來養蠶、耕種。可是弟弟卻
            暗地裡把蠶種和穀種都蒸熟了才送給他。旁箎一點也不知道,高高興興地拿著蠶、穀種子回去
            了。 到了養蠶的季節,旁箎學著鄰居的做法,小心翼翼地孵蠶種,終於養出一條蠶來。這蠶兒
            竟然長得很快,一天大一寸,十天工夫,大得像一頭牛,一天要吃好幾棵桑樹的葉子,還吃不飽
            呢。 旁箎的弟弟知道了,氣得鼻子裡直冒煙,就趁哥哥不在家的時侯,去把這條大蠶殺死了。
            一天後,方圓百里內的人家養的蠶,都飛來落到了旁箎的家,落得滿屋滿地都是雪白的繭子。
            大家這才知道,被殺死的蠶原來是蠶王。鄰居們都一起到旁箎家來繅絲,日也繅,夜也繅,總是
            繅不完似的。 再說,旁箎把蒸熟的穀種播下以後,也只長出一株稻子來,不過那稻穗竟然有
            一尺多長。旁箎天天到田頭守護著那一株稻子。一天,忽然飛來一隻鳥,一霎眼的工夫,就折了
            稻穗銜走了。 旁箎拚命追趕著飛鳥。飛鳥把他引進了深山,他一路不停地追到山裡去。大約
            走了五六里山路的光景,飛鳥就鑽到一條石縫裡去,不見了。 這時太陽西沉,漸漸地遠近大地
            一片漆黑,道路也辨認不出來了。旁箎鑽不進那個石縫,只好守在石縫外面,靠著一塊大石頭
            坐下了。 半夜裡,一輪皓月高高地掛在天上,照得遠近像白晝一般。他看見一群穿著紅衣的
            小孩來到那兒玩耍。其中一個小孩問:「你要什麼東西嗎?」一個小孩回答:「我要喝酒。」
            第一個小孩就拿出一枚金錐子來錘擊石頭,不一會兒,酒和酒杯都出來啦。另一個小孩說:「
            我還要些吃的東西。」小孩又用金錐子來錘擊石頭,不一會兒,熱騰騰的飯菜、糕餅都擺在
            石頭上面了,小孩子們就在山上歡歡喜喜地吃了一餐,過了好久才離去。 離開時,小孩將那枚
            金錐子插在石縫裡,忘了拿走。旁箎見到閃閃發亮的金錐子,高興極了,等到天亮以後,就把它
            拿回家裡來。 從這以後,他隨便要什麼東西,只要用金錐子敲擊兩下,東西馬上就會出現在
            面前,要啥有啥。這樣一來,旁箎就成了全國最富有的人了。 旁箎倒很惦記他弟弟,常常送一
            些珍珠寶貝給他,使弟弟也成了聞名的富翁。弟弟這才懊悔自己不該用蒸熟的種子欺騙哥哥
            。 可是沒過多久,弟弟卻又異想天開,跑去對哥哥說:「哥呀,你也把蒸熟的蠶種、穀種當作
            好種來騙騙我吧,說不定我也跟哥一樣能得到金錐子呢?」 旁箎覺得弟弟的想法實在太蠢了,
            趕緊勸他不要這樣想。可是說乾了嘴巴,他還是聽不進去,就只好照著他的話去做,給了他弟弟
            一點煮熟了的蠶種和穀種。 弟弟用那些蠶種養起了蠶,可是只得到一條平平常常的蠶。弟弟
            用那些蒸熟的穀種子種起了穀子,可是只得到一株普普通通的稻。 這株稻子快要成熟時,一天
            ,不知打哪又飛來一隻鳥,把稻穗折斷,銜走了。弟弟高興得不得了,連忙跟著飛鳥一起進山。
            到了鳥兒棲息的地方,不料卻遇到一群青面獠牙的鬼怪。鬼怪氣勢洶洶地說:「原來你就是偷
            我們金錐的人!」 說著,就把他抓了起來,一面大聲責問:「你願意替我們築一道二十四尺高
            的池塘堤岸呢,還是願意把你的鼻子拉成一丈來長?」 弟弟要求讓他做苦工,築池塘堤岸。
            他拼死拼活地做了三天,又飢又渴,全身一點力氣都沒有,塘堤還是築不起來,只好苦苦哀求
            鬼怪饒恕他。於是,鬼怪就把他的鼻子拉成一丈來長,跟象的鼻子一樣。 弟弟拖著一丈來長
            的「象鼻子」逃下山來,人們見了覺得非常奇怪,一傳十,十傳百,都爭著趕來觀看這個醜八怪
            。弟弟又是羞愧,又是怨恨,生起病來,不久就死了。 後來,旁箎的子孫開玩笑,故意用金錐去
            敲擊石頭,祈求狼糞,不料一陣雷響,狂風四起,金錐也就不知到哪裡去了。
            '''
        ),
    )
    assert parsed_news.category == '文化網,預言與傳奇,神話傳說,中國民間故事'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1575475200
    assert parsed_news.reporter is None
    assert parsed_news.title == '貧富兩兄弟的見證 好心和壞心結異果'
    assert parsed_news.url_pattern == '19-12-5-11702000'
