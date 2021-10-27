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
    url = r'https://www.cna.com.tw/news/aipl/201911110278.aspx'
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
            屏東基督教醫院透過畢嘉士基金會援助馬拉威醫療12年,馬拉威2008年與台灣斷交,但屏基
            醫護人員沒有間斷對馬拉威的醫療援助,因穩定資金不足,基金會決定發起固定
            捐款募資。 基金會表示,屏基醫護人員透過畢嘉士基金會在馬拉威的醫療援助,包括派
            醫護人員駐守馬拉威進行醫療、訓練馬拉威的醫護人員、教馬拉威民眾養雞、發展
            咖啡產業並在台灣協助銷售咖啡豆、建造學校廁所與濾水器,改善超過5000人的衛生條件、
            提供超過1000片布衛生棉與衛教宣導,讓生理期不再是女性的沉重負擔。 另外,還提供
            獎助學金,幫助超過1000名孩子重返校園,有高達7成為女性;以及透過經濟培力扶持寡婦
            團體,超過60人得以自立養家。 基金會表示,馬拉威今年名列世界10大窮國第4名,以沒有
            內戰國排名,是世界第1窮,馬拉威與台灣曾有長達42年的邦交,在中國大陸的金援利誘下,
            2008年與台灣斷交,而至今仍有超過7成人口生活在貧窮線以下,每天的生活費不到
            新台幣60元。 基金會執行長周文珍表示,馬拉威深受愛滋病、霍亂、虐疾等疾病之害,
            目前除了愛滋病患仍有5000多名外,每年有超過4600名的嬰幼兒及5歲以下兒童,因為腹瀉
            而死亡。 「屏基為何沒有隨著當年斷交全員撤離?」屏基院長余廣亮因長期在馬拉威從事
            醫療服務、開設「彩虹門診」,獲得「醫療奉獻獎」,目前也是基金會董事,他表示,外交
            中斷,但馬拉威人的苦難沒有中斷,「我們放不下這些有需要的人」。 周文珍說,因為
            不曾離開,所以看見改變正在馬拉威不斷發生,但10幾年來的努力,很有可能隨時回到原點,
            目前因為穩定的資金來源不到1/3,各項計畫總得面臨斷炊危機。 畢嘉士基金會決定
            發起募資,以每月固定捐300元,希望號召超過800名捐款者一同加入「馬拉威關懷計畫」,
            基金會表示,如果每年能有穩定的300萬捐款,每年就可服務2800名學童及弱勢族群,改變
            因貧窮失去生命的困境。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1573401600
    assert parsed_news.reporter == '郭芷瑄屏東縣'
    assert parsed_news.title == '援助馬拉威12年 畢嘉士基金會發起募資'
    assert parsed_news.url_pattern == '201911110278'
