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
    url = r'https://www.ntdtv.com/b5/2012/01/01/a640316.html'
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
            印度反貪腐抗議人士經過編組,在跨年夜化整為零埋伏錫克教聖廟「金廟」四周,徹夜等候
            總理曼莫漢今天入廟參拜,再以手機聯繫集結,終於成功的當面向曼莫漢表達抗議。 曼莫漢
            (Manmohan Singh)夫婦今天到位於旁遮普(Punjab)省阿姆利則(Amritsar)巿的金廟
            (GoldenTemple),遭遇反貪健將、資深社運家海札瑞(Anna Hazare)的30多位支持者,
            拉開印度反貪腐組織(India Against Corruption)的布條,當面抗議。 「印度時報」
            (The Times of India)網站今天報導,抗議人士揮舞手中的黑布條,對曼莫漢高呼抗議
            口號。報導說,保護總理的維安特勤人員,對這場早有預謀的抗議,之前竟渾然不知。 參與
            今天抗議行動的辛赫(Harinder Singh),受訪時表示,抗議人士化整為零,以4人1組的
            編組,在跨年夜徹夜守在金廟,等候總理天亮時抵達。 他說,就在曼莫漢即將步出主殿時,用
            手機相互聯絡的抗議人士立刻齊集金廟外,總理一現身便開始呼口號。報導說,後來連一般
            民眾也加入抗議行列。 警方及金廟警衛以人牆隔開抗議人士與曼莫漢。總理夫婦接下來繼續
            參拜「銀廟」(Durgiana Temple)的行程並未受到影響。 「印亞新聞社」
            (Indo-Asian News Service)今天報導,曼莫漢是在印巴分治後,自後來的巴基斯坦
            土地上遷徙到阿姆利則受教育。身為錫克教徒的曼莫漢,上1次參拜金廟是2009年3月。 海札瑞
            的團隊否認動員支持者對曼莫漢抗議。不過團隊強調,類似的自發性抗議,反映人民對貪腐
            橫行和政府毫無做為的不滿。海札瑞團隊認為,包括總理、閣員和其他的政黨領導人,未來
            面臨的抗議將有增無減。 印度國會下院去年12月27日通過政府版本反貪腐「公民監督法」,
            12月29日送交上院審議,但儘管議員們展開馬拉松式辯論直到深夜,最後仍因會期結束而無法
            進行表決,引起各方指責。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1325347200
    assert parsed_news.reporter is None
    assert parsed_news.title == '苦候總理 印反貪人士陳情不滿'
    assert parsed_news.url_pattern == '2012-01-01-640316'
