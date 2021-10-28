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
    url = r'https://www.cna.com.tw/news/aipl/202012120087.aspx'
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
            新台幣強勁走升、利率來到歷史低檔,讓民眾的理財課題增添難度,專家建議,
            國際局勢動盪不安,宜採「槓鈴式策略」;至於其他外幣,不妨先觀望局勢發展,
            或採定期定額換匯服務,降低平均成本。 「現在單純持有現金最不划算」,
            星展銀行(台灣)財富管理投資顧問部副總裁陳昱嘉表示,當前利率環境來到歷史低點,
            現金幾乎沒有孳息,而且資金市場寬鬆情境料將持續,加上市場樂觀期待明年經濟復甦、
            企業獲利回升,股市等風險性資產仍能有表現空間,此時資產配置更顯重要。 陳昱嘉說明,
            槓鈴式策略指的是一邊配置成長型資產,意即雖然波動風險較大,但具有成長趨勢,如科技、
            醫療保健等類股,在數位經濟時代來臨、後疫情時代以及人口老化等大趨勢之下,上述題材
            不太會出錯,另一邊則配置波動風險較小的收益型資產。 眼見國際股市不斷飆高,投資人
            多少會擔心「還能進場嗎?」陳昱嘉指出,市場瀰漫「害怕錯過」
            (FOMO ,Fear Of Missing Out)的情緒,因此可以看到即便股市回檔修正一兩天,
            很快又會反彈向上、持續創高,關鍵在於市場錢太多、利率太低,這兩大條件將支撐資本市場
            榮景持續。 若是較保守的投資人,陳昱嘉說,同樣適用槓鈴式策略,只是資金可以不用放太多
            在股市,重心放在固定收益部位,像是高收益債券、亞洲債券、高配息股票等均可留意。 過去
            許多民眾習慣將錢放在美元定存,如今美元弱勢、換回新台幣又會賠了匯差,手上美元該
            何去何從,恐怕是許多小資族、保守型理財民眾困擾的事情。 一家國銀資深主管建議,
            新台幣目前相對強勢,台股報酬率也相對不錯,投資人可保有既有的台幣部位,其他外幣幣別
            則「一動不如一靜」。 凱基銀行財富管理處資深協理張冠雄分析,現有的美元部位,
            一方面可以考慮透過銀行提供的定期定額換匯服務,降低平均換匯成本;其實美元計價的商品
            很多,可將資金分成短、中、長期,3至5年短中期資金以定期小額投資級債券基金為主,
            維持資金隨時可贖回的流動性,5年以上資金則以分期繳美元保單為主,發揮強迫儲蓄功能,
            同時避免提早解約,造成本金損失。 他透露,現在有滿多投資人看好中長期債券ETF,打算
            逢低布局,但不論投資哪種類型的產品,如果是採固定利率計息,未來幾年恐面臨「利率反轉」
            風險,不可不慎。 舉例來說,許多中長天期債券ETF都是固定利率,雖然美國聯準會(Fed)
            先前表態在2023年以前不會升息,但是隨著疫苗問世,且很快要進入大量施打階段,若確定
            有效,可能帶動通膨上升,利率政策也將有變化,選擇過長天期且固定利率的商品,一旦碰到
            利率反轉,收益率將比預期大幅降低。 儘管美元持續走弱,銀行業者提醒民眾,以英鎊、瑞郎
            等非美貨幣而言,今年以來都升值不少,進場點相對已經沒那麼好,宜先觀望重大變數的發展,
            再來進行下一步布局。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1607702400
    assert parsed_news.reporter == '潘姿羽、吳佳蓉台北'
    assert parsed_news.title == '台灣錢潮滾滾/強勢新台幣成理財新課題 專家建議槓鈴式' +\
                                '策略因應'
    assert parsed_news.url_pattern == '202012120087'
