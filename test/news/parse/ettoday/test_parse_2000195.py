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
    url = r'https://star.ettoday.net/news/2000195'
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
            前兩日雨彈狂炸雙北,各地傳出淹水災情,還有房屋漏水、地下室淹沒慘況。就有網友在PTT
            的home-sale板上發文,「了台北時雨量200MM,真是令人震撼,這種時雨量應該沒有一個
            地方的排水系統負荷得了......」就算有裝抽水系統,一時可能也無法負荷,就好奇請益
            「請問大家大樓有做防水閘門嗎?」 這位網友文中表示,他看到台北時雨量200mm,覺得
            很震撼,「這種時雨量應該沒有一個地方的排水系統負荷得了,若淹進地下停車場,大概裡面有
            很多車子就GG了......」他就說,即使很多大樓有裝抽水系統,但一時雨量這麼大,抽水系統
            大概也無法馬上負荷過來,「想請問各位住大樓的,有大樓在停車場地下道入口裝擋水閘門
            的嗎?」 貼文一出,其他人紛紛留言討論,「有呀,從來沒用過做心安的」、「沒有,反正
            沒淹過水」、「沒有,反正B2、B3會先淹」、「有啊,不過我的社區地勢較高,灌進去可能
            台北都沒了」、「有,每年都測試2次,透過APP公告」、「看你地勢多高吧?低窪地區都
            建議裝。」 還有苦主現身,「有,舊大樓受災過」、「30年大樓都有了,這很便宜好用的
            東西,推銷員賀伯納莉。」另外,也有網友指出,「現在法規規定要裝吧」、「建築技術規則
            建築設計施工編(100年6月21日起)第 4-1條:建築物除位於山坡地基地外,應依下列規定
            設置防水閘門(板)......汽車坡道出入口,應設置高度自基地地面起算九十公分 以上之防
            水閘門(板)。」
            '''
        ),
    )
    assert parsed_news.category == '房產'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1622962140
    assert parsed_news.reporter is None
    assert parsed_news.title == '「大樓有做防水閘門?」苦主現身 曝最強推銷員:來過就裝了'
    assert parsed_news.url_pattern == '2000195'
