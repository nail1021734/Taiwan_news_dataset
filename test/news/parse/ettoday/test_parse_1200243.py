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
    url = r'https://star.ettoday.net/news/1200243'
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
            受試者為設計師,設局者為委託人,請設計師為他製作橫幅廣告,兩人共同合作完成
            工作。 要求A組設計師:每次提案都要準備一款橫幅廣告設計,每次都請委託人提出意見。
            來回共討論了六次。(共設計了六款橫幅廣告) 要求B組設計師:每次提案都要準備三款橫幅
            廣告設計,請委託人針對每一款提出意見,來回共討論了兩次。(共設計了六款橫幅
            廣告) 結果 B組製作的橫幅設計獲得好評,點閱數也較高。 接著詢問設計師:「委託人的
            意見有參考價值嗎?」 A組設計師 35%回答:「有。」但是超過50%的人感覺
            「被挑剔」。 B組設計師 80%回答:「有。」其中有人因此對自己的設計能力更有
            自信。 由此可知,一開始提出數種方案,較容易產生良性互動。 提出企畫案或簡報資料時,
            大多數人總認為:「拿出最好的成品是員工的職責所在。」 但是,只提出一種方案,就必須要有
            心理準備,你所提出的企劃案結果可能很危險。因為負責審閱的人必須被迫在「YES」與
            「NO」之間做抉擇,而為了不傷害你的自尊,他們很可能耗費心思提出更麻煩的要求,或是拐彎
            抹角將企畫案打回票。 這不能怪任何人,因為讓會議桌上只有一個方案是非常不智的。如果
            希望企畫者與審閱者能氣氛融洽的開會討論,就不該只提出「一件嘔心瀝血的方案」,而應該
            提供「數種粗略的草案」,讓大家有思考討論的空間。 若是有好幾種備案,就比較可能產生
            正面的意見,例如,可能會出現「這一案的這一點和另一點組合起來,感覺很不錯」,或是
            「這一案最接近我想要的感覺,但若是再加強這方面也許就更好了」,像這樣多種備案不僅
            能讓專案進展順利,也能提高企畫的品質。製作資料也是如此,與其反覆寫了又刪,不如大致
            提出三種方案讓對方可以進行比較,以便打造出完美的成品。 提案時,至少提出三種構想。
            '''
        ),
    )
    assert parsed_news.category == '健康'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530167880
    assert parsed_news.reporter == '池田貴將'
    assert parsed_news.title == '提案老被打槍?專家剖析「提3種構想」開會氣氛好、省去客戶刁難'
    assert parsed_news.url_pattern == '1200243'
