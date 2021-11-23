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
    url = r'https://www.epochtimes.com/b5/12/7/30/n3646941.htm'
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
            早在Google推出線上定位服務、從非公開的無線熱點擷取資料之前,就有所謂的「綿
            羊牆」(Wall of Sheep)存在。 「綿羊牆」是由艾利斯資安公司(Aires Security
            )研發,一直是聲名狼藉的「駭客大會」(Def Con)聚會時的要角。年度「駭客大會」
            今天在拉斯維加斯(Las Vegas)閉幕。 以「安全警覺工具」為設計宗旨、多年來不斷
            精進的「綿羊牆」,擷取智慧型手機、筆記型電腦等裝置無線傳輸的資料,從中找出未
            經加密或沒有嚴密密碼保護的資訊。 「綿羊牆」研發者將輕忽無線傳輸資料的使用者
            ,稱為易受狼群攻擊的「羊人」,狼群擷取傳輸,就像在咖啡廳偷聽別人閒聊那樣容易
            。 「綿羊牆」研發者認為,Google以街景車擷取未經保護的無線資料,或許不道德、
            但是完全合法。 艾利斯資安公司總裁馬庫斯(Brian Markus)在會中發言時,身後的
            「綿羊牆」同時投影「羊人」的私人資料,他說:「如果你在公共場合、比如說星巴克
            (Starbucks)偷聽對話,你不是在犯法。」 「從無線的角度來說,如果被動監控,你不
            必違法侵入任何東西。」 「綿羊牆」團隊的T恤印著「加密,不然你總有一天會後悔」
            字樣。 「綿羊牆」的主題有沒有犯法、延伸Google街景車的作法是不是犯罪,都是這
            場「駭客大會」焦點。 賓州大學分散式系統實驗室主任布列茲(Matt Blaze)在會中
            提及擷取無線資料:「科技人覺得嗅聞沒問題,懂隱私的人覺得很可怕。」 「如果兩者
            都懂,你的頭會爆炸。」
            '''
        ),
    )
    assert parsed_news.category == '科技新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1343577600
    assert parsed_news.reporter is None
    assert parsed_news.title == '駭客英雄會 惱街景服務搶羊人'
    assert parsed_news.url_pattern == '12-7-30-3646941'
