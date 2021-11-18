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
    url = r'https://star.ettoday.net/news/2100192'
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
            台大公衛學者陳秀熙今天表示,隨著COVID-19疫苗施打涵蓋率增加,可逐步放寬公共活動
            、公共運輸、工作場所等限制,但口罩是最後防線,不要第一時間就解除。 台灣大學
            公共衛生學院教授陳秀熙與台大公衛校友群今天舉行COVID-19(2019冠狀病毒疾病)
            防疫科學線上直播,解析國際疫情與防疫策略,並邀請台北醫學大學教授嚴明芳分享
            COVID-19疫苗保護力的相關研究。 陳秀熙提到,觀察全球情況可發現,2劑疫苗平均施打率
            提升至26%,NPI(戴口罩、維持社交距離等非藥物介入措施)限制也有逐漸放寬趨勢;今年
            6月和10月資料相較,以疫苗施打率最高的歐洲,NPI下降幅度最大(33%)。 以台灣為例,
            陳秀熙指出,目前2劑疫苗涵蓋率約18%,NPI限制約36%,可逐步開放公共活動、公共運輸、
            工作場所、學校等,但不要第一時間解除口罩限制,除非等到族群疫苗涵蓋率達90%,不過
            這是很艱鉅的工作,為了讓疫情保持在可容忍範圍內,口罩是最後防線,仍要繼續佩戴
            。 陳秀熙也表示,未來大家應習慣與COVID-19病毒共存,透過疫苗和口服藥物,讓
            COVID-19防疫流感化,變成常態性生活疾病,不要過度迷戀追求清零,也不要把
            隱性感染者當作黑數,應回歸正常心態,只要把病治療好即可。 COVID-19疫苗保護力
            也是大家關注的議題,嚴明芳提到,以色列研究發現,接種2劑BNT疫苗6個月後,IgG抗體
            免疫反應顯著降低,而中和抗體濃度於前3個月迅速下降,之後就維持穩定,在6個月後,
            男性抗體濃度較女性低、65歲以上老年人抗體濃度也比45歲以下族群低。 另外,
            嚴明芳指出,卡達研究也發現BNT疫苗於施打第2劑後1個月達到峰值後就開始減弱,
            7個月後僅剩20%感染保護力,但對於減少重症、死亡,2劑接種後仍維持6個月保護力
            。 疫苗保護力隨時間減弱,也引發國際對施打第3劑加強劑的討論。 台大公衛校友群
            成員張維容指出,以色列是最早開始施打第3劑加強劑的國家,研究發現施打BNT疫苗
            第3劑12天後,比僅施打2劑者可降低症狀感染的效益達11.3倍,降低重症效益也高達
            19.5倍。 另外,張維容提到,美國提供已接種2劑8個月的民眾施打第3劑BNT疫苗,發現
            施打第3劑後1個月比第2劑後1個月產生的抗體濃度上升,年長者上升程度更明顯,對
            Delta變種病毒(最早在印度發現)的保護力也提升;莫德納疫苗多國臨床試驗結果也顯示,
            施打第3劑加強劑後,抗體濃度可提升。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634099640
    assert parsed_news.reporter is None
    assert parsed_news.title == '疫苗涵蓋率提高!學者:可逐步放寬場域「但暫勿解除口罩」'
    assert parsed_news.url_pattern == '2100192'
