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
    url = r'https://www.epochtimes.com/b5/19/12/28/n11751782.htm'
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
            伴隨著氤氳的香氣,一個女娃誕生了,從此她的世界與芳香結下不解之緣。她的雙眼能看到
            別人看不到的景象,小小年纪便能預知生死...... 明朝時期,劉家婦人羅氏夢到五彩的祥雲
            ,自天上簇擁著一個穿著絳紅衣裳的仙女,飄然降於劉家,羅氏不久即懷孕。羅氏懷孕十個月間
            ,家中始終飄散著一股瀰漫不絕的奇香。 後來,她又夢到白衣神女為她送來一個女兒,嘉靖
            四十二年(1563年,癸亥年)冬天,羅氏生下一個女孩。女嬰出生後,家中瀰漫的香氣更加濃郁
            ,於是為她取名「香姑」。 香姑容貌端莊,神情肅穆,天資聰穎,很有辯才,天性孝敬父母
            。 劉家住在舊蓮子胡同。有一次,小香姑出門卻迷了路,幸好遇到一位白衣女子,抱將她回家
            。但小香姑回到家一開門,白衣女子就消失不見。 然而,她從周歲到十歲,沒有一年不得病的
            ,並且時常做惡夢,夢到鬼祟作怪,幸得觀音菩薩救濟,才得以解脫。她的母親問起菩薩的形貌
            。小香姑說:「菩薩頭戴珠冠,穿著一身花袍,手中還拿著鐵鞭。用鞭擊打丘龍小鬼,就是那些
            作祟的小鬼。」 每次生病時,小香姑就在胸前雙手合掌,不斷地高聲呼喊道:「菩薩,菩薩!」
            羅氏問她,她說:「這是菩薩教我這樣做的。」 二月十九日那天,小香姑忽然問起母親:「今天
            是不是我的誕日?」母親告訴她:「是啊!」話音剛落,家中再次瀰漫起一股濃郁香氣。再看
            小香姑的舉止,就像在迎神、送神一般。其母知道是菩薩降臨家中了,而這時家中的几案壁上
            ,布滿了粟米般的甘露,顆顆分明。小香姑說:「這是菩薩用楊柳枝揮灑出缽中的水。」 小
            香姑十一歲時,忽然疾病大作,她對母親說:「菩薩今天來了,孩兒要離去了。孩兒無所戀,惟
            戀雙親啊!」全家人為此嚎啕大哭。 小香姑沐浴更衣後,再盤繞起髮髻,穿上躡雲履,除了常服
            之外,外加白色道袍,手執小角扇。接著小香姑一一拜別雙親與親戚,此時,門外再次瀰漫起
            奇異的芬芳,她知道是菩薩來了,於是雙腳盤坐在室側,身子凝然不動,靜默而逝。此時的小
            香姑容顏更見奇異,如同明珠丹砂,而膚香濃烈猶如檀香。 家人正哀傷時,她的兄長誌儼從
            山西匆忙奔來,說:「我在家正想小憩,忽然看見香姑前來向我道別,『二兄努力功名,妹妹走了
            。』」誌儼所以匆匆趕了回來。 次日,劉家將香姑安葬在順城門外的大光明寺旁。 其母羅氏
            體弱多病,每次生病時,就呼喚小香姑,枕邊隨即散發一陣芳香,她知道是香姑來了,病也就好了
            。此事傳出後,人們遇到危厄,呼喊香姑,就會得到庇佑。類似的事例,不勝枚舉。 後來,劉父
            將房子租賃給江沈寧庵,還沒有來得及遷走香姑的牌位,當天夜裡,沈家僕人在廳上夜宿,看見
            一群美姬叩門而來,邊走邊談笑。沈家僕人還以為是劉的家眷,然而她們的服飾容貌都非人間
            所有,沈家僕人心裡生疑。或許是天上的仙子來會香姑吧。 後來,劉家遷移香姑牌位回家,
            忽然一隻白雀飛入龕內,眾人見狀都感到驚訝。白雀飛去後,墮落了一根羽毛,皎潔如雪,其
            邊緣猶如赤霞。 當時,有一人叫胡玉林,想畫一幅香姑像,但是沒有依據,不知道從何畫起。
            忽然,一天夜裡,香姑現身於玉林夢中,畫作玉林揮筆立就,栩栩如生。
            '''
        ),
    )
    assert parsed_news.category == '文化網,預言與傳奇,神話傳說'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577462400
    assert parsed_news.reporter is None
    assert parsed_news.title == '小香姑傳奇 菩薩送來的小仙女'
    assert parsed_news.url_pattern == '19-12-28-11751782'
