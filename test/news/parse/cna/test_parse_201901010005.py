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
    url = r'https://www.cna.com.tw/news/aipl/201901010005.aspx'
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
            今年台北101煙火秀特別不一樣,長達360秒的煙火動畫秀中,透過9大主題,向社會大眾展現
            台灣的多元與文化,最後以「勇敢自信,世界同行」為煙火秀結尾,祝福大家2019年有好的
            開始。 今年跨年雖然天公不作美,北部地區整天陰雨綿綿,不過隨著時間接近1月1日零
            時,雨勢愈來愈小,人潮愈來愈多,而且人潮中可以發現不少異國面孔,大家都前來參與這
            一年一度的盛事。 台北101煙火已邁入第15年,今年煙火有1萬6000發,第一發到最後
            一發長達360秒,主秀足足比去年多了60秒,斥資新台幣6000萬元;儘管濕冷的天氣讓台北
            101罩上一層薄紗,也稍微影響能見度,但色彩斑斕的煙火與炫目的動畫,還是讓跨年民眾
            High翻天。 為了讓民眾能夠興奮地迎接2019年,台北101安排了18組名人與民眾一起倒數
            ,當藝術大師朱銘、霹靂布袋戲一哥素還真、旅美棒球好手陳偉殷、極地冒險家林義傑、前
            亞洲球王盧彥勳、中職看板球星彭政閔、世大運中華女排隊長陳菀婷、前日本奧運桌球選手
            福原愛和世大運金牌桌球選手江宏傑等人陸續出現在台北101的巨型燈網T-Pad上,民眾
            也跟著驚呼連連。 90秒的名人倒數結束後,隨即進入民眾引頸期盼的煙火動畫秀,今年
            一大亮點是煙火動畫呈現了代表台灣各個面向的9大主題,分別為「夜市、名食」、「各行
            各業」、「地理環境」、「醫療、技術」、「科技、代工」、「水果王國」、「自由、民主
            」、「信仰、力量」、「多元包容」。 「夜市、名食」主題中,完美呈現台灣「美食
            天堂」的稱號,珍珠奶茶、雞排、小籠包、臭豆腐、粽子等熟悉的小吃陸續出現,讓民眾
            會心一笑。 緊接著是「各行各業」,呈現出台灣的百工精神,以及台灣人友善、勤奮和
            踏實,「地理環境」則展現台灣被譽為「福爾摩沙」的美麗山水與自然生態,「醫療、
            技術」、「科技、代工」、「水果王國」分別展現台灣的不同面貌。 台灣讓人喜愛的不僅
            只是美食、水果,更重要的是民主自由以及多元包容的社會氛圍,台北101特別把這樣的元素
            加入煙火動畫中,讓全世界的人都能透過煙火動畫,看到台灣最美麗、最吸引人的
            地方。 隨著9大主題結束,煙火秀也進入下半場,T-Pad上陸續出現日語、韓語、英語、越南
            語、菲律賓語、阿拉伯語、法文、印度語等16國語言的問候語,代表台灣的多元包容和幸福
            共好,向世界傳遞祝福。 今年煙火秀不僅帶來一場華麗的視覺魔法,台北101在聽覺上也
            下了不少功夫,除了請來金馬獎最佳原創電影音樂得主林強編寫主旋律、希望兒童合唱團
            演唱,並邀請曾獲得金曲獎最佳重唱組合、最佳原住民語專輯獎歌手阿爆為煙火動畫
            獻聲,融合電子音樂和孩童聲樂的創新形式,希望帶給民眾一場感官盛宴,讓大家在2019年
            有個美好的開始。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1546272000
    assert parsed_news.reporter == '潘姿羽台北'
    assert parsed_news.title == '跨年煙火101秀9大主題 讓台灣被世界看見'
    assert parsed_news.url_pattern == '201901010005'
