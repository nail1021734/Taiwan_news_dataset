import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201912310042.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            立法院會今天上午開始處理反滲透法草案,在昨天朝野協商時,多數條文沒有達成共識,因此
            將在院會中由各黨團依比例推派代表進行廣泛討論、逐條發言,預計將上演
            表決大戰。 立法院長蘇嘉全昨天召集朝野協商,歷經6小時的逐條討論,朝野黨團最後只對
            法案名稱、立法意旨及施行日期達成共識,其餘條文全數保留到今天院會中處理。 立法院會
            上午進行完報告事項後,約在10時30分開始進行討論事項,反滲透法草案列為討論事項第1案;
            在廣泛討論及逐條討論時,民進黨、國民黨各推派3人、親民黨、時代力量推派1人發言;
            各條文則依親民黨、時代力量、國民黨、民進黨的順序進行表決。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577721600
    assert parsed_news.reporter == '陳俊華台北'
    assert parsed_news.title == '反滲透法 立院上演表決大戰'
    assert parsed_news.url_pattern == '201912310042'
