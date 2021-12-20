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
    url = r'https://www.epochtimes.com/b5/13/2/27/n3810172.htm'
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
            週二(2月26日),世界貿易組織裁定歐盟起訴中國向進口的X射線安檢設備徵收反傾銷稅案中
            勝訴。對歐盟來說,世貿組織的這個結論可以說是一個勝利,如果在60天之內沒有上訴,中國
            就必須取消對進口的X射線產品徵收反傾銷稅。 據法新社報導,歐盟於2011年7月將與中國
            之間有關X射線安檢設備反傾銷稅的爭端,提交世貿組織解決。 世界貿易專家小組在對
            歐盟的起訴,以及中國和歐盟的各自的觀點進行評審後,週二得出結
            論,認為中國的做法與關貿總協定和世界貿易中的反傾銷合約的規定不符。得出結論認為歐
            盟在合約中應該享有的優勢被取消或者被擱置。 因此,世界貿易組織要求中國採取相應的
            措施以便與世界關貿組織和反傾銷合約的規定達成一致。 中國自2011年1月23日開始對原
            產於歐盟的進口X射線安檢設備徵收33.5%至71.8%不等的反傾銷稅,實施期限為5年。中國商
            務部當時表示,原產於歐盟的進口X射線安檢設備存在傾銷,導致中國國內X射線安檢設備產
            業遭受實質損害。 法新社認為,這樣做的結果是歐洲的同類產品將被排斥在中國市場之外
            。 2009年10月23日,中國商務部應國內產業申請,根據《反傾銷條例》規定,發佈了對原產
            於歐盟的進口X射線安全檢查設備進行反傾銷調查的立案公告。2010年6月9日,商務部發佈
            了本案初裁決定。 歐盟認為中國採取的措施沒有任何根據,實際上是北京的一種報復措施。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1361894400
    assert parsed_news.reporter == '徐亦揚'
    assert parsed_news.title == '中國對X射線安檢設備徵收反傾銷稅案 歐盟勝訴'
    assert parsed_news.url_pattern == '13-2-27-3810172'
