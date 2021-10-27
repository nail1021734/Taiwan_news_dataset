import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/04/15/a519169.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            悉尼一年一度的復活節農展會於4月14日正式開幕。和往年相比,今年新增了更多的展覽項目
            和遊樂設施,還有更多的農展會奇趣包。 據澳新社消息,本次農展會將展示13,000只動物、
            29,000項競技表演,預計會給紐省帶來5億澳元的收入。 在創記錄的331款農展會包中,有
            130種在 10元以下,以幫助家庭節省開銷。 主會場的夜間大彙演將呈現澳大利亞最精彩的
            國際牛仔競技比賽。 此次農展會還會有新的伐木表演、展示澳洲最高的牛、傳統的伐木
            競技、大遊行和寵物護理等。 預計會有100萬人前往悉尼奧林匹克公園參加農展會。 農展
            會將於4月27日結束,入場優惠、競技和美食的相關信息可以在網上查詢。
            '''
        ),
    )
    assert parsed_news.category == '海外華人'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1302796800
    assert parsed_news.reporter is None
    assert parsed_news.title == '澳洲悉尼農展會開幕'
    assert parsed_news.url_pattern == '2011-04-15-519169'
