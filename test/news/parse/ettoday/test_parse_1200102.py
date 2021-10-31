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
    url = r'https://star.ettoday.net/news/1200102'
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
            住在美國加州的古茲曼(Esteban Guzman)是墨西哥裔,他和媽媽住在一起,有一天兩人正在
            自家花園整理的時候,突然有一名白人婦女闖進他們家中,完全沒來由就對著他們破口大罵,
            並且用「強暴犯」、「禽獸」等字眼形容墨西哥人。影片被PO在網路上後引起廣大
            討論。 27歲的古茲曼住在加州聖博納迪諾郡(San Bernardino County),一名白人婦女
            直接闖進他的家裡,伸出手指指著他的鼻子大罵。在這支網路瘋傳的影片中,古茲曼問,
            「你為什麼恨我們?」,婦女回答「因為你們是墨西哥人」,他回覆,「可是我們是老實人」,
            這名婦女接著笑說,「沒錯,你們是強暴犯(rapists)、禽獸(animals)跟毒販
            (Drug dealers)」。 古茲曼覺得很無辜,他說道,「我強暴過幾個人,我有賣毒品嗎?」,
            穿著綠色衣服的白人婦女則說,「連美國的總統都說你們是強暴犯」,甚至還比出中指。古茲曼
            上節目時提到,他禮拜一到五在IT產業上班,假日則回家到附近的工地繼續工作,「我們是在
            這裡認真工作的人」,當時他就是跟媽媽一起在協助整理客戶的房子。 他提到,當時先看到
            這名白人婦女在對著他媽媽大喊「滾回墨西哥」,接著才發生口角,對方說他們母子都是非法
            移民,「事實上,我們都是美國公民,我在加州土生土長」。他的母親教導他要成為有禮貌、
            誠實並尊重別人的人,平常偶爾也會收到種族歧視的批評,他都可以不在意,但如果是侮辱媽媽
            的話就不行,「我們並不是總統說的任何一種樣子,希望她不要相信電視上所看到的
            一切」。 美國總統川普上任之後,有關種族之間的問題就沒有停過,多家外媒指出,這名白人
            女子所用的詞彙,的確都是川普曾用來形容墨西哥或其他國家移民的,該女也明確提到總統,
            顯示是受到川普的影響。 古茲曼也在臉書上諷刺說道,感謝美國總統,現在我到哪裡都是
            性侵犯、禽獸或毒販,「你不懂被恨成這樣是什麼感覺,請大家幫忙,我們必須要一起停止種族歧視」。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530084480
    assert parsed_news.reporter == '錢玉紘'
    assert parsed_news.title == '「強暴犯加禽獸!」大媽伸中指飆罵墨西哥男 超嗆影片曝光'
    assert parsed_news.url_pattern == '1200102'
