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
    url = r'https://www.ntdtv.com/b5/2011/06/11/a545215.html'
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
            受到台灣塑化劑風波影響,在馬來西亞從事進口台灣食物的台商,銷售額在2個多星期間掉了
            2成,至於重建消費者對台灣食品的信心,台商預估需要約半年時間。 台商林皇成從2005年
            開始,從事進口台灣和日本食品的貿易,在台灣食品部份,他主要進口罐頭、泡麵和飲料
            ,供應馬來西亞3個連鎖大賣場。 台灣甫爆出黑心起雲劑事件後,他即接到大賣場要求在
            一星期內提供SGS證書,否則將把食品全數下架。 林皇成雖然在限期內成功地向台灣批發商
            取得SGS證書,代理的食品所幸沒有被下架,但消費者對台灣食品的信心卻已動搖,影響了
            大賣場的進貨量。 在塑化劑風暴發生前,林皇成的銷售額約新台幣300萬元,但在短短2個
            多星期內就跌到240萬元。而且林皇成原本已和一家大賣場達成合作協議,在7月舉辦台灣
            食品展,如今受到市場不景氣影響被迫取消。 為挽回馬國消費者對台灣食品的信心,林皇成
            表示,馬國大賣場已計劃聯合所有台灣食品進口商,一起籌辦台灣食品促銷活動。 另一方面,
            馬國台商聯合會總會長杜書垚指出,在馬國從事進口台灣食品的台商不多,而且也沒有代理
            遭到污染的食品,但是台商在馬國的形象還是受到影響。 不過,他不忘稱讚中華民國政府,
            在處理塑化劑風波上非常透明和追究到底的精神,讓民眾的傷害降到最低。
            '''
        ),
    )
    assert parsed_news.category == '財經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1307721600
    assert parsed_news.reporter is None
    assert parsed_news.title == '馬國台灣食品 銷售額跌2成'
    assert parsed_news.url_pattern == '2011-06-11-545215'
