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
    url = r'https://www.epochtimes.com/b5/19/12/21/n11737639.htm'
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
            蘇東坡的弟弟蘇轍編纂的《龍川略志》,記載了他的所見所聞,對當朝的時局、朝政、國風與
            民情多有記述,其中還記載了不少發生在當時的奇聞。比如,他的哥哥蘇東坡獲得點金方術,
            但不曾妄用的事蹟。 北宋時期,開元寺中保存著不少古畫,蘇東坡少時喜歡書畫,常常騎馬到
            寺院,整日待在牆壁前,研習古畫。一天,有一位老僧對他作揖,說:「我住的小院就在附近,您
            能否到我們那兒看看?」老僧相請,蘇東坡欣然答應了。 原來老僧見東坡是有事相託。這位老
            僧平生喜好煉藥方術。他有一個祕方,能以硃砂化淡金為足金。因其已經年邁,所以想把祕方
            傳出去。但苦於一直找不到忠厚之人。他在寺院見到蘇東坡,知道可以傳給他,故而邀請蘇東坡
            到小院一見。 蘇東坡說:「我不喜好點金術,雖然稀有難得,我也不會去用。」 老僧說:「
            對於這個方子,最重要的就是明知道,但也不會擅自亂用。假如你無意要用,正好可以傳給你。
            」 當時,陳希亮在扶風為官,此人平生沉溺於點化金銀的方術,曾經向老僧尋求此方,不過老僧
            沒有給他。蘇東坡問道:「陳卿求方術,您不給;我又不求反而得到,這是為什麼?」 老僧說:
            「貧僧並不是不喜歡陳卿,而是擔心他得到這個方子把握不住,就會亂用。我以前曾將這個方子
            交給他人,結果有的人剛用就死,有的遭遇喪亡,有的失去了官位,所以不敢輕易再傳於他人。
            」說罷,即取出一卷書交給蘇東坡,上面都是點金之方。老僧再次叮囑他:「你必是不會輕易
            擅用,但也勿要輕易授予他人。比如陳卿,一定要謹慎,勿要相傳。」蘇東坡答應了。 後來有
            一天,蘇東坡偶然遇見陳希亮,二人談話間,提到那位老僧,可能正說在興頭上,蘇東坡一時沒
            留心說漏了嘴:「最近,我得到老僧的點金方了。」 希亮驚訝地問:「你怎麼得到的?」讓他
            趕快拿出來看看。蘇東坡意識到自己失言,轉而說老僧叮囑不能輕易傳人、示人。但終是架不
            住對方的苦苦哀求,蘇東坡不得已就給了他。希亮回家一試,效果果然不錯。蘇東坡後悔地說:
            「我把方子交給你,真是辜負了老僧的一片好意。你以後謹慎為之吧。」 但是不久之後,
            陳希亮就因鄰郡官員違法之事,受到牽連,以其贓款泄漏而被革職,從此官運敗落。蘇東坡懷疑
            他曾以黃金賄賂鄰郡長官,為此深深自責。 後來,蘇東坡謫居黃州,陳希亮的兒子陳慥也在
            黃州,蘇東坡問起陳父的情況。陳慥說:「我的父親被革職後,來到洛陽,沒有錢買宅院,所以
            又大用點金方術,結果竟一病不起,已經病逝了。」聽到這個消息,蘇東坡唏噓不已,方知老僧
            先前的叮囑實在不是妄言。 蘇東坡的弟弟蘇轍謫居筠州時,有個蜀地的僧人法名儀介,拜文
            禪師為師。文禪師到來後,儀介為他修造住所,花費了許多錢財,但人們都不知道他的錢財來自
            哪兒。人們認為他一定有祕術,但是問他,他也不說。 這位儀介和尚與聰禪師交往很深厚,曾
            悄悄地對聰禪師說,他的點金方由扶風開元寺僧所傳。然而儀介不曾將一錢用在自己身上,為
            己謀取絲毫私利。所以能安然無虞。 南宋時期胡仔編纂《苕溪漁隱叢話》收錄了這些事,對此
            評價道:「《洞微志》也曾記載過葉生的事蹟,與前面的事情很像,也是因為得到點金術,擅自
            亂用,反而招致災禍。所以呂洞賓對沈東老[注]說:『聽說你有點金術,卻從不妄用,並且篤行
            仁孝節義,素來積下大德。』對他深表讚歎。這些故事真可作為貪者的借鑑。」 [注]:沈東老
            ,宋神宗時期東林庵隱士,本名叫沈思,當地人叫他沈東老。沈東老樂善好施,又是釀酒高手,
            釀得「十八仙白酒」很有名氣。他雖有點金術,但從不妄用,因此受到呂洞賓的稱讚。臨走
            之前,還在石榴皮上為沈東老題寫一首詩,曰:「西鄰已富憂不足,東老雖貧樂有餘。白酒釀
            來緣好客,黃金散盡為收書。」
            '''
        ),
    )
    assert parsed_news.category == '文化網,文明探索,人體修煉•長生延年,特異功能'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576857600
    assert parsed_news.reporter is None
    assert parsed_news.title == '真有點金術? 蘇東坡不求不用'
    assert parsed_news.url_pattern == '19-12-21-11737639'
