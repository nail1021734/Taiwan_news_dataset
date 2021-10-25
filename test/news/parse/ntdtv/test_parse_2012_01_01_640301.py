import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.ntdtv
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2012/01/01/a640301.html'
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
            巴基斯坦警方說,許多民眾為迎接新年對空鳴槍慶祝,最大城市喀拉蚩(Karachi)今天有3人
            因流彈喪生,至少60人受傷。 巴國各大城市員警幾乎都加強戒備,以防暴力衝突發生。 在
            南部港市喀拉蚩,數以千計民眾上街跨年,但警方考量到安全,決定制止民眾接近阿拉伯海
            (Arabian Sea)海岸。 巴國警方說:「群眾大年夜對空鳴槍,造成3人喪生。流彈也傷及
            60多人。」
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325347200
    assert parsed_news.reporter is None
    assert parsed_news.title == '巴基斯坦瘋跨年 流彈亂竄3死'
    assert parsed_news.url_pattern == '2012-01-01-640301'
