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
    url = r'https://star.ettoday.net/news/1200002'
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
            烏克蘭一對夫婦自親生女兒2歲開始,就多次以性侵的方式虐待女兒,還把性愛的畫面錄製成
            兒童色情影片,再以澳幣70元至140元(新台幣1570元至3140元)不等的價格,販售至澳州與
            亞洲的客戶,時間長達2年。澳洲警方近日與烏克蘭警方聯手破獲,成功拘捕到案。 綜合外電
            報導,該名父親29歲,母親30歲,據稱是表姊弟近親聯姻,兩人性侵4歲親生女兒至少2年,拍攝
            性愛影片販售給主打戀童癖的澳洲和亞洲客戶,並以「加密貨幣」進行交易,影片內容也給予
            保密,而且夫婦每3個月就搬家一次,行事相當謹慎。 澳洲調查人員在一段兒童色情影片中,
            發現一組條形的識別碼,進而找到該代碼與烏克蘭波爾塔瓦(Poltova)地區的商店都有相關,
            於是澳洲警方與烏克蘭警方聯絡,聯手調查後果真在一處屋內破獲父母正忙碌於性侵女兒,現場
            還有琳瑯滿目的性愛影片與性玩具,令警方相當傻眼。 警方已經把所有的物證都扣押,也把
            該對夫婦逮捕到案,不過調查指出,尚不知清楚是否有客戶因下載了這些影片而被逮捕。受害
            的4歲女童隨即至醫院接受檢查,安置在康復中心。律師透露,「女孩的情緒表現非常糟糕,
            她不願意跟任何人說話。」 外媒形容這對夫婦是「邪惡父母」(Evil parents),有其他
            消息指出,這名女童永遠不會回到父母的身邊,社工將會安排她至其他的寄養家庭;
            而如果「邪惡父母」被定罪,將有可能面臨12年有期徒刑。烏克蘭國家警察局直言咒罵:
            「這對夫婦不配做人父母。」
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530069120
    assert parsed_news.reporter is None
    assert parsed_news.title == '性侵4歲女兒!邪惡爸媽親拍「兒童A片」爽賺2年 床上超多性玩具'
    assert parsed_news.url_pattern == '1200002'
