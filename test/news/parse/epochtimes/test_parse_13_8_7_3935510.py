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
    url = r'https://www.epochtimes.com/b5/13/8/7/n3935510.htm'
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
            北非國家突尼西亞深陷政治危機,數以萬計群眾聚集在首都突尼斯,要求現任政府下台。 反
            對派議員布拉米(Mohaned Brahmi)7月25日遭到謀殺,引發國內政治動盪,而昨天的示威遊行
            也是他被殺以來,規模最大的反政府抗議活動。 警方估計有4萬人走上街頭,要求溫和派「
            伊斯蘭復興運動黨」(Ennahda)領導的執政聯盟下台。反對派領袖援引突國媒體數據,表示
            示威人數在10萬至20萬之間。 昨天稍早,突國制憲議會(National ConstituentAssembly)
            宣布暫停運作。 布拉米和另1位反對派政治人物貝萊德(Chokri Belaid)遇害案,一般認為
            是激進伊斯蘭分子所為,而伊斯蘭復興運動黨領導的政府則挨批在防止悲劇發生方面做得不
            夠。 這場示威活動集結了多個反對派政黨,從極左派到中間偏右派皆有;遊行發起之時,也
            是貝萊德在住家外遭槍擊身亡滿6個月。 示威群眾手持布拉米和貝萊德的照片,高呼「人民
            希望政權倒台」和「政府將於今天結束」等口號。 這場示威遊行最後和平落幕。 制憲議
            會議長雅法(Mustapha Ben Jaafar)宣布,議會將暫停作業,直到政府與反對派展開對話化解
            僵局,這「符合突尼西亞的國家利益」。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1375804800
    assert parsed_news.reporter is None
    assert parsed_news.title == '突尼西亞政治危機 數萬人示威'
    assert parsed_news.url_pattern == '13-8-7-3935510'
