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
    url = r'https://star.ettoday.net/news/7427'
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
            新北市福隆帆船協會負責人詹志鴻16日晚間上吊自殺,員工發現時他已無氣息。據悉,詹男
            的帆船界同好聞訊後很訝異,表示雖然他這1、2年來財務狀況不佳,也和幾個好友借過錢,但
            數目都不大,應該不會因此尋短,懷疑可能是有其他更嚴重的困擾。 現年44歲的詹志鴻是
            前帆船國手,體格壯碩,現任台北市帆船委員會總幹事。未料,瑞芳分局福隆派出所16日晚間
            近9時接獲報案,員工表示發現老闆在俱樂部上吊自殺;警方到場後封鎖現場,現場沒有發現
            遺書,詹志鴻的家屬也趕往警局協助製作筆錄。 據悉,帆船俱樂部已是第2代經營,雖然每年
            靠會員新台幣8000到1萬元的會費苦撐,但詹的帆船同好表示,「大家都是為了共同的興趣
            才做」,應該不至於為財務自殺。只是,他的好友也坦承,詹志鴻這1、2年來曾經跟他們借錢
            ,但因為金額不多,所以他們沒有過問。
            '''
        ),
    )
    assert parsed_news.category == '社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1321496520
    assert parsed_news.reporter is None
    assert parsed_news.title == '為錢所困? 帆船俱樂部負責人上吊自殺'
    assert parsed_news.url_pattern == '7427'
