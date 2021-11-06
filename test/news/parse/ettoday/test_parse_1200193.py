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
    url = r'https://star.ettoday.net/news/1200193'
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
            跟著捷運站買房,是許多人的購屋首選,尤其是出站就到家的捷運宅,不僅交通方便,保值性
            也高,其中又以捷運「聯開宅」最受歡迎。 敦南捷境建商代表高揚凱表示,「捷運聯開宅實
            際上是以既有地上性的站體,在它旁邊再建造一棟獨立的新建案,不同於共構宅是捷運行駛
            通過在建築物下方,因此它並沒有跟捷運連貫的問題,也不會有震動或是風水上的
            問題。」 位於台北市文山區辛亥站的《敦南捷境》建案,打出一站到大安,讓你快速置身於
            台北東區,無論是要前往台北101信義商圈,或是松山機場,都可以搭乘捷運很快的抵達。相較
            市區的高房價,文山區較親民的價格與優質地段環境,吸引許多置產客的青睞。 已購客戶
            高先生説,「平常上班或是休閒活動都是往台北市區跑,《敦南捷境》位於辛亥捷運站,大概
            2站到3站就可以到達台北市區。我們經由連結捷運的空橋進出家門口,就不用怕颳風下雨,
            而且小孩子外出跟回家也比較安全。」 除了通勤的安全,建案在建築結構上更加強了抗震,讓
            住戶住得安心。建商代表高揚凱指出,「我們SRC的建材能力,相比RC還能更有效的來抗震,
            我們的地基在打的時候,深入岩盤超過10米,這樣施工品質,在附近的建案或是在台北市裡,
            也都是非常難得的,尤其是像台北市這樣的地質,實際上並不是那麼穩的狀況下,我們的建築物
            擁有絕對的優勢。」 已購客戶陳太太表示,「因為我買房子會做蠻多功課的,建案施工的這家
            鋼構公司,它有承包過台積電的晶圓廠,如果有辦法接晶圓廠案子的廠商,我相信他在結構上或
            是施工細緻度的品質,一定不用擔心。加上他們使用的建材都很棒,像是氣密窗是使用LOW-E
            的節能複層玻璃,隔音跟隔熱的效果非常好。 敦南捷境主打2~3房格局,戶戶都有遼闊的綠
            意景觀,並享有萬芳生活圈機能,鄰近醫院和學區,更是近期難得擁有台北市門牌的捷運聯開
            宅,適合想要兼具交通與生活便捷,又喜歡遠離塵囂的置產客群。
            '''
        ),
    )
    assert parsed_news.category == '房產'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530254520
    assert parsed_news.reporter == '浦天慶'
    assert parsed_news.title == '台北市捷運聯開宅 《敦南捷境》一站到大安'
    assert parsed_news.url_pattern == '1200193'
