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
    url = r'https://www.ntdtv.com/b5/2011/04/14/a518582.html'
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
            國際貨幣基金組織(IMF)4月11號發佈《全球經濟展望》報告警告:中國可能正在形成信貸和
            資產泡沫,最終或將破裂。經濟學家們指出,中國通貨膨脹正進入危險的領域,政府的宏觀
            調控面臨兩難,目前中國經濟正在被推向「滯脹」。 國際貨幣基金組織的報告就中國經濟
            面臨的中期風險,發出異常嚴厲的警告。報告說:中國的信貸和資產價格漲勢「令人擔憂」。
            報告對中國消費者價格漲勢提出警告,預計中國今年通貨膨脹率可能達到5%,超過政府4%的
            目標。經濟學家們普遍認為,中國通貨膨脹的根本原因是貨幣發行量過多及信貸過量。 北京
            天則經濟研究所理事長茅於軾說:「通脹就是前幾年投資太多,而且投到沒有效益的項目上
            賠錢,沒有提供更多的產品。所以要改善我們的投資規則,讓民間投資要啟動起來,現在投資
            都是政府在投,這個是通脹造成的原因。」 據《華爾街日報》報導,哥倫比亞大學商學院教授
            貝姆(David Beim的一篇重要的新論文《中國增長的未來》
            (The Future of Chinese Growth)指出,中國是在利用大量超額貸款保持增長引擎的
            運轉,中國經濟恐怕要踩剎車。 據貝姆研究,中國的固定資本形成總額
            (Gross fixed capital formation)從1980年佔GDP的29%上升至2010年的42%,大多
            數投入的資金來自國有商業銀行給國有企業的貸款,這也是導致低效和腐敗的原因。而且,隨著
            中共政府在本世紀初為中國的銀行清理帳本,價值數千億美元的壞賬奇蹟般地消失了。 與此
            同時,中國通脹目前接近5%。溫家寶在3月份的新聞發佈會上說,通貨膨脹就像是一只老虎,
            如果放出來就很難再關進去。 《新世紀週刊》11號發表經濟學家謝國忠的文章指出,中國的
            通貨膨脹正在進入危險的領域。有跡象表明,通脹的恐慌正在蔓延。囤積現象已不時可見。
            當囤積成為普遍現象時,就很可能爆發社會危機。 至今,北京當局已連續出臺了許多項調控
            政策,但是,物價和房價仍在不斷飛漲。 謝國忠表示,行政權力無法治癒通脹,政府迫使企業
            不漲價只能暫時起作用。當投入成本每年以20%到30%的速度增長時,不提價,就沒有企業能
            生存。 4月5號,中國央行在半年內第4次加息0.25個百分點。謝國忠認為,這仍然遠不足以
            「消除人們對於政府製造通脹的恐懼」。 他警告,資本效率的下降和持續的負實際利率導致
            「滯脹」。嚴重的「滯脹」總是會導致貨幣貶值,並一定會觸發金融危機。滯脹期間將不可
            避免地發生社會動盪。 北京大學經濟學院教授夏業良說:「因為中國人口這麼多,經濟如果
            蕭條了,失業人口增大的話,社會壓力就特別大。而且官方其實更害怕的是失業壓力加大,因為
            那個時候,可能社會動盪不安。」 專家學者們警告,在日趨嚴峻的國內國際環境下,目前中國
            的增長模式正在將經濟推向「滯脹」,最終可能導致泡沫破裂和金融危機,由此引發的社會動盪,
            或使中國的政治體制無法實現和平轉型,同時加大進行根本的政治改革和經濟改革的難度。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1302710400
    assert parsed_news.reporter == '李元翰,柏妮'
    assert parsed_news.title == 'IMF警告中國資產泡沫與破裂風險'
    assert parsed_news.url_pattern == '2011-04-14-518582'
