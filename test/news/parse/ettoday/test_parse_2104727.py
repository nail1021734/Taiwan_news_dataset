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
    url = r'https://star.ettoday.net/news/2104727'
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
            竹市海山漁港作為台灣最具特色的定置網漁業基地,將舉辦食魚教育以及周邊景點小旅行活動
            ,分為「一日網美養成」、「生態知性導覽」、「生態知性導覽+環保DIY」3大路線,帶領
            大小朋友認識新竹在地當季魚獲,並帶大家體驗濕地生態環境與淨灘活動,活動自10月20日
            下午6時起開放報名,額滿為止,另外還可向業者報名出海深度體驗。新竹市長林智堅邀請
            大小朋友到訪旅遊,表示海山漁港緊鄰香山濕地,擁有特殊濕地的生態資源、沿岸蚵田及
            美麗夕陽海景,是兼具漁業與遊憩功能、適合全家出遊的好地方,透過導覽及闖關活動,提升
            民眾環保意識,更深入了解這塊寶地。 林智堅表示,海山漁港是新竹市唯二漁港,也是台灣
            最具特色的定置網漁業基地,具備漁業與遊憩多功能,漁港旁2家業者「明發定置網」與
            「金吉利定置網」在海面上定置網漁場中捕獲的新鮮漁獲,每日現撈漁獲往往一上岸就被
            搶購一空,遊客千萬別錯過「現撈仔」機會,誠摯邀請大朋友帶著小朋友前往旅遊,認識新竹
            海山漁港及自然生態。 「海山食魚定置網小旅行」時間為10月30、31日,11月6、7日
            一共4天,每天2梯次共8個梯次,活動採預約制,每梯次開放30人報名參加,每次搭配漁港
            旁明發定置網進行導覽,以及不同的闖關活動,分為3大路線: 路線一、「一日網美養成」
            (上午9:10-12:30)共計4梯次:香山火車站集合、海山漁港〈網美實習生-打卡美美照教學〉
            、香山濕地〈一日攝影師-最美的風景〉、明發定置漁場〈導覽活動-漁場大揭密〉。 路線
            二、「生態知性導覽」(下午13:40-16:30)共計3梯次:香山火車站集合、海山漁港
            〈專業導覽-海山印記〉、香山濕地〈環保小尖兵-淨灘活動〉、明發定置漁場
            〈導覽活動-漁場大揭密〉。 路線三、「生態知性導覽+環保DIY」(下午13:40-17:00)
            僅限1梯次:香山火車站集合、海山漁港〈專業導覽-海山印記〉、香山濕地
            〈環保小尖兵-淨灘活動〉、明發定置漁場〈導覽活動-漁場大揭密〉、生態體驗環保DIY
            。 產發處指出,歡迎大小朋友參加報名「海山食魚定置網小旅行」活動,完成任務還可
            獲得精美紀念品,活動詳細資訊及報名網址,或可撥打(03)-5244453#12。 產業發展處
            處長張力可補充說明,定置網漁業是在沿岸海域架設漁網,形成陷阱的捕魚方法,利用錨或
            石塊等固定繩索張開網具,魚被攔路漁網阻隔並順著方向進入網內,定置網漁場依潮汐收魚
            、捕捉野生活魚,當日直送漁港銷售,讓民眾買到尚青的當季海魚。 此外,市府也輔導業者
            兼營娛樂漁業,搭配海上與食漁教育遊程來推廣漁業觀光,目前明發定置網已有兼營娛樂
            漁船執照,一次最多可載客22位遊客出海參觀,想進行深度體驗定置網漁業旅客,可向
            明發定置網租用搭乘娛樂漁船出海到漁場,實地觀看定置網作業方式,明發定置網
            聯繫方式(0937-171-656)。
            '''
        ),
    )
    assert parsed_news.category == '地方'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634626080
    assert parsed_news.reporter == '蔡文綺'
    assert parsed_news.title == '新竹海山漁港小旅行 3大路線10/20起開放報名'
    assert parsed_news.url_pattern == '2104727'
