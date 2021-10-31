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
    url = r'https://www.epochtimes.com/b5/13/2/20/n3804661.htm'
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
            在每年的加拿大國際車展上,在各類汽車展區中,最光采奪目、最吸引人的還要數超級跑車區。
            超级跑车,意味着真正的风驰电掣,是跑車中的精品,象徵著極速、豪華、現代與時尚,是車迷
            們心中的夢想汽車。能在車展上見到各款超級跑車,也算不枉此行。此次參展的超級跑車中,
            有蓮花、法拉利和菲斯克等,它們都是超級跑車中的佼佼者。 法拉利超级跑车展区 超级
            跑车菲斯克 超级跑车莲花 阿尔发罗密欧超级跑车
            '''
        ),
    )
    assert parsed_news.category == '科技新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1361289600
    assert parsed_news.reporter == '多伦多'
    assert parsed_news.title == '2013加拿大國際車展 超級跑車奪目耀眼'
    assert parsed_news.url_pattern == '13-2-20-3804661'
