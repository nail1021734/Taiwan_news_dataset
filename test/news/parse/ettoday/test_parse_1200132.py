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
    url = r'https://star.ettoday.net/news/1200132'
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
            從小我就非常有長輩緣,好處就是人生路上總會有人搶著當乾爸乾媽,一路也有許多貴人提
            攜。後來我發現,把應對長輩的技巧用於面對婚姻裡的公婆也是非常受用。如果妳已經有確
            切的對象,可以參考看看,如果妳還是單身,也可以應用某些技巧在妳生活和職場上的長輩及
            長官喔! 1.孝順就要「順從」: 沒有長輩會喜歡晚輩忤逆他的,就算長輩沒有倚老賣老,但
            我也會盡量尊重他的觀念和意見。畢竟長輩都習慣仰賴他累積多年的人生經驗,說話的時候
            我們可學習先附和對方的看法,然後再委婉提出自己的見解。例如我會說:「媽,我也有聽說
            過,這方式真的不錯。但我們現在還有其他的作法,妳要不要聽聽看?」。而不是直接回嗆:
            「哪有?!妳這個方法落伍了啦!」 2.嘴甜總是惹人愛: 嘴甜並不是刻意討好拍馬屁喔!
            拍馬屁這件事我還真做不來。我覺得對長輩很有用的嘴甜技巧說穿了其實是基本禮貌,小時候
            家長就會教我們看到長輩要問好,叔叔阿姨好,但結了婚看到公婆妳會忘記喊聲爸、媽?公司裡
            的長官也是一樣,茶水間遇到點頭微笑打聲招呼都是基本禮貌啊!見面打招呼之外,「吃飽了嗎」
            「天冷了穿暖一點」這些常見的關懷,長輩都會很喜歡的。 3.時時保持感恩的心: 為何要
            把公婆當作敵人呢?雖然我有時候也會因為長輩的碎念而煩躁,但我總會記得把自己的小姐脾氣
            收起來,同時提醒自己,沒有公婆我就沒有老公,無論如何我都要感謝他們生育教養了一個好
            男人。除非妳不愛妳的伴侶那另當別論,但如果妳愛妳的伴侶,應該對所有成就了他的人(父
            母、師長、老闆等)保持感恩,然後妳會發現出自內心的感謝會讓妳跟他們自然維持良好的
            互動。 4.禮多人不怪很暖心: 很多長輩都會說你別破費送我東西,但這種話我通常聽聽而
            已。只要是去別人家裡,或是平時受到關照,有機會我就會準備禮物回饋。每次去外地旅遊
            一定會買伴手禮回家,養成禮多人不怪的好習慣。例如婆家都是兒子沒有女兒,身為媳婦的我
            就非常好發揮,我會送口紅、香水、帽子、衣服這些兒子不太會為媽媽選購的東西,婆婆就會覺
            得我很貼心。 5.善意謊言有其必要: 婚姻生活是很需要善意謊言的,可以省卻許多衝突和
            麻煩。不怕神一般的對手,只怕豬一樣的隊友。善意謊言需要伴侶和妳有共識,能夠互相掩護。
            例如有時候婆婆會一直叫我回家吃飯,但那天我就想要在外約會吃大餐,這時就會派伴侶去溝通
            。有些時候我們會對好台詞,再決定怎麼跟長輩說。我有一些社交活動甚至要離家幾天的,
            老公也會掩護我跟公婆說我被公司派去出差。 最重要的是,對於長輩要有體貼的心,例如他
            們可能對於新科技不是很了解,或者行動比較緩慢,視力比較差,很需要我們協助的時候,就
            要多一點耐心。每個人都會老,當妳試圖理解長輩們,尊敬他們,才能增進彼此的關係喔!
            '''
        ),
    )
    assert parsed_news.category == '健康'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530275460
    assert parsed_news.reporter == '艾姬'
    assert parsed_news.title == '公婆、上司超難搞? 「5招」輕鬆搞定...問吃飽了嗎絕對中'
    assert parsed_news.url_pattern == '1200132'
