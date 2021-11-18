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
    url = r'https://star.ettoday.net/news/8470'
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
            隨著蘋果教主賈伯斯的逝世,大批蘋果迷將iPhone4S當成他的紀念機款爭相搶購,也創下
            上市3天就賣破400萬支的驚人數次,不過,當一窩蜂的熱潮過了,許多購買iPhone 4S的人
            ,開始抱怨手機不如預期,甚至還有5分之1的人表示「很後悔」
            。 英國網站《GoodMobilePhones》進行一項iPhone用戶的問卷調查,共收回了1694位
            民眾的意見,結果顯示有5分之1的人後悔買了iPhone4S,當中有43%的受訪者是因為
            忌妒市場上不斷推陳出新的智慧手機,不僅螢幕更大且上網速度也快,相比之下
            ,iPhone 4S無法滿足使用需求。 5%受訪者表示,對於電池壽命太短很失望;8%受訪者則是
            不滿電子郵件系統,調中還顯示,不滿iPhone 4S的的使用者裡,科技達人就高達73%。而
            台灣預估最快12月中旬就能買到iPhone 4S。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1322005800
    assert parsed_news.reporter is None
    assert parsed_news.title == '想要iPhone 4S? 調查:1/5人後悔買'
    assert parsed_news.url_pattern == '8470'
