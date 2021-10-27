import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/12/17/a633460.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            本月16日,一份獨立報告發現,12名昆士蘭人因等待治療時間過長或治療被拖延而不幸
            死亡。 據澳新社消息,昆省健康質量與投訴委員會(HQCC)對2009年7月1日至2011年6月
            30日間收到的337例有關就醫問題的投訴進行了分析。這份標題為「我們為甚麼等待?」的
            報告發現,在一份等待名單中,1名病人因等待時間過長死亡,另有7人造成永久性傷害。由於
            醫院內部管理協調不善而造成的拖延,如錯誤轉診、不適當或不充分的檢傷分類治療,使得
            11名病人死亡,17人留下永久性傷害。 從投訴比例看,公立醫院占52%,全科醫生22%,私立
            醫院6%。大部份投訴是針對布里斯本的醫療機構,占總比例的43%,黃金海岸12%,陽光
            海岸7%。 委員會主席赫伯特(Cheryl Herbert)本週五表示,這份報告凸顯了醫療機構
            需要改善,包括更好的臨床交接培訓和檢傷分類治療。她說:「不能讓病患及時就醫,是提高
            醫療保健服務質量最大的障礙之一,可能提高病患出現反面結果的風險,包括健康狀況嚴重
            惡化、加大永久性傷害或死亡。」 昆省省長布萊(Anna Bligh)則表示,昆省醫院正在改進
            當中,改善速度之快在澳洲史無前例。「我們現在擇期手術等待時間最短,急診等待時間改善
            的速度比其它任何省份都快。」她在一份聲明中說。
            '''
        ),
    )
    assert parsed_news.category == '海外華人'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1324051200
    assert parsed_news.reporter is None
    assert parsed_news.title == '十餘名昆省病人因等候治療死亡'
    assert parsed_news.url_pattern == '2011-12-17-633460'
