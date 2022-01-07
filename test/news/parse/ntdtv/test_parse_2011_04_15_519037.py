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
    url = r'https://www.ntdtv.com/b5/2011/04/15/a519037.html'
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
            星期四(4月14号),利比亚多地炮火不断。独裁统治者卡扎菲,先动用部队摧毁重镇米苏塔拉
            的食品仓库,又切断了水电供应,试图用这种方式逼迫民众就范。当天,他还在的黎波里制作了
            一段所谓的为民所拥护的录像。 卡扎菲军周四,用大炮攻击已经被围困数个星期的米苏塔拉,
            并试图控制该镇的港口,这个港口原计划将停靠一艘医疗救护船。另外,卡扎菲军摧毁了当地
            的食品供应仓库,切断了水电,打算用断水断粮,逼迫民众投降。 当天,正值北约在柏林开会,
            商讨利比亚问题。卡扎菲借此时机,利用国家电视台,播放了一小段自己被民众支持的录像,
            招来国际社会的谴责。 美国白宫发言人卡尼:“一个镇压民众的领导人宣传自己,并不罕见,
            这种情况时有发生。我要简单的告诉你们,我们和国际伙伴一起正在逐日拉紧套在卡扎菲身上
            的套索。” 据米苏塔拉的医生透露,卡扎菲军在周四凌晨的袭击,造成至少20名平民死亡,
            更多人受伤。他说,因为卡扎菲的封锁,当地的物资已经非常匮乏。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1302796800
    assert parsed_news.reporter == '任浩'
    assert parsed_news.title == '卡扎菲断粮断水逼民众就范'
    assert parsed_news.url_pattern == '2011-04-15-519037'
