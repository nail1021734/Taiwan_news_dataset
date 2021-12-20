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
    url = r'https://star.ettoday.net/news/2104622'
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
            政府預計在溫室氣體減量及管理法修正案,將2050年達到淨零碳排放加入(或稱碳中和)。
            近年討論永續發展,聚焦氣候變遷,因而溫室氣體(主要是二氧化碳)減排與碳中和,形成
            改善全球暖化核心。 在台灣,提早受此趨勢影響的企業(稱受碳中和影響企業),皆經濟
            成長主力,我感受到這些企業有投入心力面對此一挑戰,但對能否達成目標感到憂心。 要
            達成碳中和,從全球到各國,亦蔓延到國際大型企業與投資機構。不僅是聯合國、歐盟的
            倡儀,美國、日本、南韓、中國等國家已宣布2050或2060年達到碳中和目標;甚至一些
            國際企業宣布提早2030年達到,當然此目標是含其供應鏈廠商。並且,今年三月由大型
            投資機構發起的淨零排放投資架構,希望協助全球2050年達成;此趨勢比之前責任投資,
            更加明確與精進。 台灣減碳與全球的「距離」 台灣暖化問題,相對全球平均狀況如何?
            根據八月台灣氣候變遷科學團隊資料,過去110年(自1910至2020年)台灣平均氣溫上升
            約1.6度;而我查詢全球同時期平均氣溫增約1.2度,因此台灣比全球平均更嚴重。 有關
            台灣溫室氣體總排放量,從1990年1.3億公噸,持續翻倍成長到2018年2.9億噸,中間在
            2007年達到最高近3億公噸;2008、2009年金融風暴時有下降,之後回升,接下來十年下降
            幅度仍不明顯。甚且,平均能源碳排放量,每人一年為11.3公噸;要實現巴黎協定寄望的氣溫
            增幅攝氏1.5度目標,2030年每人只能排放2.1公噸,相當於大減8成。德國一家機構發布
            氣候變遷績效指標,台灣整體排名依然在後段班,主因也是「人均排放」太高。 要達到碳
            中和,最基本要檢討的是發電結構。政府原本設定今年再生能源發電
            (主要是太陽能、風力、水力)占比應達12%,但8月只5.5%,更令人憂心2025年20%目標
            是否天邊的彩虹般?台灣能源政策受到底下因素限制:非核家園、電價便宜、電力供給要
            穩定,且現在又加入碳中和目標,令人感到發電結構與上述因素存在悖離困境。 「碳中和」
            影響台企 一旦發電結構大部分是火力,碳排放就降不下來,台灣難達到碳中和;位在國際
            大型企業供應鏈的台企,更不容易提早達到碳中和要求,而有失去訂單疑慮。再者,
            石化業、鋼鐵等排碳大戶,未來幾年若要出口歐美市場,可能被課徵昂貴碳排放費(或稱碳稅)
            。以上就是受影響企業憂心所在。 受碳中和影響企業,如何面對「即將到來、影響又甚大」
            挑戰?首先,董事會與管理階層要有正確認知,詳細盤查與衡量溫室氣體排放量,範圍包括生產
            或提供服務的直接排放、用電產生的間接排放,及供應鏈排放。 其次,進行上述範圍減排的
            設算、目標擬定與執行,作法包括低碳排放的產品設計、增強能源使用效率、生產過程技術
            與材料創新等。再者,進行抵換,包括植樹,復育熱帶草原等;另外,亦可購碳權、再生能源
            憑證抵換。然而上述作法需台灣發電結構改善或政府效能配合,若無法得到支持,企業可能
            就得到國際市場購買或投資,藉以進行抵換措施。
            '''
        ),
    )
    assert parsed_news.category == '雲論'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634623800
    assert parsed_news.reporter == '葉銀華'
    assert parsed_news.title == '全球「碳中和」風暴襲來 企業如何超前部署?'
    assert parsed_news.url_pattern == '2104622'
