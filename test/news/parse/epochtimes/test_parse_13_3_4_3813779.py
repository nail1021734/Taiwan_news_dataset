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
    url = r'https://www.epochtimes.com/b5/13/3/4/n3813779.htm'
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
            美國國務卿克里已經離開埃及,抵達沙特阿拉伯。在埃及期間,克里承諾,美方將再次給予
            埃及經濟援助。 在和埃及總統穆爾西於星期天舉行會談期間,克里表示,美方將立即為埃及
            提供價值一億九千萬美元的援助。這筆援助資金是美方準備向埃及提供的價值四億五千萬
            美元援助的一部份。這些援助是為了幫助埃及開始國內亟需進行的經濟改革。克里還表示,
            美方同時還將拿出六千萬美元來,資助企業家和年青人。 而埃及總統穆爾西擔保,埃及政府
            將會實行政治和經濟領域的改革,以幫助穩定埃及國內的局勢。 穆爾西同時還承諾要和國
            際貨幣基金組織之間,就埃及要向這一組織借貸的價值48億美元的款項,達成協議。這一項
            目過去幾個月來,一直處於被擱置狀態。埃及財政部長表示,在四月份埃及議會選舉開始之
            前,將和國際貨幣基金組織達成這項協議。 當地時間星期天晚間,埃及的解放廣場再度出現
            爭執。要求改革的抗議人士和安全人員發生了衝突,至少兩輛汽車被點燃。抗議人士同時還
            在塞得港和警方發生衝突。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1362326400
    assert parsed_news.reporter is None
    assert parsed_news.title == '克里承諾援助埃及後抵達沙特'
    assert parsed_news.url_pattern == '13-3-4-3813779'
