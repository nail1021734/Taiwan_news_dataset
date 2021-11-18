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
    url = r'https://star.ettoday.net/news/2104823'
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
            只要有得吃,就算要洗澡也在所不惜!薩摩耶「噗優」的馬麻這天帶著毛孩去公園玩耍,沒想到
            貪吃的噗優一看到池塘裡的魚兒們有吐司可以吃,立馬不管三七二十一就想跳進水中跟牠們
            搶食,媽媽眼看著岸邊的毛孩蠢蠢欲動的樣子超緊張,不斷嘶吼要牠趕快離開,但一心只有
            吐司的噗優根本聽不進去,直接把四條腿默默泡進水中。 「你們有看過為了跟魚搶吐司然後
            下水的薩摩耶嗎?沒有的話,這裡有一隻。」畫面中可以看到,當時噗優發現有人在餵魚吃
            吐司後,就露出一臉貪吃的表情虎視眈眈,怎料媽媽才一轉眼,噗優就已經衝到池塘邊準備
            下水跟魚搶食物,甚至還真的走進水裡,呆呆地站在池塘中露出燦笑,讓媽媽超頭痛,崩潰狂
            喊求牠趕快上岸,所幸毛孩最後終於聽話離開水裡,才讓馬麻鬆了一大口氣! 飼主經常在臉書
            粉專「雪橇犬麥可噗優和緬因喬鈮喵」分享毛孩日常,這次將影片PO到社團「有點毛毛的」後
            ,網友看了也全都笑噴表示,「麻麻快瘋了」、「噗優好客氣哦!沒有整個泡進去」、
            「欸...可惜了!沒看到我最想看到的一幕」、「要洗澡了」、「往草地丟一塊麵包牠
            肯定就上去了啊XD」、「噗優優:這就是『對吃的堅持』」。
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634638500
    assert parsed_news.reporter == '陳靜'
    assert parsed_news.title == '為了跟魚搶吐司衝下水! 「4條白腿泡池塘」媽崩潰嘶吼求上岸'
    assert parsed_news.url_pattern == '2104823'
