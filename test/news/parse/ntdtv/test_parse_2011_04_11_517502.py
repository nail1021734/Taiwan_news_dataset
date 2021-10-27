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
    url = r'https://www.ntdtv.com/b5/2011/04/11/a517502.html'
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
            法國駐科特迪瓦(Ivory Coast)大使館星期一(4月11日)表示,該國強人巴博
            (Laurent Gbagbo)已遭民選總統瓦塔拉(Alassane Ouattara)的「共和軍」逮捕。在
            此逮捕行動之前,法國部隊曾進行攻擊。 科特迪瓦去年11月28日舉行總統大選,瓦塔拉勝出,
            並獲得聯合國承認為合法總統,但前任總統巴博拒絕交出政權,導致全國陷入動盪戰亂,死傷
            無數。 稍早,法國軍方一名發言人說,這次軍事行動的目的是為了避免一場血戰。據報法軍
            動用了裝甲車和武裝直升機。 人權觀察組織(HumanRights Watch)9日表示,巴博軍隊在
            3月底殺害或性侵數百名平民,並焚燒村莊。這個人權組織公布新證據,詳列巴博部隊在
            北方小鎮殺害 100名男、女及小孩,並在附近村鎮發動致命攻擊等暴行。 聯合國和法國部隊
            上週展開聯合行動,開火攻擊巴博位於阿比讓(Abidjan)的總統府、總統官邸和兩座兵營,
            使其陣營無法使用重型武器對付平民。 聯合國於3月30日通過決議案,要求巴博立即下台,
            並對巴博夫婦及親信高官實施制裁與旅游禁令。 2011年4月11日在道路上的居民慶祝在
            阿比讓逮捕巴博
            '''
        ),
    )
    assert parsed_news.category == '國際專題,敘利亞局勢'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1302451200
    assert parsed_news.reporter is None
    assert parsed_news.title == '科特迪瓦前總統巴博被捕'
    assert parsed_news.url_pattern == '2011-04-11-517502'
