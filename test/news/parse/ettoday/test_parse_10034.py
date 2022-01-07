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
    url = r'https://star.ettoday.net/news/10034'
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
            NBA即將開季,對於不少球隊將目光鎖定在「魔獸」霍華德(Dwight Howard)
            、「CP3」保羅(Chris Paul)等人時,芝加哥公牛決定先「安內」,完成與
            最年輕MVP羅斯( Derrick Rose)的延長合約。 羅斯上季率領公牛隊拿下例行賽62勝
            的好成績,並以22歲的年紀,成為NBA史上最年輕的MVP,甚至讓聯盟特別訂定了「羅斯條款」
            希望給剛走完新秀合約的超級新人們合理待遇。 即將返回公牛訓練球場備戰新賽季的羅斯
            ,似乎也希望球團能夠開出最有「誠意」的合約與他完成延長合約的動作。而公牛球團也打算
            在9日自由市場開放後,正式與羅斯討論延長合約的相關事宜。 而據新版的薪資規定,羅斯
            在「羅斯條款」的幫助下,有望可以簽下5年、總價1億美元以上的大約。對於知道有新的
            條款以自己的名字命名,羅斯表示,「這真是不可思議,但這個條款將讓更多的年輕球員,努力
            追求像我一樣的成就。」 如果能夠順利與羅斯達成新約,公牛也打算為羅斯尋找一位新的
            得分後衛副手,而不打算行使柏格(Keith Bogans)的選擇權。柏格上季出賽82場,只能
            貢獻4.4分、1.8籃板和1.2助攻的成績。
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1322709900
    assert parsed_news.reporter == "劉肇育"
    assert parsed_news.title == '迎戰新賽季 公牛要先搞定羅斯新合約'
    assert parsed_news.url_pattern == '10034'
