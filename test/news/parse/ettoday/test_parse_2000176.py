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
    url = r'https://star.ettoday.net/news/2000176'
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
            南韓近日又驚傳接種疫苗後死亡的案件!釜山一名51歲的男子,根據政府近期推出的
            「剩餘疫苗」(잔여백신)制度預約施打阿斯特捷利康(AZ)疫苗,沒想到經過4天後運動時
            突然呼吸困難、心跳停止,即使施行心肺復甦術、緊急送醫治療,卻還是於第9天不治身亡
            。家屬痛訴,男子生前沒有任何慢性疾病。 根據《韓聯社》,該名男子於5月27日下午4時
            前往釜山市釜山鎮區開琴洞某間韓醫院(傳統醫學)預約接種AZ疫苗,起初的幾天內並無任何
            特別的副作用與症狀,日常生活一切照舊;豈料接種後的第4天、5月30日上午8時30分在
            住處做簡單的運動時,突然感到呼吸困難、甚至心跳停止。 男子的家屬當場為其施行
            心肺復甦術,並撥打119報案,緊急送往釜山市沙上區某間綜合醫院急診室進行搶救,雖之後
            入住加護病房持續接受治療,但卻始終無法恢復意識,在接種疫苗後的第9天、6月4日下午
            4時撒手人寰。 醫院事後診斷出,男子應是罹患「蜘蛛膜下腔出血」(SAH),認為男子死因與
            疫苗接種的因果關係模糊,不過這個結果教家屬根本無法接受。家屬表示,「死者是因接種
            疫苗副作用才死亡,防疫當局進行疫調的速度太慢,才造成死因與接種疫苗的因果關係調查
            變得更為困難。」 家屬補充道,「平常他沒有任何慢性疾病、也未定期服用任何藥物,
            規律運動、身強體壯,不過在接種疫苗後卻突然昏倒,無法恢復意識,最後才死亡。我們認為
            他的死因,與接種疫苗有關。」 家屬強烈反對為死者進行解剖驗屍,「我們告訴保健所
            (衛生所),男子在接種疫苗後死亡,然而對方的醫師卻告訴我們,如果沒有遞交醫師意見書,
            就無法進行死因與接種疫苗有關與否之調查,讓我們覺得很誇張。」 根據南韓疾病管理廳
            的統計數據,截至6月6日0時為止,共有759萬5072人完成新冠疫苗第1劑接種,其接種覆蓋率
            達14.8%;完成第2劑疫苗接種者則為227萬9596人,佔總人口比率為4.4%。其中在第一次
            接種中,AZ疫苗施打者為494萬8641人、輝瑞疫苗施打者為264萬6431人。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1622956080
    assert parsed_news.reporter == '羅翊宬'
    assert parsed_news.title == 'AZ疫苗又傳死亡案例!51歲男接種突「呼吸困難」 心跳停止不治亡'
    assert parsed_news.url_pattern == '2000176'
