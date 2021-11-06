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
    url = r'https://star.ettoday.net/news/1200021'
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
            羅志祥和女友周揚青交往7年,先前傳出他在內湖買愛巢,預計9月時讓女友升格「豬嫂」,他
            雖一度否認傳言,但近日被拍到兩人出雙入對,互動宛如老夫老妻的生活,還一起出席長輩聚會
            陪吃飯,結束後又一起回到他家,被指已經展開試婚生活。 據《鏡週刊》報導,羅志祥21日
            晚間被拍到載著女友周揚青到某泰式餐廳聚餐,同桌的還有3至4位中年男女,看起來像是他們
            的長輩,且彼此之間似乎已很熟悉,兩人用餐時還可以自在地低頭滑手機,且動作隨性自然,他
            一下伸懶腰、一下摀住鼻子,反觀周揚青動作秀氣,和他的互動像極了老夫老妻。 飯局結束
            後,羅志祥和周揚青離開返回內湖住家,羅媽媽則是跟著上了另一台車,試圖幫兒子阻擋跟拍,
            兩人在台灣同進同出,女方甚至還住進他家,被指是開始試婚同居,而另外還有傳言指出,他們
            頻繁與長輩見面,其實是已經在規畫結婚的相關事宜。 事實上,周揚青20日就在IG上PO出在
            家裡的自拍照,寫道:「在家裡無聊的時候怎麼辦,化個妝再卸掉囉~」背景是豪宅客廳,而
            21日就被拍到她陪同羅志祥出席長輩餐會,被推測當時她身處的豪宅就是羅志祥的內湖住所,
            話中的「家裡」二字也引起外界諸多聯想。 外傳羅志祥9月12日和周揚青結婚,交往7年關係
            即將升級,還被爆砸了2.7億元,買下內湖豪宅當作新婚房,不過隨後否認謠言。羅媽媽被問起
            周揚青私下是不是喊媽媽,笑回:「對呀!」證實婆媳好感情,問起婚期時,女友害羞笑回:
            「沒有啦!」不過網友已經在留言串狂催婚,「都那麼直接了為何不結婚」、「感覺你們今年
            結婚。」 羅志祥近期在《這!就是街舞》中擔任導師,提攜後輩不遺餘力,和女友周揚青交往
            多年的他,之前被爆出有想婚念頭,更被爆料2013年花2.18億元買下內湖豪宅當自住房,事隔
            5年,再花2.7億元買下同棟高樓、打通兩戶,疑似是未來的結婚新房,身價近10億元的他,
            等於在該社區就擁有4戶住宅,近200坪空間總價約4.9億元。
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530053040
    assert parsed_news.reporter is None
    assert parsed_news.title == '羅志祥、周揚青爆「台北試婚ing」 女方PO照炫「新家」露餡!'
    assert parsed_news.url_pattern == '1200021'
