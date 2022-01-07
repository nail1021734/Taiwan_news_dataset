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
    url = r'https://star.ettoday.net/news/2031852'
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
            《三國殺名將傳-威力加強版》盛情邀約全能天后「楊丞琳」為遊戲代言!事前預約活動
            熱烈進行中,還有機會獲得現金10萬元等超值好禮! 天后級代言人,楊丞琳驚艷現身
            ! 作為《三國殺名將傳》的續作《三國殺名將傳-威力加強版》,積極地提升遊戲美術與
            特效,以最美三國卡牌遊戲的姿態展現於大家的面前,就如同受到萬人關注的楊丞琳,
            歷經多年的磨練與成長後,蛻變為今日立於眾人眼前的全能天后。 本次代言合作中,楊丞琳
            以古裝扮相驚艷亮相,同時扮演了忠肝義膽的武將及傾國傾城的美人,銳利的眼神、溫柔的
            淺笑完美地演繹出角色魅力,如此突破性的合作,亦符合本次續作突破性的進化喔! 全面進化
            ,紅將養成不是夢! 在遊戲中,武將有專屬神武、合擊技技能、羈絆效果、天賦...等,
            並搭配提供豐富的養成資源,將使武將在您的指尖綻放出耀眼光芒! 事前預約進行中,
            超值好禮送給你! 即日起,玩家可於官方事前預約活動網站進行預約,有機會抽中UR
            紅將、現金10萬元...等超值好禮。另外,同步開放Google Play、App Store雙平台
            進行預約,凡預約者即可於遊戲上市時,於雙平台獲得最新資訊喔!
            '''
        ),
    )
    assert parsed_news.category == '遊戲'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1626345900
    assert parsed_news.reporter is None
    assert parsed_news.title == '最美卡牌手遊《三國殺名將傳-威力加強版》代言人楊丞琳驚艷現身!'
    assert parsed_news.url_pattern == '2031852'
