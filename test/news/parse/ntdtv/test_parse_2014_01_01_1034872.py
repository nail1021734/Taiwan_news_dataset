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
    url = r'https://www.ntdtv.com/b5/2014/01/01/a1034872.html'
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
            2013年12月初,全球五大洲、53個國家和地區,近150萬人聯署簽名,呼籲制止中共政權
            活摘法輪功學員器官。請願信已遞交聯合國。日前《新唐人》獲得消息,反對活摘的簽名
            也在大陸擴展。河北唐山,秦皇島,張家口和天津的民眾,反對活摘器官的簽名,在不到半個月
            的時間,已經有6259人。這還是大陸第二次徵簽的結果。 第一次簽名發生在12月中旬,當時
            中國大陸民眾開始了解這一令人難以置信的罪行,有300多人簽名。他們要求調查倒台的
            中共官員薄熙來和周永康參與活摘法輪功學員器官的罪行。 大陸技術工人范先生:「反對
            活摘器官,這是一個人正常思維的一種表現,如果說納粹是個很恐怖的事情,活摘法輪功學員
            器官,要比納粹高於10倍、100倍的恐怖。」 目前大陸絕大部分民眾,還沒有得到參與簽名
            的機會,能突破網絡封鎖的民眾,紛紛在《新唐人》網站留言,建議建立徵簽網站,給他們簽名
            的機會。 網友張三寫道:「我也要簽,可是不知道在哪裡簽,如果有個網址或郵箱
            就好了。」 還有網友非常著急,疾呼:「簽名網站在哪裡?我要
            簽名! ! ! ! ! ! ! !」 網友李雪青寫道:「在此,我鄭重借《新唐人》一角簽名
            聲援反活摘:李雪青。願早日清算罪惡,讓國人走向光明!」 不具名的網友說:國外的那次
            簽名我參加了,國內的渠道在哪裡? 紐約中國問題研究人士張健:「在法輪功長年在中國遭受
            非人的待遇,人類有史以來最嚴重的罪行發生在他們身上的時刻,在中國如此殘酷的
            環境下,還是有很多的有良知的中國人,為這些人去吶喊,,這些人就像星星之火一樣,它一定
            可以燎原,會讓血債幫血債血償。」 2006年3月,遼寧省三位證人,先後指證活摘法輪功學員
            器官大量存在中國,其中證人的家屬就是活摘法輪功學員器官的主刀醫生。 隨後的
            7月,加拿大著名人權律師大衛•麥塔斯(David Matas),和加拿大前國會議員
            前亞太司司長大衛 ̇喬高(David Kilgour),公佈了第一份調查報告,他們用52種
            證據,證實了中共活摘法輪功學員器官的罪行真實存在。數年來他們一直在調查取證,
            《血腥的活摘器官》一書在全世界發行時,引起轟動。 第二個獨立調查,由前美國智庫研究員
            伊森•葛特曼啟動,他的結論是,到2008年,最少有65000名法輪功學員被摘取器官
            致死。2012年7月《國家掠奪器官》發行,這本書匯集了7個國家的專家分析與證人的
            證詞。 2012年薄熙來倒台後,薄熙來等人活摘法輪功學員器官,並販賣屍體牟利的
            黑幕,進一步被披露。 其實早在2000年,海外《明慧網》就曝光過大陸「活摘器官」的
            罪惡,但由於邪惡的程度超出人類的想像力,當時沒有多少人願意相信。 范先生:「法輪功
            學員,如果他是一個不願意把自己的身份暴露,怕影響家庭,受他的牽連,他不報姓名,給他
            活摘器官,這都很正常,也不知道哪裡的,只有你想像不到的,沒有共產黨幹不到的。」 1999
            年中共迫害法輪功以來,中國人體器官移植呈直線上升,1994年至1999年,中國只有約18500
            個器官移植案例。而2000年至2005 年,上升到60000例。2006年,隨著「活摘器官」在
            國際社會大量曝光,大陸器官移植數量也直線下降。 隨後,中國不時爆出病人器官被盜取的
            驚人消息,甚至連韓國遊客在中國旅遊時,也在醫院丟失器官。 近年來,全球政府組織和
            非政府機構,都在呼籲調查「中共活摘器官」罪行。前不久,歐洲議會投票通過緊急
            議案,要求「中共立即停止活體摘取良心犯、以及宗教信仰和少數族裔團體器官的行為」。
            歐洲議會代表5億歐洲民眾發聲。
            '''
        ),
    )
    assert parsed_news.category == '法輪功,法輪功人權'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388505600
    assert parsed_news.reporter is None
    assert parsed_news.title == '大陸6259人簽名 反中共「活摘器官」'
    assert parsed_news.url_pattern == '2014-01-01-1034872'
