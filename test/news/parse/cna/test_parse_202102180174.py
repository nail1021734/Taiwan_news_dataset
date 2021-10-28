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
    url = r'https://www.cna.com.tw/news/aipl/202102180174.aspx'
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
            美國國防部官員今天表示,儘管軍隊的2019冠狀病毒疾病(COVID-19)感染率居高不下,仍有
            約1/3的美軍官兵拒絕接種疫苗。 法新社報導,由於美國食品暨藥物管理局(FDA)尚未全面
            核准COVID-19疫苗,國防部持續將它們歸類為選擇性疫苗。 空軍少將塔利亞費羅
            (Jeff Taliaferro)在國會聽證會表示,美軍「疫苗接種率約在2/3」,並強調這個數據
            是基於「非常早期的資料」。 美國國防部發言人柯比(John Kirby)表示,目前沒有美軍
            接種的詳細數據,但目前施打人數已超過91萬6500人,這個週末施打人數應會破百萬。 柯比
            表示,軍隊拒絕接種的比例與一般大眾相同,他告訴記者:「軍隊基本反映美國社會
            (對疫苗)的接受度。」 柯比表示,由於COVID-19疫苗僅獲批准供緊急使用,國防部不能
            強迫人員注射,「在強制要求軍人和軍眷接種上,我們的法律有很實際的限制」。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1613577600
    assert parsed_news.reporter == '華盛頓'
    assert parsed_news.title == '五角大廈:1/3美軍拒打COVID疫苗'
    assert parsed_news.url_pattern == '202102180174'
