import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.storm


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='風傳媒')
    url = r'https://www.storm.mg/article/4031507?mode=whole'
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

    parsed_news = news.parse.storm.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            全球128國11月1日在第26屆聯合國氣候變遷大會(COP26)簽署宣言,承諾在2030年前終結
            森林濫伐。然而,擁有世界第三大雨林、身為簽署國之一的印尼,4日卻立刻翻臉不認帳,
            認為最新氣候目標與印尼的國家發展有所衝突。印尼環境部長更在推特抗議:「強迫印尼在
            2030年終結森林砍伐,既不公平、也不恰當。」 根據《路透》(Reuter)報導,代表印尼
            遠赴格拉斯哥(Glasglow),參與聯合國氣候大會的印尼環境部長西蒂
            (Siti Nurbaya Bakar),4日在推特表示,在印尼總統佐科威(Joko Widodo)
            執政下,國內所有發展計畫都不能被「減少碳排」、「終結森林濫伐」等原因阻礙,
            暗指最新簽署的氣候協定,和印尼國家發展計畫有所牴觸。 西蒂表示,各國對於
            「森林濫伐」一詞的定義大不同,用歐洲標準來規範印尼非常不公平。她強調,
            印尼計畫在2030年前,透過減少森林砍伐和復育森林,達到「淨零排放」,而非終結森林濫伐。
            隨後,西蒂又推文表示:「佐科威總統的指示非常明確,政府的開發必須符合減少森林砍伐
            和減碳的政策,這兩者之間必須取得平衡。」 同日,印尼前外交部長馬亨德拉
            (Mahendra Siregar)在一份聲明中指稱,「2030前終結森林濫伐」並非這次氣候大會
            承諾的一部分。他進一步地解釋,「這次承諾的氣候目標並不是要完全停止砍伐森林,
            而是要確保林地不會出現淨損失(net loss)。」 馬亨德拉隨後也向《路透》補充,
            在最新氣候協定中提到「2030年停止並減緩森林損失和土地退化」的目標,印尼將其理解
            為「永續的森林管理」,而非「結束森林濫伐」。 《路透》4日則表示,目前印尼環境部
            尚未針對此事出面澄清,也無法得知佐科威政府的態度。然而,西蒂的發言卻已在網路上
            引起眾怒。網友巴瑜 (Bayu Satrio Nugroho) 在Instagram痛批西蒂:
            「你到底是環境之友,還是金錢之友?」 根據聯合國和印尼官方數據,印尼擁有世界第三大
            熱帶雨林,僅次於亞馬遜和剛果雨林,是全球重要的「碳匯」
            (carbon sink,儲存二氧化碳的天然或人工機制)之一。儘管擁有可吸納大量溫室氣體的
            雨林,印尼仍是全球第八大溫室氣體排放國。2015年的印尼森林大火,更被認為是21世紀
            最大的環境災難之一。 據《CNN》報導,佐科威在1日的聯合國氣候大會開幕式上,積極
            展示印尼減碳有成。他表示,印尼會用實際作為兌現防止氣候變遷的承諾。他指出,目前
            印尼的森林濫伐率已降至近20年來最低、森林大火發生頻率也在2020年下降至82%,印尼
            政府也預計在 2024 年復育全球最大紅樹林,預計復育600公頃。 然而,環境組織綠色
            和平(Greenpeace)印尼森林倡議家伊克巴爾(M Iqbal Damanik )則向《CNN》表示,
            「科威佐在聯合國氣候大會上說的都是屁話。」 根據綠色和平統計,2012年至2015年間,
            印尼每25秒就失去一個足球場面積的雨林,被用來種植油棕櫚、紙漿林等經濟作物。2020年,
            印尼政府更變本加厲,以振興後疫情經濟為宗旨,推動《創造就業綜合法》(Omnibus Law),
            持續放任企業毀林,森林大火燒不停。 隨著印尼電動車產業興起,常被使用於電池中的鎳,
            也成為印尼近年來積極拓展的領域之一。《路透》報導也指出,新擬定的氣候目標,可能會
            影響印尼雨林區金屬礦藏的開採,這恐怕會為印尼電動車供應鏈帶來不少挑戰。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1636071000
    assert parsed_news.reporter == '陳艾伶'
    assert parsed_news.title == '印尼翻臉不認帳:2030年終結森林濫伐,對我們不公平!'
    assert parsed_news.url_pattern == '4031507'
