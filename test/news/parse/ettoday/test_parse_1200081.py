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
    url = r'https://star.ettoday.net/news/1200081'
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
            正所謂「遠在天邊,近在眼前。」台中的飼主李秋滿日前在臉書分享一則影片,畫面中,眼睛
            大大顆的跳跳看似著急地尋找寶貝娃娃,只見牠都快把整個房間都翻遍了,但仍努力地尋找,
            可是小恐龍明明就擺在眼前啊!這讓坐在一旁頻頻提出「暗示」的馬麻忍不住爆了粗口,笑
            翻許多網友! 其實影片中的綠色恐龍,跳跳和主人都各有一隻,只是馬麻的娃娃比較大啦!李
            秋滿說,「那天跳跳想要我那隻大隻的恐龍,我故意不給,叫牠去玩自己的那隻,結果跑到小
            恐龍面前,就好像不存在一樣,所以我才會爆粗口哈!然後叫牠頭往下低,還故意跟我唱反調
            。」 今年2歲的跳跳是隻小男生,從小個性活潑又愛玩的牠非常親人,尤其是對女生。李秋
            滿表示,「2年的某一天,弟弟要出門時發現門口有聲音,結果是才2個月大的跳跳!可能是流
            浪太多天了,正在畚斗那附近找吃的,因為當時牠身上很乾淨,一開始以為是有人養的,只是
            偷跑出來;後來知道跳跳身上沒有晶片,所以就收編了。」 影片上傳到臉書寵物社團「米克
            斯傳奇」後,引發上百名網友熱議,許多人都在底下紛紛留言表示,「太好笑了 !往上看的眼
            神太萌了!」、「故意的哦」、「好叛逆XDD」、「圓圓的眼睛好可愛,來騙肉的」、「媽媽
            台語很厲害哈哈」、「快被氣死了」、「故意的無誤」。
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530095580
    assert parsed_news.reporter == '吳鎮良'
    assert parsed_news.title == '大眼汪找不到「正前方小恐龍」 台中媽激動爆粗口網笑翻'
    assert parsed_news.url_pattern == '1200081'
