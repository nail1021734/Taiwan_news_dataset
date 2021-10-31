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
    url = r'https://www.epochtimes.com/b5/13/3/4/n3814165.htm'
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
            以色列國防部長巴拉克說,伊朗核項目是以色列、中東和世界所面臨的最大挑戰,在應對伊
            朗可能研製核武器這一問題時,不能排除任何一種選擇方案。 星期天,巴拉克在華盛頓召開
            的一次會議上說,雖然伊朗面對著前所未有的外交努力和制裁,但他並不認為伊朗統治者會
            放棄其“核野心”。 以色列和西方國家懷疑伊朗打著民用核能項目的幌子研製核武器,而伊
            朗否認這一指稱。德黑蘭說,伊朗的核項目只是用於和平目的。 以色列總理內塔尼亞胡和
            美國副總統拜登定於星期一對美國以色列公共事務委員會發表演講。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1362326400
    assert parsed_news.reporter is None
    assert parsed_news.title == '以色列防長:伊朗核項目是世界最大挑戰'
    assert parsed_news.url_pattern == '13-3-4-3814165'
