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
    url = r'https://www.ntdtv.com/b5/2012/01/01/a640251.html'
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
            12月30日昆士蘭中部發生了一起意外事故,在事故中喪生的是一名省急救服務中心(SES)的
            志願者,在2010-2011年洪災中廢寢忘食救災的英雄。 據澳新社的消息,這名在意外事故中
            喪身的男子名叫史蒂文斯(Matthew Stevens),年僅28歲。30號晚上6:30左右,他在
            西奧多(Theodore)的消防站維修消防車底盤時,恰逢消防隊有任務出發,結果消防車意外
            碾過史蒂文斯,釀成悲劇。 當地居民說,作為省急救服務中心的志願者,他在2010年12月的
            洪水中表現非常出色。當時西奧多三分之二的房子都在水中浸泡了20多天。數以百計的居民
            在直升機的救援下撤離。史蒂文斯當時一直在幫助別人從家中撤離,即使自己的房子也已經
            被水淹到。 週六(31日),昆省消防局代局長麥肯齊(Iain MacKenzie)探望了死者家屬
            並帶去了全體急救成員的慰問。他說:「消防員們和當地居民對這樣一個在洪水期間救人於
            危難的志願者的死訊表示沉痛哀悼。西奧多是一個團結的社區,這起事故會使我們銘記在心。
            」 據瞭解,事故仍在進一步調查之中。
            '''
        ),
    )
    assert parsed_news.category == '海外華人'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1325347200
    assert parsed_news.reporter is None
    assert parsed_news.title == '昆省救災英雄意外喪生 社區哀悼'
    assert parsed_news.url_pattern == '2012-01-01-640251'
