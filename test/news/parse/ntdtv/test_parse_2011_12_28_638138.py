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
    url = r'https://www.ntdtv.com/b5/2011/12/28/a638138.html'
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
            位於俄羅斯中部的葉卡捷琳堡市中心的「中國大市場」25日至27日發生大火,導致華商損失
            慘重。警方不排除縱火的火災原因。 據俄羅斯《塔斯社》報導,在西伯利亞地區當地時間
            25日下午2點30分左右,葉卡捷琳堡市中心的「中國大市場」突然發生大火。由於火災面積
            高達4000平方米,倉庫內堆滿了貨物,火勢在26日才被控制, 火災直到27日完全被
            撲滅。 由於火災嚴重,葉卡捷琳堡的郊外都能夠看到市場上不斷冒起的濃濃的黑煙。火災
            發生後,很多中國商家冒著生命危險希望從倉庫內搶救出自己的商品,但被俄羅斯緊急情況
            救援部和消防人員攔住。 到發稿時為止,沒有消息證實有中國人在火災中傷亡。當地消防
            官員瓦列里•烏斯基諾夫對火災未能被迅速撲滅的原因解釋說:「我們在救火中遇到的最大
            困難是消防栓裡的水壓不足,水噴不起來,所以幾乎眼看著火勢蔓延,只在第二天調來了
            消防火車,控制了火勢。」 「中國大市場」是葉卡捷琳堡市最大的市場,佔地4萬多
            平方米,是該地區中國商品主要集散地。由於市場6000多商戶中90%以上是華人,所以,雖然
            上至俄羅斯總統,下至當地政府均多次公開宣佈,俄羅斯禁止出現唐人街,但該中國大市場仍
            被當地人稱為是葉卡捷琳堡的唐人街。 市場上華人出售的貨物幾乎清一色是「中國製造」
            的主要包括服裝、鞋帽、箱包及日用品的輕工產品。而由於目前是冬季,年前的銷售旺季,
            所以很多中國商家大量運來並囤積了裘皮、毛皮服裝,所以倉庫內火災燒毀的貨物大多為
            高貨值商品。有當地華人稱,此次火災導致華商損失至少上億元人民幣。 目前,此次火災
            造成的損失正在進一步調查之中。有關部門表示,將對各種火災發生的可能原因進行調查,
            同時不排除是人為縱火的原因。 近年來,俄羅斯的中國商人聚集的大市場均厄運連連,除了
            莫斯科集裝箱大市場被政府強行關閉,沒收的價值數十億美元華商商品,直到2012年12月份
            被宣佈被銷毀完畢之外,遠東和西伯利亞的大市場也接連發生火災被燒毀。不久前,同中國
            黑龍江省邊境不遠的俄羅斯烏蘇里斯克華人市場也被火災焚毀,警方調查火災原因結果為
            人為縱火。
            '''
        ),
    )
    assert parsed_news.category == '海外華人,歐洲'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325001600
    assert parsed_news.reporter is None
    assert parsed_news.title == '俄葉卡中國大市場火災致華商損失上億'
    assert parsed_news.url_pattern == '2011-12-28-638138'
