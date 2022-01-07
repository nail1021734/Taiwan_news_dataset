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
    url = r'https://star.ettoday.net/news/1200510'
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
            忘記是怎麼個因緣巧合追蹤到這家低調的蛋糕店 Cypress & Chestnut,後來才知道他們每
            個月會在臉書專頁上公布下個月的營業日期,透過私訊訂位,然後要等他們排定之後通知,才
            知道自己的訂位是否成功。天啊!我跟本覺得要能夠吃到他們家的蛋糕根本就需要強大的企
            圖心以及好運氣,包括有沒有剛好看到他們在臉書上公布訂位時間的貼文。 吃東西一向隨
            緣的我,就這麼看到他們的貼文了。我查了一下自己的時間,與營業時間比對了一下,依照他
            們的要求給了兩個時段讓他們排時間。接著,訊息就石沈大海,好幾天過去連「已讀」的標
            示都沒有,就在我已經忘記這件事的時候,對方來了訊息約定好
            時間。 Cypress & Chestnut 的位置就在開平餐飲學校附近,之前介紹過的小涼院霜淇淋
            就在他們的斜對面。他們外表低調,看起來像是私人招待所,推開重重的大門進去,便是另一個
            天地。 這家蛋糕店之所以受歡迎的其中一個原因,就是室內裝潢相當適合拍照。有別於這幾年
            流行的工業 loft 裝潢,也沒有日雜繽紛色調,而是素雅潔淨的鄉村風格:白色的背景加上
            大量的卻不死板的乾燥花束。只要隨便一景,就是 IG 打卡美照。 不過我不是網美,也不是個
            喜歡在咖啡館點心店大張旗鼓玩自拍的人,是專程來吃蛋糕的。既來之則大開吃戒!我先點了
            網路上大好評的「伯爵茶栗子蛋糕」,另外也想再點一份栗子小蛋糕。栗子小蛋糕有經典
            原味、黑巧克力、白巧克力三種口味,詢問了服務生,她們說黑白巧克力都會比較甜一點,
            第一次嘗試可以先從原味的開始。我從善如流,點了原味的。 Cypress & Chestnut 的
            伯爵茶栗子蛋糕單片為 180 元。厚厚的鮮奶油看起來驚人,不過因為用的是北海道知名的
            中澤鮮奶油,質地輕盈,越吃越喜歡,一點也不嫌多。伯爵茶海綿蛋糕味道清香,蛋糕體鬆軟
            濕潤,新鮮吃得出來。最令人驚喜的是最下層的栗子奶油,相較起來味道較甜,但也爽口討喜。
            整個蛋糕,不管部分單吃,或者一整個叉子落下一口全部吃進所有味道,都有自己的精彩。偶爾
            覺得想清一下口味,喝一口冷泡金萱,炎夏中的幸福莫過於此。 再來就是栗子小蛋糕。原以為
            吃了伯爵茶栗子蛋糕,再吃栗子小蛋糕會覺得無趣,但沒想到確有不同的驚喜。兩種糕點雖然
            都以栗子為名,但其實栗子只是其中一個重要的元素–畢竟店名 chestnut 就是栗子的一種。
            與伯爵茶栗子蛋糕的濕潤滑順完全不同,栗子小蛋糕的口感香酥,濃郁的蛋奶香,其中偷渡了
            一點栗子。我個人也相當喜歡這道甜點。 意猶未盡之餘,我又跟她們加點了巨峰葡萄
            蛋糕。 只是不知道是伯爵茶栗子蛋糕太出色,抑或我的味覺疲乏,覺得巨峰葡萄沒有前兩者
            那樣精彩。或許是葡萄的與這樣的鮮奶油蛋糕本身就不太合拍?吃起來總覺得不順口。然而我
            肯定店家的用心,她們特地將表面的鮮奶油特地製作成帶著淡淡的葡萄味,工序繁複。 相當
            完美的一次午茶點心。不過若問我是否還願意再去,我的答案是否定的。一來我是個佛系吃客,
            這過程大費周章的預訂對我而言不確定性太高;二來,這樣的蛋糕點心,只用用料實在、配方
            獨到、製作細心,任何店家都是可以做的出來的。若還要再吃,我會想把機會留給其他用心的
            新店家。但無論如何,Cypress & Chestnut 會受年輕女性喜歡不是沒有原因,拍照美、
            東西也有水準之上。
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530255600
    assert parsed_news.reporter is None
    assert parsed_news.title == '預約才吃得到!台北Instagram人氣蛋糕店 清香栗子蛋糕'
    assert parsed_news.url_pattern == '1200510'
