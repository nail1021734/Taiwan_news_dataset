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
    url = r'https://star.ettoday.net/news/1200037'
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
            總統蔡英文29日將出席國防部三軍六校聯合畢業典禮,鄰近的文化國小則為維安問題一度宣
            布停課,引發爭議。北市教育局坦承當時未考慮清楚,昨也緊急決定恢復正常上下課。不過,
            面對抗議團體喊「堵」蔡英文,副市長鄧家基27日上午到文化國小視察,決定是否要架設拒
            馬。 鄧家基表示,市長柯文哲特別交代來看看在局長規畫下,維安上市府能配合的部分,總
            統的安全是最高考量,維安還是要尊重專業,但希望學校活動可照常進行,有關架設拒馬一事
            則稱「會用到最少」,確保民眾能夠正常進出,學童上下課不受影響。 對於外傳將封整條中
            央北路,鄧家基說明,僅會有交通管制,一切依警方規劃,但相關的改道導引上都會非常完善,
            把對市民的影響減到最少。 民進黨執政後推動多項爭議改革,街頭抗議四起。去年蔡英文
            主持三軍六校院聯合畢業典禮,引來大批反年改民眾前往抗議,甚至衝破維安封鎖,擋下總統
            車隊,而今面對蔡英文再次到訪,轄區的北投分區不敢大意,協調鄰近的文化國小29日結業式
            當天停課,遭家長砲轟。 對此,教育局主秘陳素慧回應,因北投分局發函文化國小周邊要交
            通管制,學校回覆之前跟北投分局開會認為會影響學童進出、上課延誤,才討論是否變更結
            業式,教育局長曾燦金、警察局陳嘉昌則在考量後,確定不停課,維持結業式。
            '''
        ),
    )
    assert parsed_news.category == '政治'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530067500
    assert parsed_news.reporter == '皮心瑀,蔣婕妤'
    assert parsed_news.title == '文化國小不停課改設拒馬?鄧家基:會用到最少'
    assert parsed_news.url_pattern == '1200037'
