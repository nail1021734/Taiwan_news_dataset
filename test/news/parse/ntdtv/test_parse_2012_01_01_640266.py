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
    url = r'https://www.ntdtv.com/b5/2012/01/01/a640266.html'
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
            根據美國地質調查局表示,日本當地時間今天下午2時28分發生地震,初步發佈為裏氏7.0級
            ,而後判定為6.8級,所幸未引發海嘯,未造成人員傷亡,核電廠也沒有異常。 据《中央社》
            報導,日本氣象廳指出,地震發生於下午2時28分(格林威治時間0528),震源深度約370
            公里,震央位於東京南方約560公里處的鳥島附近。 根據日本氣象廳,東京都中心、福島縣
            與周圍地區測到震度4。 目前並未立即傳出財物損失或人員傷亡,也未發布海嘯警報。 東京
            迪士尼樂園發言人說:「部分正在步行的民眾並未注意到發生地震」,主題樂園部分設施自動
            停擺後再次照常運作。 東京都內外地鐵和飛機航班未受影響。根據共同社報導,日本北部
            部分高速鐵路服務因地震暫時中斷,不過很快恢復運作。 東京電力公司表示,遭海嘯肆虐
            的福島第一核電廠這次震後未回報任何異常狀況。
            '''
        ),
    )
    assert parsed_news.category == '天災人禍,各國地震,日本地震'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1325347200
    assert parsed_news.reporter is None
    assert parsed_news.title == '日本關東元旦強震 修正為裏氏6.8級'
    assert parsed_news.url_pattern == '2012-01-01-640266'
