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
    url = r'https://star.ettoday.net/news/2053611'
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
            「醫生,我的臉怎麼又紅又熱又癢?大家都以為我喝醉酒真是困擾。」泛紅的臉頰與膿皰,
            是酒糟皮膚炎的特徵,卻常被誤診是濕疹與痘痘,皮膚科醫師周宛儀發文提醒,酒糟皮膚炎的
            治療是一場長期抗戰,要避免許多誘發因素,搭配生活作息正常、飲食節制與改變保養習慣與
            治療才能穩定肌膚。 在台灣,酒糟皮膚炎好發於20至60歲女性,周宛儀解釋,酒糟皮膚炎是
            一種皮膚慢性發炎性疾病,也屬於敏感肌的一種,因皮膚神經血管活性不穩定,容易產生
            紅、熱、癢、刺等症狀,也常因為蠕形蟎蟲共生狀態失衡,形成丘疹膿皰。她說明,酒糟好發
            位置以中臉為主,常呈現「干」字形,包含額頭、鼻子、臉頰兩側、下巴,有時會被誤診為
            成人痘或臉部濕疹,長期使用類固醇反倒讓酒糟雪上加霜。 周宛儀指出,酒糟患者常有
            「先天不足」的基因、體質、免疫失衡、神經血管活性不穩定等問題,再加上「後天失調」,
            例如常做臉、去角質、敷面膜、曬太陽等因素,就可能產生酒糟。她也提到,約有6成以上的
            酒糟患者合併有神經方面的症狀,包含緊張、失眠、焦慮、憂鬱,由於酒糟的泛紅和丘疹會
            嚴重影響外貌,會讓酒糟患者更容易出現憂鬱與沒自信。 依照傳統臨床分類,酒糟有四種
            類型: 一、 紅斑血管擴張型:臉部容易潮紅或出現一條一條血絲(血管擴張),嚴重時甚至
            會出現持續性的紅斑,且不會自然消退。常常會有刺痛與灼熱感、臉部皮膚易乾燥脫屑、
            發紅發癢。 二、 丘疹膿疱型:長得很像青春痘,但卻沒有看到黑頭或白頭粉刺,有時會有
            灼熱或刺痛感。 三、 鼻瘤型(酒糟鼻):皮脂腺和軟組織增生伴隨毛細孔變明顯,好像一顆
            或多顆高爾夫球長在鼻頭一樣,少數案例也可能出現在下巴、臉頰、前額或耳朵
            。 四、 眼部酒糟:大約有兩成的酒糟患者會發生,可能會出現眼睛紅癢、乾眼症、異物感、
            視力模糊、畏光、流淚,甚至產生結膜炎、角膜或是眼瞼炎。 周宛儀提醒,這四種酒糟常
            合併出現,其中以紅斑血管擴張型與丘疹膿皰型最為常見。如果是眼部酒糟釀成眼部不適,
            她建議,要找有眼部酒糟經驗的眼科醫師或皮膚科醫師檢查。 想避免誘發酒糟,周宛儀表示,
            酒糟不單只與蟎蟲有關,也要搭配生活作息與改變保養習慣才能穩定,應避免作息不正常、
            情緒起伏大、日曬、過冷/熱/悶濕環境、不當保養;飲食上,要避免食用辛辣刺激、含酒精或
            太熱的食物,像是火鍋、燒酒雞、羊肉爐與奶製品。 「酒糟治療是長期抗戰」,周宛儀強調,
            酒糟治療相當複雜,在經過正確診斷後,需要花上數月甚至是數年的時間治療,平時更要盡量
            避免誘發,也不可自行停藥。在日常保養方面,她分享,可以溫和清潔、單純保濕、做好防曬
            為原則,選擇溫和、成分單純、低敏、不含酒精/香精/色素/精油的產品,若肌膚穩定後想要
            上妝,則不要使用粉底液、素顏霜等濕粉類產品,可改用乾粉類的腮紅、眼影、蜜粉、
            乾式粉餅,並使用溫和的卸妝用品清潔。
            '''
        ),
    )
    assert parsed_news.category == '健康'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1628917200
    assert parsed_news.reporter == '許若茵'
    assert parsed_news.title == '讓酒糟肌不糟 醫籲做好「4件事」:少吃辣、別碰火鍋!'
    assert parsed_news.url_pattern == '2053611'
