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
    url = r'https://www.ntdtv.com/b5/2011/04/12/a517801.html'
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
            自從311大地震後,不斷召開記者會,向國民交代救災及核事故情況的內閣官房長官枝野幸男,
            走出會議室來到街上,親自品嘗福島縣的草莓和番茄,並強調這些食物是安全的。 4月12日,
            日本官房長官枝野幸男出席在東京舉行的福島縣磐城市農產品展覽,親自品嘗草莓和番茄,
            他表示,獲准在巿面出售的食物均是安全,可以放心食用的。同場還以輻射探測機,以證實
            這些食物未受輻射污染,並希望國民通過消費支援災區。 共同社報道,磐城市部分地區處於
            福島第一核電站方圓30公裡範圍內,一些證實安全的蔬菜,價格仍然下跌。
            '''
        ),
    )
    assert parsed_news.category == '天災人禍,各國地震,日本地震'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1302537600
    assert parsed_news.reporter is None
    assert parsed_news.title == '枝野幸男親嘗福島番茄 強調食物安全'
    assert parsed_news.url_pattern == '2011-04-12-517801'
