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
    url = r'https://www.epochtimes.com/b5/13/2/1/n3790819.htm'
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
            經常有朋友問我,要買什麼樣的新車才是好車?通常我的回答是:「除了中國大陸自主品牌的
            車以外,都是好車!」(Euro NCAP曾將中國某些品牌送去測試車輛,評為最不安全的車)。因
            此,你不管買什麼用途的車輛,它的先決條件就是「安全考量」。此外還必需符合你的購車
            需求,否則就算送你一輛頂級勞斯萊斯,你也不一定養得起用得起是吧!筆者舉個活生生買錯
            車的例子,給讀者朋友們作為借鏡。 位朋友他屬中產家庭,開2,000c.c.排量房車作為交通
            工具,每天先送小孩上學送太太上班再開車到自己公司,有時需帶年邁父母去運動或健診,偶
            爾也會全家開車出遊,過著和樂幸福的日子。有天他氣急敗壞的告訴我說:「我買了一輛新
            車但很爛!開上路噪音很大乘坐不舒服,座椅硬邦邦還很耗油,父母乘坐不舒服,噪音大講話
            也聽不清楚。」父母常為此事與他嘔氣呢!原來他買了一輛渦輪增壓(Turbo)2,000c.c.排量
            性能房車,此車為追求高性能,輪胎加大了,為提升支撐性懸吊系統也調校至偏硬的狀態,那
            當然胎噪就大,乘坐也不舒服也比較耗油,但喜歡操控性能的駕者們,很可能會認為它是一輛
            好車,也可能是購車的選項之一。可這輛車的功能性就不符合這位朋友家庭房車的使用需求
            ,一家老小經常乘用的交通工具除安全為先決條件外,還需考量舒適性、經濟性、實用性與
            保修的方便性。 因此真正能符合你預算及需求的車種,才是你理想的購車首選。 購車三要
            素 信心、需求、購買力 在新車銷售領域中,購車三要素是買賣雙方都需慎重考慮與評量之
            所在。其中尤以顧客購車需求最為重要,那購車需求是什麼呢?簡單的說也就是你最原始的
            購車動機,舉凡購車目的是商用、家用或是多用途、預算多少,誰開這輛車、誰經常乘用、
            行車距離與路況等都是要優先考量的。 再從銷售面來談,銷售顧問在推銷產品之前,必需對
            客戶進行許多的提問與交流,以確實掌握顧客的購買動機及需求,並進行需求分析最後推薦
            一輛最符合顧客需求的車種給客戶。這是銷售顧問的責任與義務。 然而有少數銷售顧問未
            能站在顧客的立場為顧客設想,也沒把顧客買車當成自己或家人買車,因此忽略了最重要的
            「需求分析」銷售流程,這會讓顧客面臨買錯車的嚴重後果,探查其原因可能是: 1.新進銷
            售人員未受此訓練還不會為顧客做需求分析。 2.公司庫存車種不完整沒有符合顧客的選項
            。 3.公司政策先推庫存較多的車型。 4.銷售顧問個人推單價高或獎金多車款,前所述案例
            即為銷售顧問為了自己個人利益,推薦一輛不符合顧客需求的車子給了顧客,對顧客負面影
            響是長遠而嚴重的,因為一輛車少說也要用3~5年。 此筆者建議讀者諸君在購車前,先將自
            己的購車需求詳盡羅列後,先期進行需求分析! 你是買商用車、家庭用車或綜合用車、是男
            生開還是女生開、開長途還是市區使用,經綜合判斷後先選出車種,如:轎車是三廂還是兩廂
            、休旅車五人座還是七人座、全商用車或半商用車(後廂是可拆卸的一排椅、兩排椅或選擇
            全空)、吉普車兩輪或四輪傳動等等。 當你有初步的車種選擇後,再去汽車公司與銷售顧問
            洽談,並與銷售顧問從長諮商,有這樣的先期準備必然對你日後的購車有莫大的助益。 購車
            地圖 你這次買車預算多少? 買車目的? 家庭用 商業用 綜合用途 買車是誰在開? 男
            生 女生 買車是當 交通工具 注重操控性能 買這部車偶爾會 採買 載貨 經常開 長
            途 短途 高速路 市區 困難地形 以上問題的答案作為你選擇車種的指標
            '''
        ),
    )
    assert parsed_news.category == '科技新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1359648000
    assert parsed_news.reporter is None
    assert parsed_news.title == '如何買新車過好年'
    assert parsed_news.url_pattern == '13-2-1-3790819'
