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
    url = r'https://star.ettoday.net/news/2100233'
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
            全聯先前推出「貓咪生吐司」大受好評,也成為消費者在疫情期間的新寵兒;如今更與台灣
            知名飲品店老虎堂合作,推出2款「READ BREAD X老虎堂」聯名生吐司,包括療癒造型的
            「虎虎生吐司」及肉桂控必買的「黑糖肉桂生吐司」,預計再搶下網路人氣話題。 全聯
            自去年開始經營READ BREAD生吐司系列商品,以不須預約、不用排隊、風味不打折的特色,
            成為婆媽們的心頭好。洞悉市場趨勢,展開「生吐司進化史」,除了原味也發展各式口味的
            選擇,像是抹茶、義式青醬、燕麥奶,今年則有貓咪造型生吐司、包餡生吐司,像是金沙肉鬆
            、芋泥等,滿足消費者味蕾,開賣至今陸續推出共8款商品,累積已賣破超過1000萬片,銷售
            金額超過1億5000萬元。 看好生吐司市場,10/15~11/18 攜手知名手搖飲品牌老虎堂
            TIGER SUGAR,推出2款聯名新品。2017年誕生的老虎堂,最大特色是使用虎式黑糖取代
            果糖、鮮奶取代奶精,訴求療癒感,曾一度引領黑糖虎紋風潮。老虎堂選用台灣在地黑糖為
            原料,以台灣古法熬出的虎式黑糖,用17斤紅蔗糖才能熬出1斤純黑糖,熬成的濃濃琥珀色,
            最讓消費者喜愛。 全聯「READ BREAD X老虎堂」新品限定販售35天,2款商品之一為
            吸睛的造型吐司「虎虎生吐司」,使用老虎堂虎式黑糖,味道濃郁回甘,並結合天然奶油製成
            生吐司,外型可愛,風味層次令人愛不釋口,勢必再創造一波DIY熱潮。 另一款為
            「黑糖肉桂生吐司」,嚴選老虎堂虎式黑糖並與日本第一大香料品牌GABAN結合,嚴選來自
            越南最頂級的肉桂品種,擁有清爽香氣及燒甜滋味,結合生吐司體,詮釋傳統與時尚的全新
            融合。 全聯表示,READ BREAD生系列商品共有3大類別,包括生吐司、生貝果、生鬆餅,
            銷售佔比以生吐司最大宗佔有7成,可謂後起之秀,非常受到矚目,像是生吐司以高含水量
            、吐司邊Q軟,加上無添加人工色素及防腐劑的特點,受到消費者青睞,是該系列的銷售冠軍,
            販售金額累計超過1億元。 值得一提的是,先前因疫情苦悶,三級警戒期間,不少民眾也會
            在家找樂子,根據銷售發現,療癒型的貓咪生吐司逆勢成長,在網路上聲量頗高,許多消費者
            發揮創意將貓咪吐司神改造,搭配果醬、巧克力醬、水果等食材,變身成栩栩如生的貓咪
            、少女,疫情期間賣出1000萬的業績。
            '''
        ),
    )
    assert parsed_news.category == '民生消費'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634103960
    assert parsed_news.reporter == '林育綾'
    assert parsed_news.title == '全聯推出超療癒「虎虎生吐司」!加碼肉桂控必吃黑糖肉桂生吐司'
    assert parsed_news.url_pattern == '2100233'
