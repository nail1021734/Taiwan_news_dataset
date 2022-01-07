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
    url = r'https://www.epochtimes.com/b5/13/1/6/n3769836.htm'
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
            讀者Simon問:李先生,您好。我的車是2001年 Chrysler Intrepid 2.7。近來開熱風的開始
            幾分鐘總有很難聞的氣味。不知道是不是因為多年沒更換車廂空氣過濾器(Cabin Air Filt
            er?)的緣故。如果是的話,應如何更換?我查了說明書,沒有此方面的內容。謝謝。 李進答:
            Simon 您好。2001 Chrysler Intrepid 可能沒有車廂空氣過濾器。難聞的氣味原因可能是
            :1) 空氣入口處有臟東西需要清除。2) 空氣入口閥門失效。 (新鮮/循環的控制
            失靈)3) 暖氣的水管可能有滲漏,熱冷卻液被蒸發掉導致難聞的氣味。4) 冷氣的凝結水
            排泄管道堵塞,造成潮濕而產生發黴。需要清潔排水管道。 讀者Thomas問:你好!謝謝你曾
            二次滿意地解答了我的問題。我的2006年出廠的Toyota RAV4 V6。最近,當車起動後,
            轉動方向盤時,會聽到「cook、cook」的什音,行走過程中則一切正常。請問是什麼原因?
            嚴重嗎?是否要立即去撿修?請回答! 李進答:您需要首先確定聲音是來自何方?是方向盤
            本身的聲音呢?還是前輪的下方的聲音? 如果是方向盤本身的聲音,請檢查方向盤內部的軸承,
            和方向盤轉向電路旋轉接頭是否需要潤滑或維修。 如果怪聲是來自前輪下方的,請修車師傅
            檢查驅動軸的萬向節(CV Joint),轉向系統的各個連桿和連桿球節(Ball Joint) 沒有
            鬆動或損傷。還有需要檢查的是轉向系統的齒條/齒輪(Rack and Pinion) 是否因哪個地方
            磨損而造成噪音。
            '''
        ),
    )
    assert parsed_news.category == '科技新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1357401600
    assert parsed_news.reporter is None
    assert parsed_news.title == '汽車維修問與答 – 難聞氣味'
    assert parsed_news.url_pattern == '13-1-6-3769836'
