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
    url = r'https://www.epochtimes.com/b5/12/8/12/n3657466.htm'
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
            美國宇航局的太陽動力學天文臺(SDO)捕捉到太陽表面一個鞭狀延伸五十多萬公里以
            上的呈現黑色的長弧。在太陽表面出現一個巨大的黑暗結構,這是科學家們以前未曾
            發現的。 那是一條長達500,000公里的黑色條帶或是「裂縫」! 這條黑色區域是由美
            國宇航員拍攝的,美國航天局專家正試圖弄清楚這種異常現象的本質 科學家們稱,這
            極有可能是冷氣體密集,由於磁場的作用停留在太陽表面。它之所以呈暗色,是因為其
            溫度比太陽的溫度低得多。 根據科學家的說法,這很可能是由磁場維持在太陽表面的
            一連串稠密冷氣。 該結構呈現黑色是因為其溫度遠遠低於太陽的溫度。 天體物理學
            家推測太陽上的黑斑是那些溫度較低的區域。然而我們所看到的並不是普通的太陽黑
            子,而且它正在以驚人的速度增長著。 根據研究人員的說法這片區域在僅僅三天內增
            長到差不多50萬公里。 NASA曾預測在2012年9月太陽可能會有空前的爆發。預期巨
            大的太陽耀斑可能對全世界造成嚴重的影響。 天體物理學家Daniel Baker評論這一
            「空間氣象」的危險性,稱其效果猶如爆發核戰爭或是巨大小行星墜落到地球。然而,
            對於電力網絡和衛星來說,令專家擔心的並不是耀斑,而是日冕物質拋射,「這很危險,
            或許有一天它們將徹底毀滅我們整個電氣文明」。
            '''
        ),
    )
    assert parsed_news.category == '科技新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1344700800
    assert parsed_news.reporter == '李明宇'
    assert parsed_news.title == '一條50萬公里的「裂縫」出現在太陽表面'
    assert parsed_news.url_pattern == '12-8-12-3657466'
