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
    url = r'https://star.ettoday.net/news/1200197'
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
            不用再去文青咖啡廳打卡,簡單一招讓你由內而外變文青! 每到週末全台各地的文青咖
            啡廳總是大排長龍,想拍個文青照都被各種路人亂入鏡,當文青不成還常被人潮搞的心情超
            差,真的很讓人心煩!沒關係,不想去文青咖啡廳人擠人,小編有妙招讓你瞬間變文青,讓我們
            從內在充實文青氣息。新推出的左岸線上咖啡館,貼心的提供了詩集、音樂、插圖等藝文素
            材,佐著咖啡的濃韻,再以手寫字的方式呈現,讓人從頭到腳、從內到外充斥著滿滿的文青感
            啊! IG手寫字網紅亦安在貼文內提及,與左岸線上咖啡館首次合作的專屬手寫字影片已經上線,
            這個特別的合作勾起粉絲強烈的好奇心。 亦安也在貼文中提到,愛情是悠閒的生活中所扮演的
            不可或缺角色,並附上了在線上咖啡館的前10秒預告片段。雖然僅有短短的秒數,但手寫文字
            配合上抒心的攝影作品,馬上就能進入亦安帶來的愛情情境,但才剛剛沉浸而已,影片就立刻
            結束了,只有10秒真的太吊人胃口啦! 想看完整版的文青們不要擔心,亦安在文末也有詳細
            教學,想要體會手寫文字帶來的全部情境,只需要簡單幾個動作,就能在左岸線上咖啡館看到
            完整版的影片囉! 大師級的手寫字
            專家葉曄老師,也在粉絲團上預告已和左岸線上咖啡館合作,推出了專屬左岸咖啡館的手寫
            情詩影片,能夠一邊啜飲咖啡,一邊欣賞優美的書寫文字,真的太令人迫不及待,想一睹這優美
            的意境了! 在線上咖啡館除了能欣賞影片內呈現的優美文字外,也能跟著葉曄老師一筆一捺
            寫出浪漫的情詩,真是讓人從內到外都有著滿滿的文青味啊! 除了手寫字大師,還有許多合作
            意想不到的特別合作即將上線! 左岸線上咖啡館除了療癒的手寫字影片外,也有著詩文、音樂
            等多種藝文素材,之後還有許多名人的專屬合作會陸續上線喔! 各位文青們不要再傻傻地到
            文青咖啡廳排隊了,買杯咖啡、戴上耳機,體會手寫字的筆觸在紙上律動,跟著左岸咖啡館
            靜靜地享受悠閒氛圍吧!
            '''
        ),
    )
    assert parsed_news.category == '民生消費'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530583200
    assert parsed_news.reporter == '左岸咖啡館'
    assert parsed_news.title == '熱門咖啡店爆滿!療癒手寫讓你一秒由內而外變文青'
    assert parsed_news.url_pattern == '1200197'
