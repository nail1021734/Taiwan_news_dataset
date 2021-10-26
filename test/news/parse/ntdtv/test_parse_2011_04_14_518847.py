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
    url = r'https://www.ntdtv.com/b5/2011/04/14/a518847.html'
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
            巴黎舊公寓大火-5人死亡 巴黎第20區一幢6層住宅樓14日淩晨發生火灾,目前已造成5人
            死亡,57人受傷,其中6人傷勢嚴重。這是2005年以來巴黎最嚴重的一次火灾。 據法國媒體
            報道,當天淩晨3時這幢住宅樓的樓梯間發生大火,由于樓梯是老式的木質結構,火勢迅速
            蔓延。三名女子和一名男子不堪大火和濃烟,跳樓身亡,另有一名男子燒傷身亡。一名消防員
            因觸電傷勢嚴重,6名兒童受輕傷。 接到火警後,約300名消防員8分鐘後趕到現場。這幢
            住宅樓位于一個樓房較密集的小區內,這給滅火工作造成不少困擾。約5時30分,火勢得到
            控制。受火灾影響的居民已被安置在附近一個體育館內。目前火灾原因不明。 2005年巴黎
            曾發生一場大火,造成25人死亡,其中有10名兒童。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1302710400
    assert parsed_news.reporter is None
    assert parsed_news.title == '巴黎發生自05年來最嚴重火灾 5死57傷'
    assert parsed_news.url_pattern == '2011-04-14-518847'
