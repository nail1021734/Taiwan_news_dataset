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
    url = r'https://www.epochtimes.com/b5/19/12/27/n11750092.htm'
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
            香港民間人權陣線再次發起元旦大遊行,以「毋忘承諾 並肩同行」為主題,2020年1月1日
            由維多利亞公園步行至遮打道行人專用區。新唐人電視台和大紀元將進行網絡直播, 香港
            示威浪潮已經持續超過半年,踏入2020年仍未見停止之勢。民陣策劃的
            2020年元旦大遊行已經獲得香港警方的不反對通知書。遊行將以傳統的維多利亞公園為起點,
            步行至遮打道行人專用區。時間從1日下午3點到晚上10點。 民陣下午5時許表示,因應警方
            要求需解散遊行,但嚴厲譴責警方濫用不反對通知書的權力中止遊行,以及只給半小時疏散
            、包抄和平遊行人士、對密集人群施放催淚彈等草菅人命的「極度冷血行為」。 警方說,截至
            下午5時15分,共有約47560人由維園出發,當時有約13000人仍然在維園。 民陣則指,今日
            的遊行人數超過6月9日的103萬人。由於被中止,無法完全準確計算今日的遊行人數,但與
            6月9日的遊行情況對比,相信超過當日的103萬人。 民陣此前強調,元旦大遊行還是要向政府
            表明,香港人新一年的願望仍只有「五大訴求,缺一不可」。當天還會有超過40個新成立的
            工會亮相。 民陣表示,迎接2020年,有太多工作需要努力:縱然區議會取得意外戰果,社區戰線
            仍須打穩;黃色經濟圈與工會戰線,要在各行各業被打壓下匍匐前行;街頭行動一旦鬆懈,或
            被政府視為秋後算帳的時機。
            '''
        ),
    )
    assert parsed_news.category == '香港'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577376000
    assert parsed_news.reporter is None
    assert parsed_news.title == '逾103萬港人元旦大遊行'
    assert parsed_news.url_pattern == '19-12-27-11750092'
