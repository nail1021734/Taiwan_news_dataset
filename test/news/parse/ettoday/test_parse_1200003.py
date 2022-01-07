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
    url = r'https://star.ettoday.net/news/1200003'
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
            台南市一名就讀國中一年級、家境單親清寒的13歲李姓少年,從小學五年級開始,他就利用
            自己的「年齡輩份」,霸凌勒索大他1歲的「姪子」,3年時間共拿到6萬多元,對方家屬察覺
            有異,事情才曝光;經老師約談,少年嚇得在白紙上寫下高達97筆帳目,包括劃除未得逞的次數,
            令校方錯愕。 根據《蘋果日報》報導,警方調查,就讀國中二年級的14歲被害少年時常向
            阿嬤要1000元鈔票,繳完書錢沒多久又要繳補習費,察覺有異,因此向導
            師反映此事,才知道原來少年長時間被人勒索,對方竟然是小他1歲、住附近且有親戚關係的
            13歲「叔叔」。 由於論輩分得稱對方「叔叔」,被害少年從小學六年級開始就被各種名目
            勒索要錢,雖然兩人從小學畢業後各自就讀不同的國中,但放學或假日後,「叔叔」仍會霸凌
            威脅,讓少年相當害怕,只好向家人騙錢或偷錢,再帶到學校門口交易,每次約是從1、200元
            至1000元鈔票不等。 報導指出,校方啟動機制輔導調查,要求李姓少年寫下悔過書,他認錯
            寫下犯案次數、參與人數、索討金額等事項,寫了滿滿5張,總計97筆帳目,誠實吐露這3年來
            所有的勒索。校方起初懷疑少年亂寫,但他則解釋,有些沒有順利拿到錢,開始拿紅筆扣掉近
            50筆紀錄,估得手金額高達6萬多元。 李姓少年否認幕後有指使者,僅是他一人犯案,校方兩
            個月來共輔導各8次法治教育與人際關係。調查指出,李姓少年來自單親清寒家庭,父親無業
            ,他不愛寫作業、成績中下,但他卻擁有超強記憶力,記下97筆紀錄,因此校方認為欠缺栽培,
            得加強學科基礎教育,再鑑定資優生為否、並輔導他步入正軌。
            '''
        ),
    )
    assert parsed_news.category == '社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530056700
    assert parsed_news.reporter is None
    assert parsed_news.title == '小學生勒索學長97次!3年共拿6萬多元 校方驚見「超強記憶力」'
    assert parsed_news.url_pattern == '1200003'
