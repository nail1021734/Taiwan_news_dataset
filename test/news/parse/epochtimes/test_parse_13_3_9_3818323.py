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
    url = r'https://www.epochtimes.com/b5/13/3/9/n3818323.htm'
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
            「從來陰騭(zhì,陰德)能回福,舉念須知有鬼神」,這兩句詩句說自古以來積德做好事都是
            有福報的,因為天地之間人生一念,鬼神是都知道的。古代印證這個理的故事有很多,今天就
            來說說裴度還帶的故事。 唐朝晉公裴度(765年─839年)在未發跡之前,生活得很破落,一貧
            如洗。一天他去找一個相士算命,那相士說:「先生的功名之事,先且不必問。我這裡有句話
            ,如若您不見怪,我才敢說。」裴度回答道:「我正是因為在迷途才來找先生詢問,怎麼會見
            怪呢?」相士說道:「先生有蛇藤縱理紋入口,數年之間,必將餓死在溝渠。」說完之後,相士
            堅持分文不取。裴度本來就是個知命的君子,也沒有把相士的話放在心上。 一天,裴度到香
            山寺閒遊,見到供桌上金光閃閃,走近一看原來是一條寶帶。裴度想一定是有什麼貴人到這
            裡禮佛更衣時忘記的,應該會回來找尋。於是便收了帶子在廊子下等候。過了一會兒,只見
            一個女子慌慌張張地逕跑到供桌前張望,連聲叫苦,哭倒在地。 裴度走上前問道:「小娘子
            為何如此哭泣?」那女子說:「我的父親被人陷害,無門申訴,之前我曾來此求佛祖保佑。現
            在父親終於從輕贖緩。可惜我家貧窮拿不出錢來。我求遍了高門,終於昨天有一貴人可憐我
            ,借給了我一條寶帶。我知道是佛祖相助,今天就拿寶帶來呈於佛祖以表感激。可惜贖父心
            切,走之前竟然忘了收那條帶子。半路上想起就趕回來,可是帶子已經不在了。沒了這條帶
            子,我父親真是不知道什麼時候才能出獄了。」說著又哭了起來。 裴度拿出帶子對那女子
            說道:「姑娘不必悲哀,帶子我撿到了,一直在等失主來領,現在就把帶子還給你吧。」那女
            子感激不盡想要問裴度的姓名,他日來拜謝。然而裴度覺得還人遺物本就是理所當然的事情
            ,所以沒有告訴姓名就走了。 過了數日,裴度又遇見了那個相士,相士看到他非常吃驚,就問
            他近日來是不是做過什麼好事,裴度說沒有。相士說:「先生您今天的面相比先前有很大不
            同。 您的陰德紋大顯,他日必當位極人臣,福壽雙全啊!」裴度當時以為相士只是在說戲言
            。 後來,裴度果然出將入相,歷事四朝,被封為晉國公,年享上壽。
            '''
        ),
    )
    assert parsed_news.category == '文化網,預言與傳奇,神話傳說,中國民間故事'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1362758400
    assert parsed_news.reporter is None
    assert parsed_news.title == '裴度還帶改變命運──從餓死鬼到宰相'
    assert parsed_news.url_pattern == '13-3-9-3818323'
