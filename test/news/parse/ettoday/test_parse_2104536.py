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
    url = r'https://star.ettoday.net/news/2104536'
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
            蘋果原本一直使用英特爾晶片,直到近年,蘋果開始自行研發晶片,逐漸降低對英特爾的依賴,
            這也讓英特爾的生意受到影響,因此一直希望能贏回蘋果的心。日前,英特爾執行長
            Pat Gelsinger再次向蘋果呼喊,希望能讓蘋果回頭,根據外媒Appleinsider報導,
            他在接受採訪時表示,英特爾希望能贏回蘋果的業務,但首先英特爾需要創造比蘋果更好的
            晶片來達到這點。 隨著蘋果宣布從Intel晶片向 Apple Silicon 過渡到下一代設備,
            英特爾執行長Pat Gelsinger表示,他永遠不會放棄Mac重新使用英特爾處理器的希望
            。 Pat Gelsinger在接受Axios on HBO採訪時表示,他並不怪蘋果放棄英特爾,因為
            蘋果一定是認為,他們能生產出比我們更好的晶片,所以要贏回蘋果,英特爾首先要做的就是
            做出比蘋果更好的晶片。 Pat Gelsinger也說,與此同時,英特爾必須確保我們的產品比
            他們的更好,我們的生態系統比他們的更加開放和充滿活力,我們為開發人員和用戶使用基於
            英特爾的產品創造了更有說服力的理由。 Pat Gelsinger最後也強調,英特爾會
            很努力來贏回庫克(蘋果執行長)的生意。
            '''
        ),
    )
    assert parsed_news.category == '財經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634614020
    assert parsed_news.reporter == '高兆麟'
    assert parsed_news.title == '英特爾呼喚蘋果回歸 執行長:會打造比蘋果更優晶片贏回生意!'
    assert parsed_news.url_pattern == '2104536'
