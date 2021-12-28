import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/19/10/21/n11602441.htm'
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

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            由於對「申請助學金」存在誤區,每年有數百萬的家庭沒有提交申請,或本應該獲得助學金的
            家庭,卻沒有拿到助學金。當家庭收入、資產、人口結構發生了變化,對申請助學金有影響嗎?
            如何應對?曾是全美500强,硅谷軟件公司總監的理財專家Guno,擅長大學財務規劃,幫助許多
            家庭輕鬆拿到了大學的學費補助。 從五百強公司總監,到硅谷理財專家 Guno曾任全美500强
            硅谷軟件公司總監,後自創移動軟件公司,2015年被成功收購。高度的前瞻性、自信心以及
            嚴謹的邏輯分析,Guno不僅始終站在硅谷科技創新的前沿,也在理財界中獨擁一片藍天,尤其
            在大學財務規劃方面別具一格。 Guno的親戚,最早在灣區引進知名升學輔導機構「Elite
            教育」。Elite每年都有兩千人左右的家長年會,指導學生怎麼報考醫生、律師、理工等學科
            。去年Guno首次在Elite年會期間舉辦了針對學生家長的講座「大學財務規劃」,連續2場,
            300多人座無虛席。講座結束後不少家長找到Guno,最後都如願以償地拿到了理想的大學
            助學金。 硅谷理財Guno談「申請助學金三大誤區」 助學金(Grants or Assistant
            ship)是由美國各機構資助學生,無需償還的。Guno多年幫助家長申請助學金,發現他們有
            3大誤區: 申請助學金誤區一、助學金是給低收入家庭的。很多家長聽說:只有家庭年收入
            低於5萬美金的家庭,才能申請到聯邦政府的補助。每一年有上百萬這樣的家庭,沒有提交
            助學金申請,錯過拿助學金的機會。 申請助學金誤區二、高收入拿不到助學金。許多家長受
            同事、朋友誤導,認為家庭年收入超過20萬,不可能獲得助學金。其實通過合理的財務規劃,
            高收入家庭也可以拿到助學金。 申請助學金誤區三、孩子自己填寫申請表。有許多華人父母
            英文不好,孩子自己填寫申請表。孩子會問父母家裡的資產,比如我們家房子價值多少?父母說
            ,150萬。好,這一年的助學金可能就拿不到了。Guno提醒家長:當孩子問到家庭財政情況時,
            父母一定要請教專業人士,不能怕麻煩,否則數千美金的助學金可能就泡湯了。 股票多賺4萬
            ,助學金少拿1.8萬 硅谷某工程師的孩子是12年級,今年申報,下一年入學。他聽完Guno的
            講座後,把家裡的稅單給Guno看,本來他家可以拿到2萬助學金,(按照EFC規定)他們需要交的
            學費只有1萬~1.3萬。但是今年,他要交學費3萬~3.5萬,因為他上一年賣股票,賺了4萬多。
            這樣,他孩子的助學金就少拿了1.8萬左右。 他來的太晚了,Guno說:「你如果提早一年找到
            我,我及時告訴你賣股票,你可能當時少賺一點,但是助學金卻不會損失。」好在,他的孩子是
            四年大學,Guno第一年幫不上忙,如果做好以後的三年財務規劃,就能幫他在第三年、第四年
            節省升學費用。 年收入增加$4,000,助學金可能損失一萬多 硅谷另一客戶雖然有兩套房子,
            可是他的家庭年收入AGI為4.6萬,學校應該給全額助學金的。按照加州條例,年收入4.8萬
            不用申報資產。後來,他高興地告訴Guno:我下一年收入要漲到5萬多啦! Guno對他笑了笑說
            :你家收入多$4,000,但你一年就會損失一萬多助學金。現在還來得及,只要把家庭收入降
            下來,我還能幫你申請到全額獎學金。 生意緩售,節省近2萬升學費 有一位客人的年收入是
            五萬左右,他的孩子2021年要上大學。申報助學金是按照孩子上大學前兩年的稅表來看。今年
            他有幾筆生意要出售,向Guno諮詢。Guno告訴他:生意如果虧錢,就趕快賣。他回說是賺錢的
            。Guno問他:你可以暫時不賣嗎?或者分幾次慢慢地賣嗎?客人回答可以。 這樣,Guno幫他
            申請到助學金,他一下子省了1萬多升學費。如果這位客人再早一年找到Guno,那就更省事,
            如果在2018年把生意都賣了,對現在沒有任何影響。如果再早4~5年或者10年,Guno可以為
            他做更好的升學財務計劃,節省更多費用。 自己填錯表,助學金少拿3萬 填寫助學金申請表
            不是一件簡單的事情,不僅要有會計知識,還要熟悉教育部的規定。Guno兩年前在紐約辦
            培訓班,免費教華人填寫助學金申請表。一個人聽完課,自己回家填好申請表交上去了,結果
            收到學校的反饋與Guno說的結果不一樣。 Guno拿過他的填表一看,發現他把自己的資產和
            收入放在孩子那一欄,寫錯位置了,結果少拿一萬多助學金。 與此相反,Guno在硅谷免費教
            另外一個人如何填表,填對了就能省3萬。那人不放心,寧願花錢請Guno做,結果他家穩穩當
            當地拿到了3萬助學金,還省心省力。他懂得專家的價值。 與單親媽媽的前夫溝通,獲取
            助學金 為了幫助單親媽媽們順利拿到助學金,Guno還要跟她們的前夫約談,談財產、錢的
            分配、529教育儲備基金何時支付?是不是用贍養費來買保險?因為孩子到了18歲,就領不到
            生活費(贍養費)了。孩子沒獨立的時候,有什麼事情可以用保險來處理;如果助學金不夠,就從
            人壽保險中拿出現金值(免稅的)來給孩子上大學。何樂而不為呢? 有不少單親媽媽,因老公
            沒留下什麼財產給她們,生活艱難。單親媽媽想工作,又要帶孩子,在時間上處於兩難之間。
            她們在與Guno打交道的過程中,既對他的理財產品有所了解,又看到他熱情、正直、善良的
            人品,不知不覺中成了Guno的助手,在家上網就可以工作,還能照顧孩子。 Guno服務理念:
            不求一時回報 Guno能歌善舞,在「選美會」等大型公共活動中廣結名士,對於陌生人也常常
            仗義相助,義務幫人買房子、找律師等等,解決燃眉之急。他知識廣博,朋友們稱他為「活字典
            」,時常問他一些時興的概念,比如怎麼經營比特幣呀,什麼是高科技模擬合成空間呀等等,他
            有問必答。 有一次,一個西雅圖的陌生華人在社交媒體問:在哪買奶粉送中國便宜?五分鐘
            之內,Guno在自己的社交圈裡了解到5家西雅圖快遞公司,送貨到中國的運費價格最具競爭力,
            並把他們的聯繫方式給了他,那華人連連道謝。 兩年前,Guno在紐約碰到一個新移民,熱心地
            介紹給她一些很好的商機,她非常感激,可是她英文不夠好,沒把握住機會。一個月前她結婚了
            ,找Guno幫她先生買保險。Guno給了她一點點幫助,都兩年了她還裝在心裡。Guno認為:宇宙
            是圓的,循環的,暫時沒得到回報,沒關係,不看重一時之利。 硅谷有許多做名校升學計畫的人
            ,都找Guno做財務規劃。Guno發現一些年薪二十多萬的工程師,為孩子拿不到助學金而沮喪。
            Guno經常對他們說:不用難過呀,收入高,恭喜你啊!關鍵是你的錢有沒有管理好?孩子升學前
            2年是痛點,做好財務規劃能拿到理想的助學金;如果早在上大學前10年就做規劃,不僅能節省
            可觀的升學費用,還能節稅、永續收入呢! 每年的十月、十一月份是申請助學金的最佳時機。
            如果你還沒有做過這類申請,或者曾經申請沒有被批准的,請聯繫硅谷理財專家Guno,您會有
            意想不到的收穫。如果您是Guno的理財客人,他的團隊會免費幫您填寫申請表。 硅谷理財
            Guno的聯繫方式 精通粵語、國語、英語。
            '''
        ),
    )
    assert parsed_news.category == '美國,舊金山,生活嚮導,投資理財'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1571587200
    assert parsed_news.reporter == '余亨之'
    assert parsed_news.title == '硅谷理財Guno:助您順利拿到「助學金」'
    assert parsed_news.url_pattern == '19-10-21-11602441'