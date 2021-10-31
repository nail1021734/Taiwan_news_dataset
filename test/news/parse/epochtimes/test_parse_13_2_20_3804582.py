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
    url = r'https://www.epochtimes.com/b5/13/2/20/n3804582.htm'
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
            一年一度的加拿大國際車展,再次受到車迷們關注。人們饒有興趣地觀看各種類型的汽車:
            超前的、現代的、實用的、環保的等等,當然,更少了古典的老爺車。在車展上展出的老爺車
            多為加拿大安省的私人收藏車。 车主:
            Steven Bloom, 73 Chagal Drive Thornhill, Ont 车主:
            Jules Saari, 8 Costen Blvd St. Catharines, Ont 车主:
            Alex McClure 11 Peebles Drive Freelton, Ontario 车主:
            Frank Mitchell, 2164 Country Club Drive Burlington, Ontario 车主:
            Paul Hopla 24 Lynvalley Crescent Toronto, Ont。 车主:
            Paul Hopla 24 Lynvalley Crescent Toronto, Ont。 车主:
            Paul Hopla 24 Lynvalley Crescent Toronto, Ont。 Robert & Fiona You
            ng 3 Fantail Court Whitby, Ontario。
            '''
        ),
    )
    assert parsed_news.category == '科技新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1361289600
    assert parsed_news.reporter == '多伦多'
    assert parsed_news.title == '2013加拿大國際車展 老爺車風光无限'
    assert parsed_news.url_pattern == '13-2-20-3804582'
