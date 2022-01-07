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
    url = r'https://star.ettoday.net/news/1200125'
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
            廣東深圳一名張姓婦人於20日上午7時騎摩托車載著兒子們上學,由於小兒子年紀較輕
            ,所以張婦讓他站在腳踏板上,結果突然一個急剎車,導致小兒子從左側摔倒在地,被一旁的
            貨車後輪輾壓過去,當場死亡。 根據澎湃新聞報導,經過警方初步調查,張婦於20日騎車載
            著大小兒子出門,送完大兒子上學後,決定要先返家一趟,卻沒有讓身材矮小的小兒子坐去後
            座,反而讓他一直站在機車腳踏板上。 報導指出,母子倆在7時28分騎車經過某個窄巷,此時
            碰上一輛由薛某駕駛的清潔車,雙方會車時,由於兩邊道路都停有車輛,整條路面較窄,迫使
            張婦必須剎車。但在張婦剎車的過程中,站在腳踏板上的小兒子疑似重心不穩,從左側摔倒
            在地,慘遭薛某駕駛的清潔車左後輪輾壓。張婦心急跳腳,薛某也緊急從車上下車查看,但由
            於小兒子傷勢過重,當場死亡。 影片曝光後,許多網友們表示「這種家長平時麻痺大意,一
            旦發生意外跺腳後悔也晚了......」、「兩路側違章停車是根源」、「完了,這司機真慘。
            」、「停在兩邊的車也一起通通罰了」、「這麼大的車,你讓他先過不好嗎?非要去擠」、
            「真的要瘋掉!心碎!」、「機車前面真的不可以坐孩子」。
            '''
        ),
    )
    assert parsed_news.category == '大陸'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530070980
    assert parsed_news.reporter == '袁茵'
    assert parsed_news.title == '站機車踏板上!母騎車急剎摔落 男童當場遭大貨車輾斃'
    assert parsed_news.url_pattern == '1200125'
