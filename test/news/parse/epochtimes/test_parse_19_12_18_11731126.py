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
    url = r'https://www.epochtimes.com/b5/19/12/18/n11731126.htm'
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
            今年,中共最駭人的「一胎化」公共政策已邁入40周年。幸運的是,《獨生之國》這部新紀錄
            片,揭開了這個殘酷計劃40年來的陰暗面紗。 中共通過人為控制快速成長的人口,來提升生活
            水準,於1979年開始推行一胎化政策 十幾年來,中共政府一直嚴格執行一胎化政策,在都會
            地區更是如此。 那些不守規定者遭到慘絕人寰的對待,在前幾年,被抓到的有第二胎家庭必須
            付出高額罰鍰,甚至被沒收財產,有些家庭因此幾乎被中共村、省官員摧毀。中共甚至派了
            一支「家庭計劃」軍隊徹底執行一胎化。 有些想要第二個孩子的婦女必須在生完第一胎後
            定期植入避孕器。如果有婦女膽敢自行取出避孕器並懷孕,也難逃定期強制結紮的命運。 數據
            顯示,從1980年到2014年,有三億兩千四百萬中國婦女被植入宮內節育器(俗稱避孕環或
            子宮環),一億八百萬名婦女被強制結紮,此數據還不包括私下墮胎。更悲慘的是殺害嬰兒也在
            有計劃地進行著。 根據統計,在實行一胎化期間,高達500萬名新生兒「被消失了」,直到這個
            政策在2014年被官方停止。 這個駭人的計劃在1992年有了更可怕的發展,中共開始允許外國
            認養孩童。隨之而來的是貪污腐敗還有猖獗的販童黑市。總的來說,中國至少有十三萬孩童
            (根據某些專家說法可能高達百萬)被迫離家,遭賣到公立的孤兒院。 這些孤兒隨後被「賣」
            到美國家庭 (平均認養一個中國孩童需要一萬到兩萬美元),這些錢都進了中共官員和那些
            幫助這個黑市的仲介口袋。更令人髮指的是,中共國有孤兒院向領養父母撒謊,告知他們領養的
            是被遺棄的小孩。事實上,是中共無恥的在操作著這個國際販童騙局。 就如同《獨生之國》
            所揭露的,在中國有成千上萬的家庭現在仍不知道自己孩子的下落(這些孩子被強行帶走)。
            有一個國際平台正在幫助這些孩子找回自己的親生父母。不過只有少數孩子可以重新聯繫上
            他們在中國的家人。 你可能會困惑,雖然一胎化是個悲劇,不過在今日究竟造成了什麼影響?
            畢竟中共已經在五年前廢除此計劃。 其實最大的問題在於,一胎化及其在無數家庭中造成的
            陰影,正顯現了共產主義和社會主義政府的病態本質。一胎化其實是一個失控的中央巨型政策。
            該紀錄片鉅細靡遺地記錄了血淋淋的事實,廣大的中國居民(甚至是那些被迫結紮或墮胎的
            婦女))竟真的相信這個政策的好處及必要性。 這怎麼可能呢?因為(中共)政府不斷用政治
            宣傳對民眾洗腦,強力推行一胎化政策。不論是或明或暗的威脅,還是運用各種洗腦策略,中共
            說服了成千上萬的民眾,一胎化全是為了國家著想。 換句話說,在中國,個人自由屈於共產黨
            及其集體主義意識形態之下。 其實總體來看,最大的癥結在於:一胎化及其在幾十億人民身上
            造成的傷痕,只有在個人自由、私有財產權、法律和社會主義、集體意識形態對立的情況下才
            可能發生。 但願在美國人可以透過《獨生之國》了解社會主義、共產主義和集體主義的扭曲
            之處,還有他們經常造成的瘋狂和巨大傷亡。 就我自己來說,我很榮幸我的父母十年前從中國
            領養了一個小女孩,當時正值一胎化政策的高峰。今天她生活得很好,也很高興有機會可以住在
            美國。我現在好奇她是不是那些中共猖獗人蛇集團的受害者,這我們可能永遠無法得知。 可以
            確定的是,30年來一胎化政策加諸在人民身上的殘酷與恐懼永遠不該被遺忘。 當然,一胎化
            政策的結果是徹底失敗。一胎化造成的兩個災難,使中國的人口正面臨巨大壓力。 第一,
            性別比嚴重失衡,為了傳宗接代,男性人數遠超過女性。 第二,中國青年人口嚴重不足,不足以
            支撐龐大的老化人口。 為了解決這個問題,中共在2016年推出了新的政策:兩胎化。 中共
            集權者永遠無法記取教訓,這眾所皆知。
            '''
        ),
    )
    assert parsed_news.category == '大陸新聞,中國人權'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576598400
    assert parsed_news.reporter is None
    assert parsed_news.title == '中共一胎化警示集體主義之邪惡'
    assert parsed_news.url_pattern == '19-12-18-11731126'
