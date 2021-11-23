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
    url = r'https://www.epochtimes.com/b5/12/12/29/n3763996.htm'
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
            平板電腦和智能手機日益流行,使得PC業一片慘淡,平板電腦和智能手機的優點在於小
            巧與便攜,但是它們無法播放CD,不能進行多任務處理,或創建和管理大型的電子表格
            或圖形文件。要對付這些問題,還得靠PC。 PC市場發展至今,一體機(All-in-One)已
            趨於成熟,各廠商真正需要改變的地方在於如何做到與眾不同、別具一格。多功能一體
            機電腦,外觀簡潔,內部處理器速度快、硬盤容量高,顯示器尺寸大,是PC電腦中的佼佼
            者,以下是3款電腦一體機,可以在電腦市場博得一席之地,和平板機抗衡。 戴爾(DELL
            ) XPS 一體機 (2,000 元) 該款電腦採用27英吋WLED背光(白光LED)顯示屏,分辨率
            達到了2560×1440像素,也就是所謂的WQHD規格。它看起來像電視,配備有電視調諧器
            、 藍光驅動器和遠程遙控,是玩遊戲或編輯視頻的理想選擇。 主要規格: 2 TB 硬
            盤 ;16 GB DDR3 內存 ;DVD + RW 藍光驅動器組合 ;四個 USB 3.0 端口 ;10
            80p 高清網絡攝像頭 ;高清晢視頻HDMI 輸入輸出 ; 它有2560 X 1440 顯示分辨
            率、 Nvidia 2 GB 圖形卡,中央處理品CPU是英特爾Core i7。可選的電視調諧器。
            可選的觸摸屏,使其可用 Windows 8 finger-worthy 功能。 華碩(Asus) ET27
            01 (1,299 元) 華碩一體機有27 英吋的 LED 背光觸摸顯示器, 178 度的可視角度
            ,以及外部低音炮聲波主音頻系統。其1920 x 1080 分辨率稍低,這是它價格較便宜
            的原因。 主要規格: 2 TB 硬盤 ;8 GB RAM ;DVD 藍光讀/寫驅動器 ;4個 USB 端
            口 ;2meg像素網絡攝像頭 ;HDMI 輸入 ;可選電視調諧器。 華碩稱,Asus ET2701提
            供了超清晰接近零失真畫質,板載 DTS Surround Sensation UltraPC ll (DTS聲
            音辨識音頻技術),提供最真實,最具立體音效的聲音。 惠普精英(HP Compaq) Elit
            e 8300 (929 元) 一體電腦憑藉一體化呈現方式所帶來的豐富功能和直觀操作,被越
            來越來的企業和商業用戶所接受。惠普深耕中小企業市場多年,基於對細分市場用戶的
            周全考慮,推出一款集旗艦級性能及商務管理特性於一體的商用一體電腦——HP Compa
            q Elite 8300 AiO Touch,同時這款產品還為有需求的企業用戶提供可定製的觸摸
            解決方案。 惠普這款觸摸式一體台式機,放棄高價策略,以向更多企業推廣。此款機
            採用23英吋寬屏LED背光防眩光全高清液晶顯示器,內置200萬象素(MP)攝像頭和雙麥
            克風陣列,有效節省空間,方便用戶在本地搭建桌面端視頻會議,節省差旅支出。其塑
            料外殼看起來可能過時,但其持久和可靠的 256 GB自我加密固態驅動器就意味著有非
            同小可的計算能力。 作為旗艦級商用一體電腦產品,這款機採用多點光學觸摸技術,能
            夠識別多個手指操作指令,並能有效識別手勢操作。觸摸技術的加入,令用戶和產品之
            間的交互更為友好。 主要規格: 1 TB 硬盤 ;16 GB DDR3 內存 ;DVD + RW 驅動
            器 ;6 個 USB 端口 ;2meg像素攝像頭。
            '''
        ),
    )
    assert parsed_news.category == '科技新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1356710400
    assert parsed_news.reporter == '文芳多倫多'
    assert parsed_news.title == '3款多功能電腦一體機 抗衡平板機'
    assert parsed_news.url_pattern == '12-12-29-3763996'
