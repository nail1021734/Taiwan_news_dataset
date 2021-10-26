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
    url = r'https://www.ntdtv.com/b5/2011/04/16/a519478.html'
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
            4月14日,皇家近衛騎兵團(Household Cavalry)在位於倫敦市中心海德公園附近的兵營
            進行演練,為臨近的英國王子威廉和凱特的王室婚禮做準備。
            '''
        ),
    )
    assert parsed_news.category == '海外華人,歐洲'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1302883200
    assert parsed_news.reporter is None
    assert parsed_news.title == '為王室婚禮演練的皇家騎兵'
    assert parsed_news.url_pattern == '2011-04-16-519478'
