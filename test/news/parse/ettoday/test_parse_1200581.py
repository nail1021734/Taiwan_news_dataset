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
    url = r'https://star.ettoday.net/news/1200581'
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
            炎炎夏日,毛孩也需要消暑啊!我們家每天都會開冷氣開電扇,希
            望可以讓狗兒「球球」能比較涼爽點,只是有時看牠還是熱到舌頭歪一邊,還是覺得捨不得,
            想說牠這麼愛玩水,不如帶去體驗一次游泳好了。台北近幾年為了毛孩,其實有不少間寵物
            游泳供奴才考慮,我們上網看了不少資料,在評估過交通、泳池環境、消費方式後,決定去新
            北五股的GoGo Coffee 饗食樂園試試看,沒想到第一次體驗寵物游泳完的感覺還不錯,也提
            供給有在考慮帶毛孩消暑的奴才們考慮囉! 前往泳池的路上都會有路標指示,只要放心跟著
            走就可以抵達了。GoGo Coffee 饗食樂園的停車場是一大片水泥地,只要有空位就可以停,
            同時門口會有服務人員確認入場的人數。樂園的入口共有兩道門,服務人員會先開啟第一道
            門,等客人跟毛小孩都進到中間的空地區,才會再開第二道門進到場內,避免狗狗突然跑到停
            車場發生意外(蠻貼心的設計),而且店家帶客人入座後,還會附上寵物專用的水碗(貼心度再
            ++++)。 樂園大致分為兩個區塊,外部區塊包含寵物泳池、草坪玩耍區及小型生態植物園區
            (規劃中),各區域會定期清潔消毒除蟲,可以放心地和毛小孩一同玩樂;用餐區分為室內及半
            露天區,若選擇室內座位的話,寵物都須包上尿布才能入內(店家會免費提供一個),半露天區
            則沒有這項限制。 一進到樂園的左手邊就是泳池,有緩降坡設計,可以讓毛小孩們安心下水
            ,水深最淺是到成人的小腿、最深會到成人的腰部,如果是第一次游泳的狗狗,可以先到旁邊
            借救生衣,只需要抵押一張證件就可以了。除了狗狗之外,小孩也可以下水,所以家裡有養寵
            物、有小孩的家庭就能一起享樂。 樂園的環境真的不錯,除了乾淨的泳池之外,還有一大片
            的草地可以讓狗狗盡情奔跑,旁邊還有小山丘跟隧道可以讓牠們探險,若是毛小孩們在草地
            上大小便,園區的周圍有提供撿便袋,主人們千萬要自行清理完並丟進專屬的垃圾桶喔!在半
            露天區也有設置兒童遊戲區,如果小朋友不想下水玩耍的話,也可以在遊戲區玩的快樂。 已
            經玩耍完的毛孩,主人可以將他們帶到旁邊的自助沖洗區洗澡,洗澡區有提供稀釋瓶可使用,
            洗毛精等東西要自備(也可以跟櫃台購買),洗完之後可以到身後的自助吹毛區吹乾,一次10
            元、可吹3分鐘,使用的是220V的吹水機及吹風機,風力真的是強強強啊~有下水的奴才若是
            想簡單沖洗換衣服,也有提供3間更衣間,這間樂園真的是把所有你會需要的設施都細心想好
            了! 玩到一半或是玩累了想要補充體力,店家也有提供餐點及寵物鮮食,能選擇的種類蠻多
            的,鹹食、甜食、炸物、點心或飲料類都有,寵物鮮食也有義大利麵或各種肉類餐點可選擇,
            讓狗狗們在玩耍後也能吃東西補充體力,若是想要幫毛孩慶生的話,也可以提前跟店家預定
            客製化的造型蛋糕呢! (小提醒,如果狗狗剛下水完要進入室內的座位區,還是要包上尿布,
            才不會影響到室內的其他客人,露天區則沒有限制。) 我們去的當天,半露天區正好有狗友
            團聚包場,所以來了不少狗狗及主人,有人還是從台南特地上來的!原本也有看到貓奴帶自家
            的貓貓來游泳,只是因為現場大多是狗的關係,貓咪看起來有些緊張,後來就也沒看到他們了
            ,如果有打算要帶寵物來一起享受的主人,建議先評估自家毛小孩的狀況。 如果你最近有在
            考慮要帶家中的毛小孩去消暑的話,不妨可以考慮到新北五股的這間寵物游泳樂園,除了讓
            毛小孩有個盡情玩樂的地方,也許還能認識更多鏟屎官們、一起做個交流!
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530361020
    assert parsed_news.reporter == '安琪'
    assert parsed_news.title == '毛孩夏天也要消暑!讓主子們盡情奔跑、游泳的寵物泳池'
    assert parsed_news.url_pattern == '1200581'
