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
    url = r'https://star.ettoday.net/news/1200267'
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
            南韓最大色情網站Sora.net一名宋姓負責人長年在海外逃亡,近日自主歸國,隨即被警方逮
            捕。首爾地方警察廳25日指出,45歲宋女因涉嫌違反兒童、青少年性保護,以及情報通信網
            路利用促進暨情報保護等相關法律,已經遭到拘捕。 為躲避警方追緝,宋女長年在紐西蘭生
            活,因護照被外交部作廢而自主歸國。據悉,她曾經向外交部提出告訴,要求撤銷限制她護照
            的處分,最後敗訴。 據警方說法,宋女及其丈夫和另一對夫妻,於1999年9月起,利用海外伺
            服器營運Sora.net,2003年擴大規模,在2016年3月被關閉以前,共有超過100萬名會員,成為
            國內最大規模的色情入口網站。 他們涉嫌促使該網站會員散播不法偷拍、報復性色情影片
            、群交影片等非法色情物,還透過置入賭博網站、性交易、性玩具廣告,賺取高達數百億韓
            元的不當所得。 警方自2015年3月著手調查Sora.net,2016年鎖定6名負責人,首先檢舉了其
            中2名居住在國內的嫌犯。其他4人不斷在海外各國逃亡,而宋女是其中唯一一名仍持有南韓
            護照的嫌犯,最先遭到逮捕,其餘3人目前仍逍遙法外。 該網站許多影片是透過設置在廁所
            或更衣室的隱藏式攝影機拍攝,或是使用者為惡意報復前伴侶,將影片上傳分享,造成許多受
            害女性受到精神傷害,自殺身亡。負責刪除網路使用者個人資料的「數位洗衣機」公司代表
            金浩鎮(音譯)4月受訪時就表示,他曾致電幾名受害者,但常常是由他們的家人接聽,「自殺
            的人不只一兩個。」 對此,南韓當局已經擬定新措施來打擊非法色情網站,包括提供諮詢與
            法律協助、刪除非法影片等等。女性家族部也推出法律修正案,自9月14日起,政府將向加害
            人索取在網路空間刪除非法偷拍影片的費用,也考慮在公共廁所、澡堂、商場與健身房更衣
            室等空間禁用電子攝影器材。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530082560
    assert parsed_news.reporter is None
    assert parsed_news.title == '17年釀多人自殺!南韓最大色情網站Sora.net負責人被逮'
    assert parsed_news.url_pattern == '1200267'
