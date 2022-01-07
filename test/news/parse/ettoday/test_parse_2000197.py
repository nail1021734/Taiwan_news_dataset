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
    url = r'https://star.ettoday.net/news/2000197'
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
            新冠肺炎疫情嚴峻,除了戴好口罩之外,保持社交距離之外,現在還可以多使用漱口水,高雄市
            吉田耳鼻喉科診所醫師曾哲凰就指出,今年5月22日出刊的
            《European Archives of Oto-Rhino-Laryngology》當中,有一篇針對漱口水跟
            新冠病毒之間的抗發炎效果和臨床試驗研究裡頭提到,漱口水可以降低咽喉中的病毒量高達
            9成,呼籲大家可以多使用漱口水
            。 《European Archives of Oto-Rhino-Laryngology》(歐洲耳鼻喉期刊)在
            5月22日出刊的內容當中,其中有一篇研究
            《漱口水對於新冠肺炎病毒的抗發炎效果和臨床實驗研究》提到,他們以34位新冠肺炎患者為
            對象,患者用漱口水來漱口1分鐘之後,可將咽喉部的病毒載量降低約90%。 研究中以漱口後
            的初期、2 小時、4 小時和 6 小時等時間點,分別對 5 名患者的病毒載量進行了採樣,
            發現病毒的數量得需要大約 6 小時才能恢復到初始病毒載量。另外也有發現高傳染性患者在
            6個小時左右能夠恢復病毒量,而傳染性較低的患者在漱口後 6 小時無法恢復最初的傳染性
            。所以研究認為漱口水特別是對於初始 Ct 值在25到30的患者,用漱口液治療在減少
            新冠肺炎傳播方面最有效。這也就是說是在「無症狀感染期」或是「感染初期」的時候是
            有用的。 曾哲凰醫師強調,病毒多是由口、鼻,經過喉嚨,進入體內,透過漱口水來漱喉嚨,
            是一個還不錯的保護自己的動作,是可以適當減少病毒量,建議民眾在疫情期間如果有
            固定漱口,降低病毒量也會降低感染別人的機率,保護家人和周邊的人,如果更多人增加
            固定漱口的習慣,應會有利於整體社區對疫情的控制。 另外,高雄市耳鼻喉科診所醫師張
            簡培崙也表示看過這篇研究,不過這篇研究裡頭說的「漱口水」,並非是單純的水,
            但他也指出,反正多使用漱口水,有好沒有壞,其實也可以多做,另外個人基本防疫動作像是,
            多戴口罩、勤洗手、保持社交距離之外,也千萬別少。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1622945640
    assert parsed_news.reporter == '吳奕靖'
    assert parsed_news.title == '個人防疫可多做這件事!歐洲研究:新冠患者用漱口水可降9成病毒量'
    assert parsed_news.url_pattern == '2000197'
