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
    url = r'https://www.epochtimes.com/b5/13/12/7/n4028473.htm'
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
            美聯社根據南非總統朱瑪(Jacob Zuma)和新聞局今天發布的消息,整理出未來9天追悼與安
            葬前總統曼德拉(Nelson Mandela)的重要活動。 曼德拉因肺部感染住院近三個月後,9月出
            院返家,昨天在約翰尼斯堡的家中過世。 12月8日 全國祈禱與追思日 朱瑪說:「我們號召
            全民聚在廳堂、教會、清真寺、寺院、猶太教堂和家中祈禱與默想,追思馬迪巴(Madiba)一
            生及其對我國和世界的貢獻。」馬迪巴是曼德拉的族名。 12月10日 約翰尼斯堡足球城體
            育場官方追悼會 曼德拉生前最後一次公開活動,是2010年在約翰尼斯堡足球城體育場
            (FNB Stadium)的世界盃足球賽閉幕典禮。這座體育場因世界盃而稱為足球城
            體育場。 12月11日至13日 遺體暫厝普勒托利亞(Pretoria)政府大樓,供各界瞻仰。這段
            期間內,南非各省和地區也會舉行官方追悼會。 12月15日 南非國葬曼德拉於東開普省
            (Eastern Cape)庫努村(Qunu)。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1386345600
    assert parsed_news.reporter is None
    assert parsed_news.title == '南非15日國葬曼德拉'
    assert parsed_news.url_pattern == '13-12-7-4028473'
