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
    url = r'https://star.ettoday.net/news/1200297'
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
            軍校畢業典禮,是一個軍校生轉換國軍最基層領導的角色分水嶺,也代表了一個通過
            武德、武藝鑑定的軍校生,將離開事事標準、規格、制式化的環境,走向距離「標準」很遠
            的部隊軍陣實務環境,總統主持、任官的軍校畢業典禮,曾經讓軍人一生榮耀,如今榮耀不再
            。 民國44年,黃埔軍校在高雄鳳山復校,那年,陸軍官校24期是在台首屆軍校生,兩岸敵我漢
            賊不兩立,反共,是軍校生承襲老校長蔣中正唯一的從軍理念,24—36期的三軍官校畢業典禮,
            都在陸軍官校舉行,都由蔣中正總統親自逐一對畢業生點名貼標,認證成為「黃埔子弟兵」;
            那年代,能蒙三軍統帥親點、聆聽訓勉,是軍校生畢生的榮耀。 從37期起,畢典從鳳山陸軍
            官校移師台北復興崗政戰作戰學校舉行,那時除陸、海、空三軍官校外,加上政戰學校畢業
            生的「三軍四校」聯合畢業典禮,軍校畢業生都一樣是焦點;畢典前,實施為期2週的「反共
            復國革命教育」,透過高階將領、專家學者反共講演及國防部的思想教育、分組討論,進一
            步強化反共意識、敵我認知。 陸官37期畢業生在蔣經國主持畢業典禮時,因起鬨過於吵鬧,
            引發蔣經國不快,導致37期畢業生任初官期間,不管在哪一個部隊服務,都備受打壓、修理,
            被放話「永不錄用」;但該期實習團長高華柱最後不但升了上將,還出任國防部長、國安會
            秘書長;而在校的38—40期學生則受池魚之殃、掃到颱風尾,不但被加強基本教練、暑訓時被
            狠操;談到這段過往,這幾期學弟還不忘酸一酸37期的學長。 軍校聯合畢典,從陸、海、空
            、政戰三軍四校,增加中正理工學院、國防醫學院為三軍六校,再加國防管理學院、中央警
            官學校成為三軍八校;76年解嚴,軍警分家,原中央警官學校與各軍校新生一起在鳳山陸軍官
            校入伍訓練的政策,改委由陸軍新訓師代訓入伍,也脫離「聯合」畢典陣容自辦。 陳水扁執
            政時,要求國慶焰火等中央舉辦的活動,必須兼顧南北平衡,因此研議軍校聯合畢典移回高雄
            陸軍官校舉行;馬英九上任後,從97—105年,軍校畢典在陸軍官校舉行,為避免三軍統帥同月
            重複南下行程,浪費行政資源,還併陸軍官校校慶實施,蔡英文上台後,106年起再度移回台北
            復興崗舉辦。 三軍四校畢業生2週的反共復國革命教育,集中進駐復興崗,反共思想教育、
            分組討論、聽專家學者反共講座,都是軍方對軍校畢業生敵我意識的最後叮嚀;期間,各軍總
            司令、參謀總長、總統分批逐一對畢業生點名,該唱名答「有」,被軍校生謔稱為「點將」,
            誰都要表現精神抖擻、音調高亢有力,讓長官印象深刻。 軍校畢典由總統親自主持,除頒發
            畢業證書、頒獎績優學生,重頭戲當然是「掛階」任官,當肩上不管掛上「中尉」、還是「
            少尉」階級章,軍校畢業生都知道,保國衛民的重責大任必須一肩挑起;畢業餐會後,2噸半軍
            卡載著一車車新任軍官,直奔圓山忠烈祠,列隊向先賢先烈致敬,宣誓繼志承烈;備役劉姓上
            校說,向先烈敬禮時,感覺胸中熱血澎湃,救國救民捨我其誰? 退役高姓中校說,當卡車駛出
            復興崗大門時,兩旁的民眾向車上的畢業軍官笑著揮手、鼓掌致意,那一刻,軍民一家的溫馨
            ,讓軍人的榮譽感油然而生,那時候,感覺成為軍官的莫大驕傲;他說他從不後悔投身軍旅、
            奉獻一輩子的青春;他感慨地說,任官踏出復興崗各奔部隊後,有些一起相處七年多的同學,
            為國家犧牲了生命,有些幾十年過去了也沒見過面,他只想問一句:「同學,你還在嗎?你還好
            嗎?」
            '''
        ),
    )
    assert parsed_news.category == '軍武'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530136920
    assert parsed_news.reporter == '林健華'
    assert parsed_news.title == '榮耀不再的軍校畢業典禮「反共復國革命教育」敵我意識最後叮嚀'
    assert parsed_news.url_pattern == '1200297'
