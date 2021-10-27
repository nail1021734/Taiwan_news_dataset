import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/12/19/a633525.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            各位觀眾朋友,您好!歡迎您收看「社區廣角鏡」。 過節期間,給親朋好友準備禮物總是
            必不可少的,不過花錢的同時,也提醒您注意理財。今天節目的一開始,我們就請專家來
            聊一聊年底理財規劃;然後來聽聽派特•布朗的故事,這位已故的加州州長對加州有著深遠
            影響;台灣清華大學的學生們,在一項世界級的電腦競賽中,獲得第一;計劃去台灣旅遊的
            朋友,我們要向您介紹國際級飯店,屏東的玫瑰溫泉和大閘蟹,還有臺南的烏魚子。 聖誕、
            新年、中國新年,接下來兩個月,您都安排好怎樣過節了麼?那麼同時,您安排好節日的財務
            規劃了麼?在加拿大如何做好年底的理財規劃,來聽聽專家的意見。 湯先生做投資理財已經
            有十多年,每年的這個時候他都會給客戶提供一個理財清單,提醒他們在忙著過節的時候,
            不要忘記理財。 首先,在年底之前向下面的幾個賬戶存錢。 TFSA免稅儲蓄賬戶,每年有
            5000塊的儲蓄上限,這些錢可以免稅。 RESP給孩子的高等教育儲蓄的賬戶,在年底之前存錢,
            政府會按照您存入的錢給20%的補助。 RRSP退休儲蓄賬戶,雖然截止日期在明年2月底3月初,
            但是也要提前計劃,不要等到節日過去之後發現錢已經花完了。 但是在使用TFSA免稅儲蓄
            賬戶的時候要避免進入誤區。 Edward Jones理財顧問湯遠智:假定今年1月3號您放了
            五千塊進去(TFSA),3月3日拿了兩千塊出來,有些人不知道,以為拿出來之後還可以放回去,
            就又把錢放回去,可是今年五千塊的額度已經放滿了,您今年不能再放回去了。您今年領出來
            的錢,要過了一年,到第二年的1月1日之後,才可以跟第二年的額度一起放回去。 所以如果在
            同一年把兩千塊重新放回賬戶,就會被罰款,超出五千塊之後的額度,每個月要交1%,也就是
            20元的罰金。不過反過來說,如果在年底把錢從免稅儲蓄賬戶中拿出,這部分錢不用繳稅,
            同時又增加了明年賬戶的免稅額度。 Edward Jones理財顧問 湯遠智:另外兩個是華人
            朋友們比較少接觸,但是事實上很重要的,一個是捐錢,因為加拿大政府很鼓勵大家在自己的
            能力範圍內這樣做,想要得到退稅,就要在年底12月31日之前做(捐款)。 還要提醒投資股票
            或債券的觀眾們。 Edward Jones 理財顧問 湯遠智:如果在年底之前已經賣出一些基金、
            股票、公債或者其他的投資,是要上稅的,那麼在年底之前可以重新看一下戶頭裡面還有哪些
            是可能有賠錢的,在年底之前做一些節稅的處理,不然可能今年就要交不少的稅。 最後,在
            年底還要回顧一下過去一年的投資情況,調整下一年的投資計劃。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1324224000
    assert parsed_news.reporter == '史青多倫多'
    assert parsed_news.title == '過節不忘理財 加國年底理財清單'
    assert parsed_news.url_pattern == '2011-12-19-633525'
