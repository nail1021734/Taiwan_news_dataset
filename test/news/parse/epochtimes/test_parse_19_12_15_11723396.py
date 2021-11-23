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
    url = r'https://www.epochtimes.com/b5/19/12/15/n11723396.htm'
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
            前白宮首席策略師、前布萊巴特新聞(Breitbart News)執行主席史蒂夫‧班農
            (Steve Bannon)近日接受了英文大紀元資深記者楊傑凱(Jan Jekielek)在 「美國思想
            領袖」(American Thought Leader)系列節目的專訪。 「在過去的20年裡,中共變得
            更加激進,他們變得更加危險,他們變得更加腐敗,他們變得更像流氓,這是為什麼呢?」班農
            在採訪中說。
            '''
        ),
    )
    assert parsed_news.category == '美國思想領袖'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576339200
    assert parsed_news.reporter is None
    assert parsed_news.title == '班農專訪字幕版'
    assert parsed_news.url_pattern == '19-12-15-11723396'
