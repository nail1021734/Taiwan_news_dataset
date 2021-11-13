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
    url = r'https://star.ettoday.net/news/2104659'
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
            天降奇蹟是指有天大的好運,但是花園裡天降活雞可就不太妙了,一名女網友在
            「我是東湖人」社團張貼影片表示,有2個女人把2隻白色活雞往她家花園裡丟,
            現在雞滿園子跑,讓她很傻眼,不知該怎麼處理,對此則有網友提醒「這是詛咒」,讓她要小心
            。 貼出影片的網友表示,家裡監視器拍到兩個戴口罩的女人偷偷摸摸地把白色活雞往
            花園裡丟,中間還不小心把袋子弄掉了,用雨傘勾半天,撿回袋子後就轉身走人,留下2隻雞逛
            花園,讓她超傻眼,只好把影片發上網問問「有人認識這兩個丟雞的女人嗎?」 原PO表示,
            住家附近常有野狗出沒,因此不敢把雞直接放生,可是花園也曾發生野狗咬死下山覓食山羌
            事件,這2隻雞放在這裡也不安全,希望大家幫忙找到原主把雞帶走。網友開玩笑回復
            「是美食外送啦,只是要自己煮」「沒有附蔥薑太過分了」「冬天進補囉」;不過也有網友
            指出這「可能是一種詛咒」。 民間傳統習俗有一種說法,若一年內家中不幸有2人相繼過世,
            喪禮就要做「祭三喪」儀式,也有稱作「祭草人」或「祭空棺」,祈求家族內不要再發生
            不幸之事,其中可能使用活雞進行草人開光,白鴨則用於壓制煞氣,習俗中,這些用作祭祀的
            活雞或鴨可能帶有煞氣,老一輩的人都會告誡不要隨意觸碰或是捕抓甚至是食用,可能會
            招來霉運。 原PO看完網友提醒更傻眼,直呼嚇出一身冷汗,因為溪裡真的是出現白鴨和白雞,
            隔天雞就被丟在她家花園,幸好她隨後想起可以打給動保處尋求幫助,目前2隻雞已經被帶走。
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634622300
    assert parsed_news.reporter == '鏡週刊'
    assert parsed_news.title == '花園被丟入「2隻白色活雞」 內行人狂喊:小心!這是詛咒'
    assert parsed_news.url_pattern == '2104659'
