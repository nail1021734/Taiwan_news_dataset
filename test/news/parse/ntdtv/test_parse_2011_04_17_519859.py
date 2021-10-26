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
    url = r'https://www.ntdtv.com/b5/2011/04/17/a519859.html'
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
            英國王室官員今天宣布,哈利王子已完成阿帕契(Apache)攻擊直升機第1階段飛行訓練,並
            已晉升為上尉。 哈利已有資格在無指導員情況下駕駛阿帕契直升機,現在將學習操作武器
            系統。 2007和2008年的10周期間,哈利曾在阿富汗引導戰機空襲海曼德省(Helmand)
            塔利班陣地,如今完成這項飛行課程,將使26歲的哈利更近一步重返前線。 哈利本月稍早
            表示,如果英軍不打算調派他,那麼他的飛行訓練將變得毫無意義。 哈利表示:「你成為1項
            昂貴資產,訓練所費不貲,如果他們不派我出去做這份工作,他們不會讓我接受訓練,否則我
            只是佔用別人受訓的名額罷了。」 哈利於2006年4月任命為軍官,並於去年7月展開阿帕契
            直升機飛行訓練。訓練過程包含大量學習,以及數小時的日夜模擬機飛行。 哈利王子從軍
            5年後,獲得上尉頭銜。 哈利胞兄威廉王子本月稍晚將與凱特.密道頓(Kate Middleton)
            完婚,哈利將擔任伴郎。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1302969600
    assert parsed_news.reporter is None
    assert parsed_news.title == '哈利王子晉升上尉 盼重返火線'
    assert parsed_news.url_pattern == '2011-04-17-519859'
