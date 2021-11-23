import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/19/5/13/n11255964.htm'
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

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
           2019年5月16日,來自世界各地的萬名法輪功學員代表,將匯集世界之都紐約,舉辦盛大遊行,
           以慶祝法輪大法洪傳世界27周年。新唐人電視台作為海外最大的中文電視媒體,將全程直播遊行
           盛況。大紀元網站、新唐人網站、社交媒體等也將同步直播。 遊行將從5月16日早10點30分
           開始,行經世界之都紐約曼哈頓最繁華的街道,從聯合國前的哈馬舍爾德廣場為起點,穿越
           曼哈頓中城42街,途經大中央車站、布萊恩公園、時代廣場,直到中領館,全長2英里。 直播
           節目將實時呈現遊行現場畫面,從「天國樂團」演奏的雄壯行進軍樂、深具中國傳統特色的
           腰鼓表演,到身著華麗民族服飾的世界各國法輪功學員、繽紛多姿的花車、燦如花海的各色彩
           旗條幅、法輪功功法演示等。觀眾還有機會一睹遊行路線上的大中央車站、布萊恩公園、時代
           廣場等紐約著名地標。 此外,直播節目還將有親歷者解疑:為什麼中共口中「唯心、迷信」的
           精神信仰,卻讓從美國知名高校的教授、到澳洲富豪的主流人士們感到醍醐灌頂?為什麼這個
           源自中國的修煉方法,能使全世界各族裔的民眾獲得身心昇華?為何這個遭到中共迫害的信仰,
           能廣泛受到國際政要名流的褒獎與讚揚? 節目中也將帶您觀察,中國大陸正進行退黨大潮,逾
           三億民眾退出中共以及相關組織,醞釀著一個沒有中共的未來? 新唐人多位當家主播、記者——
           陳曉天、姜光宇、林瀾、JoJo、李蘭、宇亭將帶領觀眾,直擊遊行進展情況。知名時事評論員
           橫河,法輪大法信息中心發言人張而平,也將做客直播間分享觀感。
            '''
        ),
    )
    assert parsed_news.category == '北美新聞,美國華人'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1557676800
    assert parsed_news.reporter is None
    assert parsed_news.title == '2019法輪大法日 紐約萬人大遊行'
    assert parsed_news.url_pattern == '19-5-13-11255964'
