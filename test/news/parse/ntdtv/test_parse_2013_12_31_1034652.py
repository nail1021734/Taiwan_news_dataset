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
    url = r'https://www.ntdtv.com/b5/2013/12/31/a1034652.html'
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
            俄羅斯伏爾加格勒市近兩天發生的爆炸襲擊,造成的死亡人數已上升到了34人,還有大約
            60人受傷。俄緊急情況部週二出動飛機將一些傷勢嚴重的人送往莫斯科救治。與此同時,
            伏爾加格勒市也進入了警戒狀態。數千名警察在公交車上巡邏,並檢查過往
            車輛。 伏爾加格勒在連續兩天的爆炸襲擊後加強了警力。警方帶著警犬在公共場所,車站
            等地巡邏,以防爆炸事件再次發生。 目前傷員被送往莫斯科接受治療,緊急情況部官員說,
            所有的死者身份也都已獲得鑑定。而心有餘悸的伏爾加格勒市民現在正籠罩在緊張而恐慌的
            陰影之下。 俄緊急情況部心理幫助緊急應變部門負責人奧爾加•瑪卡洛娃:「受害者家人處境
            很艱難。這座城市基本上瀰漫著一種非常緊張的氣氛。人們很恐慌。這就是人們現在需要
            心理幫助的原因。(我們收到)了很多的求助。」 目前為止,還沒有人出面承認發動了這
            兩起爆炸襲擊,不過俄當局已認定這兩起都是恐怖攻擊,令人們擔憂,伊斯蘭分子還會對即將
            到來的索契冬奧會發動襲擊。 對此,白宮國家安全會議(NSC)發言人海頓
            (Caitlin Hayden)30號表示,美國政府願意全力支持俄羅斯對索契冬季奧運會的
            安全保障。同時,美國國務院也在星期一正式發出警告,提醒打算參加索契冬奧會的美國
            公民,務必保持警惕,注意自身安全。
            '''
        ),
    )
    assert parsed_news.category == '國際,社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388419200
    assert parsed_news.reporter == '韋青一'
    assert parsed_news.title == '俄城加強警戒 美願助索契冬奧保安'
    assert parsed_news.url_pattern == '2013-12-31-1034652'
