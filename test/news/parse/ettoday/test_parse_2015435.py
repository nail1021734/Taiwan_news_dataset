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
    url = r'https://star.ettoday.net/news/2015435'
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
            最近宜蘭常零確診,頭城地區出現外地遊客潮,讓當地人好緊張,臉書《頭城二三事》
            發起募資4000元,做「防疫期間,宜蘭人都在家,你來幹嘛?好意思嗎?」看板,獲得
            熱烈回應後,預計在29日在頭城市區掛上第一面看板,而第二面看板也在尋找募資中
            。 臉書《頭城二三事》版主看到上周末頭城湧現外地遊客潮,令居民們相當緊張是否會出現
            防疫破口,再看到日前有墾丁民眾自立看板要遊客不要來,為此在22日發起集資活動,
            預計29日起在市區掛上「防疫期間,宜蘭人都在家,你來幹嘛?好意思嗎?」帆布,
            勸遊客疫情期間不要來頭城。 《頭城二三事》說,印布條需要4000元,拆成40股,1股100元
            ,每位鎮民最多「認領」2股,這項嘜擱來頭城看板集資活動一出,獲得網熱烈回應,不到
            15分鐘就額滿,不少人來不及跟到,要求要參加第二面募資活動。 而經頭城城南里長林春
            三奔波看板將掛在青雲路二段、頭濱路三段街口,遊客從頭城大橋進市區或前往外澳都能清
            楚看到,預計從29日掛到三級警戒解除。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1624591440
    assert parsed_news.reporter == '游芳男'
    assert parsed_news.title == '嘜擱來啊!宜蘭頭城人募資掛看板:你來幹嘛?好意思嗎?'
    assert parsed_news.url_pattern == '2015435'
