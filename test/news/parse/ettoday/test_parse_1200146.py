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
    url = r'https://star.ettoday.net/news/1200146'
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
            「日系」總是令人聯想到溫柔、精緻的療癒氛圍,我們特別整理了八位日本人氣Instagramer
            名單,從彩妝、髮型、保養到美甲,帶你掌握日本最新流行訊息。別忘了將最得你心的帳號
            納入追蹤清單! 大地色系裸妝教學:石田一帆 石田一帆為日本小有名氣的部落客,她的妝容
            教學影片以裸色系、大地色系為主,散發了日本女性流行的「大人っぽい」風格,同時,也時
            常示範時下流行的土色系彩妝。 除了彩妝品以外,也可以從石田一帆的IG牆上看到臉部及頭髮
            保養品的推薦,欣賞這些療癒美妝品之餘,也可以從她的教學影片中知道許多好用的商品
            資訊。 石田一帆會把眼妝、頰彩、打亮、唇妝拍成一個簡單的小短片,並在文中標記自己使用
            到的產品,這些產品有些是最新推出的,有些則是石田一帆的愛用彩妝。 濱田あおい是一名
            來自東京的女孩,除了IG之外還擁有自己的Youtube頻道,在Instagram上可以看到她的妝容
            分享以及妝容教學小短片,貼文裡也都會貼心地標記每個妝容使用到的產品。 此外,在她的
            Youtube頻道中,有一系列的「牙齒矯正」經驗Q&A,經驗分享都很真實十分具有參考
            價值。 濱田あおい常常會分享最新上市的日本藥妝,Instagram更新的資訊很迅速,若是喜歡
            日本美妝資訊的人,絕對可以從她的IG中得到第一手情報。 濱田あおい的妝容走的是日系
            粉嫩的甜美風格,「底妝清透、眼妝自然、臉頰紅潤、唇妝粉嫩」宛如日劇女主角的必備
            日常妝。 Ayana為日本公司modelate旗下的模特兒,除了工作性質相關外,Ayana對於美妝
            十分感興趣因此研究了許多彩妝技巧。 Ayana的彩妝風格也是走粉嫩色系的,但與前面介紹的
            濱田あおい不太一樣的是Ayana在甜美中又帶著成熟的女人味,整體而言,很適合上班族女性
            模仿學習。 Ayana的教學影片比較特別的是她除了影像的呈現外還會放上字幕,這讓追蹤她的
            人不只能知道她使用什麼產品,也可以更清楚妝容的細節與進行的技巧,讓想模仿的追蹤者的
            完整度能更高。 田中亞希子以編髮為主題,出現在許多日本雜誌的專欄中,之前還出書,在日本
            大受好評。 她染著一頭透明感的霧感灰咖色,柔順的髮絲永遠頂著天使光圈,對於頭髮的照顧她
            十分有心得,每一款編髮都彷彿是日本漫畫中的造型,讓人看了想馬上跟著田中亞希子
            學習。 田中亞希子的Instagram上有許多簡易編髮教學的小短片,教學短片中步驟簡短、
            不複雜,對於編髮初學者來說,成功的機率滿大的。此外,田中亞希子偶爾也會把日雜刊載的
            髮型專欄分享到Instagram上,讓追蹤者能透過影片以外的方式學習日系編髮。 忍舞出生在
            日本宮崎,曾擔任過資生堂旗下的專科網路模特,一頭有個性的清爽短髮與和風五官讓她深受
            歡迎,熱愛美妝與時尚的她,時不時會在自己的Instagram上分享好用的彩妝、保養品與
            指彩。 由於本身工作性質的關係,忍舞掌握的美妝消息永遠是最前線的,想要一窺日本模特兒
            的愛用品清單嗎?趕緊按下追蹤鍵吧! 看著手上的電棒總是不知道要如何捲出日系的空氣感
            捲髮嗎?讓日本專業髮型師教你其中的訣竅吧! miyuwada從編髮、婚禮髮型到日常造型
            都十分拿手,彷彿外國人自然捲的電棒造型深受日本女性喜愛,在Instagram上和田美由紀常
            會分享教學影片及成品照,想學習日系捲度的人可以到她的Instagram上一探究竟。 利用人
            手一支的平板夾,和田美由紀就創造出了自然的捲度,實用之餘,難易度也不大。除此之外,
            miyuwada也是個熱愛美妝的人,髮型教學之餘,也會po出一些愛用的彩妝品分享給
            大家。 一進入Akina的Instagram就會馬上被她精緻的眼妝所吸引,「茶色系、光澤感、
            根根分明的睫毛」,Akina的每一張照片都散發著高尚的氣質。對於美妝的熱愛使Akina
            考取了日本化妝品檢定2級,讓她的分享文更有專業依據性。 Akina也不藏私的分享愛
            用的眼彩,雖然眼部彩妝的貼文佔多數,但Akina偶爾也會放一些推薦的頰彩與唇彩照片到IG
            牆上,讓追蹤者看完這些貼文後都好想購入她的彩妝清單。 據
            傳是日本女星堀北真希的妹妹──原奈奈美,她在美容沙容擔任美睫師,同時還身兼髮型模特
            兒,熱愛時尚的她,也時常會在社群上分享美甲成品照。 喜歡日系風格的女孩,可以到原奈
            奈美的IG牆尋找從髮型、美睫到美甲的成品照做參考。
            '''
        ),
    )
    assert parsed_news.category == 'fashion'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530163860
    assert parsed_news.reporter is None
    assert parsed_news.title == '8位必追蹤的日本Instagramer!第一手知道日系流行妝髮'
    assert parsed_news.url_pattern == '1200146'
