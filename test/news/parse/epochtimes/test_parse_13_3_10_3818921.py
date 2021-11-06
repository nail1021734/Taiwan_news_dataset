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
    url = r'https://www.epochtimes.com/b5/13/3/10/n3818921.htm'
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
            春秋後期的魯國,政權握在季氏手中。哀公四年至二十七年(公元前506~前468年)執掌國政
            的是季康子,季康子權傾魯國,他的叔父公父文伯則是很受寵信的大夫。 魯季敬姜,是莒國
            的女子,號戴己,魯國大夫公父穆伯的妻子,公父文伯的母親,季康子的從祖母。她博識通達,
            熟諳禮儀。穆伯早逝,她一直守寡,撫養兒子。 敬姜到季氏家去,季康子正在大堂,和她打招
            呼,敬姜沒回應。康子跟著她走到家室的門口,敬姜也不答應一聲就進去了。 康子放下工作
            ,離開廳堂,進入內室去見敬姜,說:「我剛才沒聽到您的教誨,是不是得罪您老人家了?要不
            怎不理我呀!」 敬姜說:「你沒聽說過嗎?天子和諸侯商議人事在外廷,研究神事在內廷;從
            『卿』以下,商議公事在外堂,研究家事在內堂;而寢門之內,則是婦人做活的地方。上上下
            下都是同一個規矩。外堂,你要辦理國君交給的公務;內堂,你要處理季氏家族的私事,都不
            是我這婦道人家敢說話的地方啊!」 康子到她家去的時候,她開著門和康子說話,彼此都不
            跨過門檻。祭祀悼子時,她不親手接康子獻的祭肉,也不參加撤除祭器後的宴飲。如果宗臣
            不在,就不再祭;再祭之後,飫(音玉)禮未畢就先告退。 孔子聽說以後,認為敬姜是懂得男女
            有別之禮的。 《魯語上》裡還有這麼一件事: 哀姜(魯莊公夫人)來到魯國,莊公命令大夫
            、宗婦都用玉、帛之類為見面禮去拜見哀姜夫人。宗人夏父展說:「沒這種規矩。」莊公說
            :「規矩都是國君定的。」夏父展回答說:「國君的創制如果順乎禮義,那就可以成為成規;
            如果違背禮義,那就要在史書上記載它違禮。臣既然忝為宗人之官,就不能不懼怕這違禮之
            舉不幸載入史冊傳之後人,所以不敢不告。」 「依禮,婦人的見面禮,只不過是些棗子、栗
            子一類的東西,用以表示勤勉敬畏之婦道。男子的見面禮,才可以使用玉、帛、禽、鳥,用以
            表示尊卑貴賤的不同身分和地位。如今,您讓宗婦也拿玉帛去晉見,這就沒有男女之別了。
            男女之別,是國家禮治的關鍵大節,不可廢除啊!」 莊公不聽他的勸諫,結果哀姜禍亂魯國,
            導致災變連年。 從這幾則史實看來,上古時期神傳文化,對「禮」的講求是非常嚴格與細緻
            的,內外朝、內外堂、門檻內外;神事、政事、公私事、男女、見面禮......等等,都有一定
            的規矩、禮節與限定,根本不得逾矩,否則就是與禮不符,讓人笑話的。 特別是男女有別,以
            今日的眼光看來,簡直迂腐不堪。可人是神造的,之所以男女有別,是因為神造時所帶的特質
            、因素不同而有男女、陰陽之分。 陰柔陽剛之故,所以男主外、女主內,剛柔並濟、陰陽調
            和而成就家、國、天下而達天人合一的境界。並非互爭短長、互別苗頭、自立為王,而是讓
            你因著天賦、秉性的不同而和衷共濟,相互配合,各就其位開創幸福美滿的家庭生活。 所謂
            時代進步而造成的負面影響,已經超越其正面價值許多倍了,因著男女無別、關係混亂的結
            果所衍生的社會問題,已不是渺小的人所能解決了,只能等著「天治」啦!
            '''
        ),
    )
    assert parsed_news.category == '文化網,文化百科,文化博覽,文化漫談'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1362844800
    assert parsed_news.reporter is None
    assert parsed_news.title == '敬姜論男女有別之禮'
    assert parsed_news.url_pattern == '13-3-10-3818921'
