import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/12/24/a636565.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            北韓共產領導人金正日去世後,官方媒體大造聲勢說,老百姓為他哭泣,連天地也為之動容,
            狂風暴雪,堅冰爆裂,靈鳥悲愴。然而這一切造神言論,被有過相同經歷的中國人視為荒唐
            可笑的騙人把戲。 金正日離世的這幾天,朝鮮官方媒體一直報導,老百姓如何為失去一位
            偉大的領導人而悲痛傷心。不過據《路透社》消息,這些人是被動員而上街哭泣的。 剛從
            朝鮮逃到韓國的人士反映,如果民眾不掉眼淚,會被人視為忠誠不足,因此不管怎麼樣,還得
            擠出一滴眼淚來。其實,很多人的感覺是,終於結束了,可以放鬆一些了。 大陸作家鐵流表示
            ,凡是專制國家都會出現為獨裁者身亡而哭泣的虛假歷史,毛澤東去世的時候,他正在監獄
            遭受迫害,儘管他心裡很高興,也不得不戴上黑袖章。 大陸作家鐵流:「這就是歷史的假象,
            實際我心裡高興得不得了,覺得毛澤東一死了以後,中國的政治就會發生變化,所以當時9月9
            日,那天我寫了一首詩,這首詩可以代表現在的朝鮮人。『喜聞雪崩冰山倒,試看春水三分嬌,
            有歡不敢呈臉上,背立青紗亦嚎啕。』現在北朝鮮老百姓就這個心情,一個暴君死當然高興
            啦。」 鐵流說,他當時很想放聲大笑,但因為笑了會被加刑,甚至掉腦袋,他不得不放聲大
            哭。 《朝中社》報導說,在金正日死亡的上週六早上,被視為聖地的白頭山天池的堅冰破裂,
            響聲震耳慾聾,白頭山更刮起暴風雪,一只丹頂鶴週二晚上在咸興市的金日成銅像上空盤旋
            三週,在樹梢上低頭停留,十點多才向平壤方向飛去。 號稱「無神論」的共產黨,為甚麼在
            領導人離世時,總會說出一些神蹟呢? 中國歷史學專家李元華表示,在共產極權的國家,他們
            總是編造謊言來表明他們政權的合法性。 中國歷史學專家李元華:「 跟共產極權的本質
            有關,它就是靠騙來做事情的,他對統治下的百姓也是靠騙來維護的,只有這樣,他才覺得這個
            事情可信,在一個封閉的一個環境下,在百姓不了解真相的情況下,它能起到一定作用。」 原
            北京大學新聞與傳播學院副教授焦國標在《當年中國人怎樣哭毛》一文中,列舉了毛澤東去世
            時,很多真哭、假哭、傷心痛哭的例子。 李元華分析,部分老百姓在被矇蔽的狀態下,確實
            以為毛澤東一死,天就會塌下來。 李元華:「不了解真相的百姓也覺得,好像這個世界不能夠
            正常的運轉似的,過後他看了以後,實際上是一種可笑的舉動,有些人還真是由於在中共這種
            謊言的矇騙下,還真覺得世界末日要來了,世界上好像失去了一個偉大的神一樣,實際上是中共
            一手導演的,百姓被欺騙的情況下才發生這種事情。」 李元華還表示,民主國家的人可能
            看不懂為甚麼北韓獨裁者死了,老百姓會哭,有過類似經歷的中國人一眼就能看出其中的因由。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1324656000
    assert parsed_news.reporter == '劉惠,周天'
    assert parsed_news.title == '朝鮮神化金正日 民眾斥騙人把戲'
    assert parsed_news.url_pattern == '2011-12-24-636565'
