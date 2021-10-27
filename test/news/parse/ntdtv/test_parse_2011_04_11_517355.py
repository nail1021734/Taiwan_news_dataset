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
    url = r'https://www.ntdtv.com/b5/2011/04/11/a517355.html'
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
            今天下午2時46分,日本舉國上下,從首相到百姓、各行各業所有人陷入一片沉寂,為1個月前、
            在3月11日爆發規模9.0強震海嘯時罹難的上萬人默哀。 在重災區氣仙沼市,仍在廢墟中
            挖掘尋找1萬5000名失蹤者下落的自衛隊隊員。 隨著警報聲響起,1名官員下令所有人員
            暫時停下手邊工作,放下工具、脫下頭盔和手套,悼念1個月前天災蹂躪日本的這一刻。這分鐘
            過去後,自衛隊員再度拾起工具,恢復搜尋屍體和清理廢墟作業。
            '''
        ),
    )
    assert parsed_news.category == '天災人禍,各國地震,日本地震'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1302451200
    assert parsed_news.reporter is None
    assert parsed_news.title == '震災滿月 日舉國默哀'
    assert parsed_news.url_pattern == '2011-04-11-517355'
