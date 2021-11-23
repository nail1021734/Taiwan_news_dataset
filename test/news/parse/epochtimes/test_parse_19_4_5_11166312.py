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
    url = r'https://www.epochtimes.com/b5/19/4/5/n11166312.htm'
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
            新唐人電視台應觀眾要求,從4月1日起開始在美東、美西、大陸和歐洲頻道再播一輪《蠶食
            美國》紀錄片,分四週播完。 《蠶食美國:碾碎美國的圖謀》(Agenda:Grinding Ame
            rica Down)及續集《蠶食美國2:欺詐大師》(Agenda 2:Masters of Deceit)由美國
            愛達荷州前眾議員柯蒂斯‧鮑爾斯(Curtis Bowers) 製作,先後於2010、2015年推出。
            上映後引起轟動,並獲得了2010年聖安東尼奧獨立製作基督教電影節(SAICFF)最佳影片
            大獎。 該紀錄片深刻揭露了共產主義對美國及全世界近百年來進行的精心部署,並結合美國
            的現實使人清楚地意識到共產滲透的破壞力之大、毒害之廣。該片被稱為「迄今揭露共產主義
            者、社會主義者及進步主義者企圖奪取美國的最有力的作品」。 《蠶食美國》分為兩集:
            (一):碾碎美國的圖謀 (上,下);(二): 欺詐大師 (上,下)。
            '''
        ),
    )
    assert parsed_news.category == '北美新聞,美國政治'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1554393600
    assert parsed_news.reporter is None
    assert parsed_news.title == '新唐人電視台再播出《蠶食美國》紀錄片'
    assert parsed_news.url_pattern == '19-4-5-11166312'
