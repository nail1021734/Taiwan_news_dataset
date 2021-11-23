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
    url = r'https://www.epochtimes.com/b5/19/5/3/n11232059.htm'
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
            2019年4月30日晚,舊金山灣區佛利蒙市(Fremont)的法輪功學員在中央圖書館舉辦免費
            教功班。當天的活動,吸引了包括來自中國大陸、歐美、越南、伊朗、印度在內的不同族裔的
            人士。 明慧網報導,很多人學功後表示,感到身心放鬆,精力充沛,非常喜歡,將會繼續學煉
            下去。 大陸移民:很早就想學了 「我很早就想學法輪功了。我知道煉法輪功肯定會身體好。
            」來自廣東的司徒維榮非常喜歡法輪功,來教功班之前,他在家曾看過教功錄像帶。 談到他
            為什麼決定來參加法輪功教功班,他說:「法輪功這個功法肯定是好,真、善、忍原則好,
            中國人太需要真、善、忍了。」 他表示,支持法輪功,痛恨共產黨,希望有更多的中國人來
            學功。「中國人來學功的比較少,我感到遺憾。」他認為中國人不來很可惜,「我希望中國人
            不要受中共(宣傳)的欺騙,要了解法輪功真相。」 司徒維榮表示,知道法輪功好,會堅持煉
            下去。 法輪功於1992年由李洪志先生在中國公開傳出,該功法能快速提升人的道德品質,
            同時對祛病健身有奇效,至今,在全球所獲各類褒獎數千份,受到各族裔的推崇。 因法輪功
            遵循「真、善、忍」準則修煉,敬天信神,與中共無神論及鬥爭等意識形態相悖,1999年7月
            ,中共前黨魁江澤民凌駕憲法之上,對這個修煉群體進行打壓,迫害政策持續近20年,無數
            法輪功學員被非法關押、酷刑折磨、判刑,甚至被迫害致死。 「真善忍原則吸引我」 越南裔
            的妮妮女士帶著三個孩子來參加教功班。來之前,她上網查詢了有關法輪功的信息,對法輪功
            非常有興趣。她說:「法輪功的真、善、忍原則非常好,這也是法輪功吸引我的地方。」 來
            之前妮妮感到頭暈,煉功後她感覺輕鬆「今天的教功班信息量很大,對我非常有幫助。」她說
            。 她已經在網上訂購越南語的《轉法輪》,並表示,會去公園的煉功點煉功。 《轉法輪》是
            法輪功創始人李洪志先生最主要的一本著作,書中闡述了宇宙、時空、人體、修煉等博大內涵,
            現已被翻譯為40種語言,在全球一百多個國家和地區發行。 「法輪功對每個人都有益」 印度
            裔居民阿威恩德·巴德特(Arviend Bhadat)表示,「我非常高興找到了法輪功。這個功法對
            身心都有益。我們將繼續煉下去,非常好。」 巴德特還讚揚,教功的法輪功學員非常友善,
            非常熱情,「我要說:謝謝。」 第一次學練法輪功的巴德特表示,他煉功時感受到了能量。「
            可能是身體不好的物質被去掉了,造成壓力的東西去掉了,我現在感覺很好。」 「你們為社會
            做了件好事。免費教功,免費提供資料,詳細地讓我們了解法輪功。」他說:「我會告訴更多
            的人。法輪功對每個人都有益。」 巴德特最後表示,這麼好的功法,「我絕對要告訴給我的
            朋友,向他們推薦。」 參加教功班的瓦什·阿南德(Urvashi Anand)女士身體有許多疾病。
            學功後,她感到非常輕鬆。 「我現在感覺很好。這是我要開始做的事情。我一定會在家煉功,
            也想參加週末在煉功點的集體煉功。」阿南德認真地在紙上寫下了煉功點的地點和時間。 她
            感謝法輪功學員舉辦教功班。並表示,也要去閱讀《轉法輪》一書。 克里希納·納拉亞南
            (Krishna Narayanan)來學功前,從來沒有聽說過法輪功。了解了法輪功後,他說:「我
            喜歡法輪功的真、善、忍原則。」「非常好,我學到了很多。」 學煉功後,他說:「我感到
            平靜。學功時,我感到身體得到放鬆,身體和心靈成為一體,頭腦清醒,對我來說,是個很好的
            體驗。」 他表示,會上網查詢有關法輪功的更多信息,「我絕對會繼續煉下去。」 「感受
            強大能量」 硅谷電腦工程師阿尼什·巴博爾(Anish Babbar)表示,煉功時能感受到很強的
            能量。 「我來到這個班,感覺非常好。煉功後感到身體輕鬆,精力充沛。這個功很好,不受
            時間地點的限制,可以在家煉。」 建築工人大衛·魯恩(DavidLun)下班後參加了教功班,
            他表示,煉這個功非常好,感覺也非常好。煉功可以幫助他,也可以幫助他的孩子。 「我感到
            可以減輕壓力。煉功時,頭腦非常清醒,平時腦子裡的雜念都沒有了。」他說。 來自伊朗的
            希瑪·拉曼(Seema Raman)剛生了一個小孩,感到生活充滿壓力。參加教功班後,她說:「
            現在感覺比學功前好多了。」 「我感到精神振作、煥然一新,精力充沛,煉功時,我感到手
            發熱,有能量,感覺更好了。」
            '''
        ),
    )
    assert parsed_news.category is None
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1556812800
    assert parsed_news.reporter is None
    assert parsed_news.title == '大陸移民舊金山推崇法輪功:真善忍好'
    assert parsed_news.url_pattern == '19-5-3-11232059'
