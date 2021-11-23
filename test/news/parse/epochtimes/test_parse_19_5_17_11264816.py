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
    url = r'https://www.epochtimes.com/b5/19/5/17/n11264816.htm'
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
           美國商務部週四(5月16日)公佈對從中國進口的石英檯面產品進行反傾銷稅和反補貼稅調查
           的最終裁定。商務部調查發現中國出口商以低於公允價值265.84%到336.69%不等的價格在
           美國銷售石英檯面產品。商務部還認定,中國出口商獲得了45.32%至190.99%不等的補貼
           。 在肯定的反傾銷最終裁決公佈後,商務部將指示美國海關和邊境保護局收取與適用的最終
           加權平均傾銷幅度相等的反傾銷保證金。 此外,鑑於商務部做出了肯定的反補貼稅最終裁決,
           如果美國國際貿易委員會隨後做出肯定的損害裁決,即認定中國(中共)的補貼行為給美國企業
           帶來傷害,商務部將指示海關和邊境保護局恢復徵收與補貼率相等的反補貼稅保證金。如美國
           國際貿易委員會做出否定的最終損害裁定,有關調查將會終止,也不會發布稅令。國際貿易
           委員會目前計劃在2019年6月24日或前後做出最終的損害裁決。 2017年,美國從中國進口的
           某些石英檯面產品價值約4.6億美元。 美國商務部目前維持著481項反傾銷和反補貼關稅令。
           自川普(特朗普)總統上任以來,商務部共開展了162項新的反傾銷和反補貼調查,比上屆政府
           同期增長224%。
            '''
        ),
    )
    assert parsed_news.category == '北美新聞,美國經濟'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1558022400
    assert parsed_news.reporter is None
    assert parsed_news.title == '美商務部:從中國進口石英檯面傾銷有補貼'
    assert parsed_news.url_pattern == '19-5-17-11264816'
