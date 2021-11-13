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
    url = r'https://star.ettoday.net/news/2100012'
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
            農委會配合行政院五倍券加碼,祭出每張面額888元「農遊券」,連續4週抽出88萬份!
            今(13 日)上午10點30分首抽約22萬份,現場準備樂透機和彩球,抽出身分證後2碼或
            3碼「89」、「32」、「54」、「597」、「453」、「152」,總計230,695人可獲得
            農遊券。幸運中籤者,下午5點就會陸續收到簡訊通知;而未中籤者也別氣餒,只要登記,未來
            三週還有3次抽籤中籤機會! 今(13)日由農委會主秘范美玲進行抽籤,此次共超過1071萬
            人有抽籤資格,最後抽出230,695人幸運中籤。其中身分證末2碼「89」117,267人;身分證
            末2碼「32」3985人;身分證末碼「54」共86,123人;「597」共405人;「453」
            共11,146人、「152」共11769人。由於本週超出預定的22萬張,將於第四週調整抽籤
            張數。 農委會提醒,農遊券仍持續開放申請登記,有興趣的民眾可在10月29日晚上11時59分
            前,至五倍券官網勾選參加農遊券抽籤。相關農遊券訊息可上農遊券網站查詢,或洽業者
            客服專線07-9700275,以及消費者客服專線07-9752215。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634092800
    assert parsed_news.reporter == '林育綾'
    assert parsed_news.title == '「888元農遊券」首波抽籤出爐!身分證末碼這6組中獎快來對'
    assert parsed_news.url_pattern == '2100012'
