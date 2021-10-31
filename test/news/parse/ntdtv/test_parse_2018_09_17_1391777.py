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
    url = r'https://www.ntdtv.com/b5/2018/09/17/a1391777.html'
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
            超強颱風山竹過境香港時,造成當地嚴重浸水,樹木被吹倒。並造成超過300人受傷。 記者:
            史上最強的颱風吹襲香港,十號風球下尖沙嘴碼頭是風大浪大,我站在這裡需要扎緊馬步才能
            站穩。 山竹來勢洶洶。十號風球下,尖沙嘴海傍,大浪衝上岸,地面水浸,垃圾桶被強風吹倒
            在地,天花板也破裂。雖然風暴潮令海陸空交通基本癱瘓,不過,有市民仍冒著危險到海旁
            追風。 香港市民:「搭地鐵過來的。難得一見看這個,十號風球 香港市民:
            「六十歲人第一次來(追風)。留三分鐘左右就走了,不會太久,因為安全問題。」 印度裔
            港人哥佬:「我從來沒有看到這麼大的風,我經常來這邊,水沒有這麼高,我第一次看到
            水都差不多衝上岸。」 去年颱風「天鴿」重創後,港島杏花村居民雖然一早做好防護措施,
            但難敵強風。巨浪達幾層樓高,海水淹沒屋苑低層,水深到腰。部分大廈停電停水。 紅磡海濱
            廣場幕牆爆開,大角咀樓盤發生天秤倒塌事件。風暴過後,旺角彌敦道外到處塌樹,招牌、
            外牆跌倒在地,一片狼籍。 香港歷史上共有11次十號風球,但山竹威力最大,中心時速高達
            175公里,部分地區更達256公里。截至晚上11點,共有300多人在風暴中受傷。教育局宣布,
            所有學校週一會停課。
            '''
        ),
    )
    assert parsed_news.category == '港澳'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1537113600
    assert parsed_news.reporter == '梁珍,王仲明'
    assert parsed_news.title == '「山竹」肆虐香港災情慘重 逾300人受傷'
    assert parsed_news.url_pattern == '2018-09-17-1391777'
