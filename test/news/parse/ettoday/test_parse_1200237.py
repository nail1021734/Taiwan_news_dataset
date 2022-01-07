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
    url = r'https://star.ettoday.net/news/1200237'
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
            寬鬆是近年來不停地佔據時尚版面的重要詞彙,有別於合身的服裝,刻意不符合身形的剪裁
            才是能與時髦畫上等號的設計。謹記這樣的概念,不同單品只要能以 Oversize 的形式表現
            就可以穿出趨勢的寬鬆搭配。 先前也曾介紹過以寬褲為重點搭配的寬鬆感造型,本回則是
            要以每個人在夏天時都會必備的 T-shirt 單品為主題,看看日本男生是如何將簡單的
            素面 T-shirt,利用其不合身的版型穿出簡約卻充滿個人特色的寬鬆穿搭。 寬鬆還是有
            精神 純淨的白色 Oversize Tee 為肌膚打上好氣色的自然光澤,寬大的版型搭配同屬寬鬆
            系列的寬褲,日本男生最擅長的寬 X 寬穿搭技巧,簡單完成日系街頭的青春風格。 下擺及膝
            也沒問題 落肩的設計搭配上相當寬鬆的袖口及下擺,搶眼的 Oversize 款式展現了高度的
            特色感。想利用寬版 T-shirt 作為整體的穿搭重點,其餘的單品就可以以不搶戲的黑色為
            配角選擇。 倒三角體格效果 All Black 的單一色調可以為休閒感短褲穿搭減去幾分隨興
            的氣息,而利用 Oversize Tee 還能營造出倒三角的體格效果。活潑健康的形象用全黑
            單品也可完成。 低調沉穩休閒感 怎麼穿都還是大地色系T-shirt 的話,今夏就選擇沉穩
            色彩與寬鬆版型的 Oversize Tee穿搭吧!酒紅色調低調地表現衣著的明亮感,0 束縛的
            上身與丹寧褲一起組合出輕鬆的日常衣著。 反差的童趣印象 除了將衣襬自然擺放之外,紮進
            褲子內的穿搭法也別有一番趣味性。落肩的袖子使手臂線條顯得溫柔不造作,對比刻意收乾淨
            的衣襬,兩處的反差增加了穿搭的童趣印象。
            '''
        ),
    )
    assert parsed_news.category == 'fashion'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1531087620
    assert parsed_news.reporter is None
    assert parsed_news.title == '日系男生搶搭Oversize潮流 越寬越有個性'
    assert parsed_news.url_pattern == '1200237'
