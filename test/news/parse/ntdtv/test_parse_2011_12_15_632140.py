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
    url = r'https://www.ntdtv.com/b5/2011/12/15/a632140.html'
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
            選前30天,民進黨今天(14日)啟動全臺市場掃街拜票行程。總統參選人蔡英文,也親自到
            板橋埔墘市場拜票。民進黨這一波市場總動員,由各地立委候選人,到當地的菜市場向婆婆
            媽媽們拜票,預計要掃完全台灣一千個市場。 來到人擠人的傳統市場,蔡英文在板橋立委
            參選人陪同下,逐一與攤商握手拜票,雖然天空下著雨,不過有些民眾看到蔡英文,還是很熱情
            的搶著要和蔡英文握手。 攤商:「她看起來人很好,氣色也很好」 攤商:「她隨扈旁邊太多
            人了啦,連看都不好看到,我們那麼矮,(很想跟她握手嗎),很想,還要給她簽名又
            簽不到啊」 攤商:「感動啊,就覺得台灣有希望,我是欣賞她不是選黨籍的關係」 選前一個
            月,民進黨發起全臺一千個市場總動員,由輔選幹部和立委候選人,全力掃街拜票,進行選前
            倒數衝刺。 民進黨總統參選人蔡英文:「我們希望透過這一千個菜市場掃街,在最後的選舉
            30天,我們可以對台灣的人民傳達,我們民進黨這次,對於這個選舉的熱切的一種期待,跟
            我們選民在最後階段的相互的互動。」 選舉拼場,民進黨將焦點選在市場,和基層互動,也要
            爭取更多的婦女票源。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1323878400
    assert parsed_news.reporter == '阜東,劉姿吟台灣臺北'
    assert parsed_news.title == '選前30天 蔡英文上市場拜票'
    assert parsed_news.url_pattern == '2011-12-15-632140'
