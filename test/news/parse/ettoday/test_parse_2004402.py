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
    url = r'https://star.ettoday.net/news/2004402'
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
            日本女星大久保麻梨子於2016年與台灣老公Jerry(盧德張)結婚,成為台灣媳婦的她,
            因為新冠肺炎疫情影響,已經一年半沒有回家鄉日本了,現在都只能透過和媽媽視訊一解思念
            。 近期新冠肺炎疫情升溫,12日將迎來端午連假,也讓人擔憂再度造成群聚感染,
            大久保麻梨子就表示非常感謝決定不返鄉的民眾們,「謝謝你們選擇待在家一起繼續對抗
            疫情,保護自己保護別人。」 而因為新冠肺炎影響,大久保麻梨子透露自己已經長達一年半
            沒有回家鄉日本,她只能透過電話視訊傳達對家人好友的關心,她也分享和媽媽的視訊畫面,
            只見母女兩人笑得開懷,她開心地表示:「媽媽的笑容笑聲總讓我有回家的感覺,雖然不能
            擁抱她,但大家都能健康平安就是最大的幸福。」 端午節決定不返鄉的朋友們, 謝謝你們
            選擇待在家一起繼續對抗疫情, 保護自己保護別人。 電話視訊也能表達對家人親朋好友的
            關心與愛。 我已經1年半沒辦法返鄉了。 不過不管視訊通話,媽媽的笑容笑聲總讓我回家的
            感覺。 雖然不能擁抱她,但大家都能健康平安就是最大的幸福。 先照顧自己好好生活,
            一起等待能安心回家的那天吧。
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1623375180
    assert parsed_news.reporter == '許皓婷'
    assert parsed_news.title == '大久保麻梨子1年半沒回日本!嘆想抱媽媽:等待能回家那天'
    assert parsed_news.url_pattern == '2004402'
