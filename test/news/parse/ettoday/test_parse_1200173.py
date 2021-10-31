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
    url = r'https://star.ettoday.net/news/1200173'
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
            假日到了,想爬個山運動一下,卻又不想跑太遠嗎?在內湖就藏著一條「金面山步道」,坐捷運
            就能到,而且還有網美最愛的「剪刀石」可以拍美照,也可以俯瞰整個台北市的美景,宅女
            愛出門 Hi I'm 57就在《旅遊超爽的!》社團中帶大家一起去爬山! 不用再舟車勞頓
            只為了登一座山,你可以直接搭捷運到西湖站,大約10分多鐘的路程就可以抵達
            「金面山步道」。而金面山步道全長約三公里,海拔約150~250公尺,來回需要1~2個小時,宅
            女愛出門 Hi I'm 57建議大家可以在爬山前先在西湖站旁邊的麥當勞吃早餐,補充體力,才
            不會餓昏頭! 金面山,過去曾是清代的打石場,由於這座山的地質中含有石英,所以在陽光的
            照射之下,山頂會閃閃發亮,因此當地人稱這座山為「金面山」,而金面山最為著名的就是山
            頂的「剪刀石」,有分成多個入口可以抵達,可以從竹月寺登山口開始走,距離較短,許多人
            在攻頂之後,會坐在剪刀石上取景拍美照。 攀爬金面山步道的過程中,會遇到許多上坡、大
            石塊以及石板路,頗有運動量,而且下山時會有些陡峭,所以想來這裡爬山的民眾記得要穿一
            雙舒適的運動鞋,步道中間有個涼亭,如果走累了可以在這裡乘涼休息一下,
            宅女愛出門 Hi I'm 57也提醒大家夏天爬山要多喝水避免中暑,也建議大家可以避開假日
            時段來爬山,這樣就能不必人擠人登上山頂獨享美景!
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530147660
    assert parsed_news.reporter is None
    assert parsed_news.title == '台北風景盡收眼底!搭捷運去金面山步道「剪刀石」拍美照'
    assert parsed_news.url_pattern == '1200173'
