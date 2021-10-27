import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201412300008.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            義失火渡輪10死疑41失蹤 搜救未停 義大利渡輪「諾曼大西洋號」在波濤洶湧的亞得里亞
            海域失火後,救難隊36小時內撤離船上400多人,但死亡人數今天增至10人,且仍有40多名
            人員下落不明。 目前不清楚諾曼大西洋號(Norman Atlantic)失蹤乘客是否溺斃或
            其他死因,也不確定人員名單是否有誤。 目前搜救尚未落幕,儘管入夜好幾小時,義大利
            海軍持續在渡輪所在的阿爾巴尼亞附近海域搜尋遺體。 法新社報導,義大利交通部長
            盧比(Maurizio Lupi)證實,直升機在異常惡劣天候下展開24小時救援行動,一共安全
            撤離427人。 渡輪清單列有478名乘客和組員,目前確定10人罹難,代表仍有41人下落
            不明。 盧比表示,目前不清楚人數不符是否因為乘客名單有誤,還是有人登記後未登上
            渡輪,或是有人在渡輪中途行經希臘伊高曼尼沙(Igoumenitsa)時下船。 盧比說:「這是
            為何我們持續努力(搜救),我們不知道確切人數。」 路透社引述盧比的話報導,船長賈科
            馬奇(Argilio Giacomazzi)等船上所有人全撤離後才棄船。他還說有56名船員
            撤離,而獲救的人中有234名希臘人、54名土耳其人、22名阿爾巴尼亞人和22名義大利
            人。 希臘報導則說仍有38人失蹤,盧比不會證實這則消息,他表示現在就說有多少人失蹤
            還太早。 義大利海軍今天指出,在亞得里亞海上1艘渡輪因起火造成的死亡人數已增加至
            10人。 由於「諾曼大西洋號」渡輪清單的正確性仍不明朗,在這項數據更新前,義大利
            官員宣布應該在渡輪上有超過40名乘客下落不明。 義大利今天指出,渡輪
            「諾曼大西洋號」在地中海上起火,死亡人數已增至8人,另有427人獲救。 義大利當局
            表示,救援人員正在調查是否還有更多人失蹤。 義大利交通部長盧比(Maurizio Lupi)
            說,下午稍早時,渡輪上人員已完全撤離,有427人獲救,包括56名組員在內。 原本渡輪清單
            列有478名乘客和組員。 盧比表示,現在猜測是否仍有人失蹤為時過早,但表示可能有人
            預留位置,但未登上渡輪。 他說,他們正就獲救人員姓名與渡輪清單進行核對。 在獲救
            人員中,有些未名列渡輪清單上,意味船上些人是偷渡。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1419868800
    assert parsed_news.reporter == '羅馬/雅典,羅馬,羅馬'
    assert parsed_news.title == '義渡輪失火死亡人數增至10人'
    assert parsed_news.url_pattern == '201412300008'
