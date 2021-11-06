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
    url = r'https://star.ettoday.net/news/1200413'
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
            金管會開放2張純網銀執照,在立法之前將召開公聽會聽取外界意見,公聽會預計本週五(29
            日)登場,由金管會主委顧立雄親自主持,據金管會公布的資料,LINE、中華電信、遠傳、日
            本樂天等有意做純網銀的業者都將出席。 金管會在4月26日正式公布開放2張純網銀執照,
            開放家數以2家為限、業者設立需至少100億元、發起人中至少有1家銀行或金控且持股達50%
            以上、且須設立實體總行與客服中心,但不得設立實體銀行。 目前先傳出LINE有向金管會
            表達過意願,國票金隨後也宣布日本樂天合作,中華電信也攜手兆豐銀、一銀合組「國家隊
            」,正式形成「三搶二」的局面。也有金控高層建議金管會應該保障國家隊的名額,但中華
            電日前引發「499之亂」也引起金管會關注是否有公司治理的疑慮。 金管會表示,純網銀公
            聽會本週五(29日)上午召開,包括央行、中央存保、銀行公會都派人參與,外界關注哪些業
            者會出席,據金管會公布的出席名單,包括台灣區LINE負責金融科技的劉奕成、中華電信董
            事長鄭優、遠傳電信董事長徐旭東、PChome網路家庭董事長詹宏志與日本樂天銀行等,銀行
            公會也會邀請有意加入的銀行業者參加。
            '''
        ),
    )
    assert parsed_news.category == '財經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530081240
    assert parsed_news.reporter == '戴瑞瑤'
    assert parsed_news.title == '公聽會29日登場 LINE、中華電都將出席'
    assert parsed_news.url_pattern == '1200413'
