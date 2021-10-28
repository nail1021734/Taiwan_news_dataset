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
    url = r'https://www.cna.com.tw/news/aipl/202109060288.aspx'
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
            英國國防部高級官員今天表示,一些曾參與阿富汗戰爭的退伍軍人,對於美國撤軍與塔利班
            勝利感到痛心而結束生命,但他隨即聲稱是口誤,並說政府已就是否真有此事展開
            調查。 路透社報導,這場戰爭長達20年、耗資1兆美元與奪走數十萬人命,下場是塔利班
            閃電接掌阿富汗,許多退伍軍人嚥不下如此「恥辱」。 英國在阿富汗折損457名官兵,占
            國際聯軍自2001年以來陣亡3500人當中的13%。 英國國防部主管武裝部隊次長
            哈佩(James Heappey)一開始告訴天空新聞網(Sky News):「據我所知,不幸的是,有些
            曾在阿富汗服役的軍人,確實還有一位是我上次派駐阿富汗時在那裡服役的軍人,為了阿富汗
            發生的事情感傷而在上週結束了他們的生命。」 曾在阿富汗、北愛爾蘭與伊拉克服役的哈佩
            又說:「這令人非常擔憂和不安。」「這讓我打從心底非常難過。」 但是哈佩後來改口,他
            告訴英國廣播公司(BBC):「事實上我說的事情不大正確。」「我們正非常非常謹慎地
            調查,過去幾天是否真有人結束自己生命。」 英國國防部表示是哈佩口誤,否認有任何
            退伍軍人因為撤軍而自殺。 從政前官拜少校的哈佩說,他聽說塔利班已控制整個
            阿富汗,但龐吉夏(Panjshir)淪陷的情勢並未改變大局。 距2001年911攻擊事件不過
            20年,英國擔心塔利班回鍋與西方混亂撤退所導致的權力真空,將使蓋達組織(al Qaeda)
            激進分子在阿富汗坐大。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1630857600
    assert parsed_news.reporter == '倫敦'
    assert parsed_news.title == '英官員稱老兵痛心阿富汗撤軍自殺 隨即改口待查證'
    assert parsed_news.url_pattern == '202109060288'
