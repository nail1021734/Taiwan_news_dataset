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
    url = r'https://star.ettoday.net/news/1200563'
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
            護理師不是禮儀師!超繁瑣的「技能準則」曝光 網友都怒了 護理師難為!臉書粉絲專頁《
            靠北護理師》PO出一張護理師的「服務技能準則要點」,讓許多網友都怒了,就連律師呂秋
            遠也在臉書轉發批「護理師不是禮儀師,真的不需要這麼多繁文縟節。」
            '''
        ),
    )
    assert parsed_news.category == '來了'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530095880
    assert parsed_news.reporter is None
    assert parsed_news.title == '難為!超繁瑣的護理師「技能準則」曝光 網友怒了'
    assert parsed_news.url_pattern == '1200563'
