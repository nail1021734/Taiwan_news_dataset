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
    url = r'https://www.epochtimes.com/b5/13/3/3/n3813542.htm'
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
            「瀕臨絕種野生動植物國際貿易公約(CITES)」第16屆締約國大會今天在曼谷開幕,泰國總
            理盈拉致詞時透露,泰國將提案修改國家立法,以終結象牙交易。 盈拉
            (Yingluck Shinawatra)表示,修法將符合國際規範,有助保護各種類的大象,包括泰國
            野生象、馴養象以及非洲的大象。 泰國雖禁止野生象象牙交易,卻允許馴養象象牙交易,不肖
            商人利用法律漏洞非法走私非洲象牙,因為需求導致許多非洲象遭盜獵。 世界自然基金會
            (WWF)指出,泰國是世界上不受管制象牙交易的最大市場,並呼籲泰國修改法律,完全禁止象牙
            交易,才能真正遏止大象遭濫殺。 世界自然基金會代表團團長德魯斯(Carlos Drews)透過
            新聞稿表示,盈拉誓言終止泰國象牙交易讓他們感到振奮,但她必須提出禁止象牙交易的
            時間表,因為大象遭濫殺的問題,已事態急迫。 英國威廉王子也以影音致詞方式參予開幕
            典禮,呼籲打擊非法野生動植物盜獵、交易等。 簡稱為「華盛頓公約」的「瀕臨絕種野生
            動植物國際貿易公約」(Convention on the International Trade in En
            dangered Species of Fauna and Flora),簡稱為CITES)1973年簽署,被列在附錄一
            的物種禁止商業性國際貿易,列在附錄二的物種,目前雖未瀕臨滅絕,但如對貿易不嚴加管理,
            有可能變成滅絕危險的物種。 這次大會共有177個締約國、大約2000個代表出席,會議將
            進行到14日,會中共有70個提案討論,包括鯊魚、魟魚、龜類、犀牛、大象以及其他多種
            動植物。 締約國將在會中討論是否同意提案物種列入附錄一或附錄二,或改變原列附錄,也
            將討論如何整合策略,以終止盜獵、走私瀕絕動植物。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1362240000
    assert parsed_news.reporter == '林憬屏曼谷3日專電'
    assert parsed_news.title == '泰總理允諾修法終結象牙交易'
    assert parsed_news.url_pattern == '13-3-3-3813542'
