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
    url = r'https://star.ettoday.net/news/9616'
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
            桃園縣觀音鄉29日凌晨發生一起火燒車意外,一名周姓男子和2名友人在快炒店吃完東西之後
            ,疑似酒駕車速過快,連撞兩根電線桿後車子起火燃燒,3人因為卡在車內無法逃出,不幸死亡
            。 29日凌晨,周姓男子和2名友人駕車離開桃園觀音鄉的快炒店,開到新華路一段與
            66快速道路時,由於當地是90度的大轉彎,疑似車速過快,車子連撞兩根電線桿,立刻燃燒
            ,3人卡在車內,因為重傷無法逃出,結果全部喪命。 回到事發現場,周男駕駛的白色轎車
            整個車身都被撞壞,側半邊嚴重扭曲,顯見當時撞擊力道有多大。死者家屬聽到噩耗
            哭倒在地,想不到一場朋友聚餐竟成為永別。 由於醫生在急救時聞到酒精味,警方初步
            研判是酒駕釀禍,但詳細事故原因仍待進一步調查。
            '''
        ),
    )
    assert parsed_news.category == '社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1322533440
    assert parsed_news.reporter == "黃啟洞,張嘉慧"
    assert parsed_news.title == '疑酒駕連撞2電桿 小轎車起火3死'
    assert parsed_news.url_pattern == '9616'
