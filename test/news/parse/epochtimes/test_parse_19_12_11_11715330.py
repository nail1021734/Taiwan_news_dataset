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
    url = r'https://www.epochtimes.com/b5/19/12/11/n11715330.htm'
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
            小孩子的眼睛就像攝像機鏡頭一樣,24小時在看著大人。在孩子成長過程中,是否因為您不
            經意的一句話,給他帶來長久的心理陰影?作為父母,如何避免在孩子面前的不當言行? 有
            一天,有一位家長來找我說,自己2歲的孩子幾天前非常慎重地對她說,「媽媽,我是不是笨?
            」 我是笨小孩嗎? 這個媽媽懂得當父母是要學習的,她看過很多書,她也不斷提醒自己,在
            孩子面前講話要小心。孩子問她之後,她反省了自己養小孩的過程,感覺自己沒有流露出自己
            孩子是個笨小孩的想法啊? 我就問這個媽媽,這個孩子一直都是你帶的嗎?她回答說:是,都是
            我自己帶的。 我又問她,在孩子睡覺的時候,或者你覺得他不注意妳的時候,妳會做什麼事情
            呢?她說:我會和朋友打電話聊天啊。 我又問她:你們都聊什麼呢?她回答說:當然都是聊孩子
            的情況啊。 我然後問她:妳有沒有在聊天中開過孩子的玩笑呢?她就被我問住了,她想了想說
            :是有。 我就問她,都說了些什麼呢。她就大叫起來:啊!原來就是我說的! 這個母親可能是
            不經意地和朋友說,也可能只是客氣話,但被孩子聽到,就記住了。雖然2歲的孩子,可能不懂
            「笨」這個詞的意思,但可以從母親的聲音能感受到某種意思。 嬰兒聽力很敏銳 在前面的
            第5講裡面,我們談到到聲音,提到聲音的頻率是有感情的。孩子從母親的聲音中聽出了怪怪的
            意思,有點不是很舒服的感覺,也沒有強烈的痛苦,但是與母親平常的講話不太一樣。 在資優
            孩子教育的定義當中,孩子為什麼聰明,是因為他的接收能力特別敏銳,他可以感覺得到別的
            孩子感覺不到的差異。那個差異越小,接收的越完整,那個孩子的接收能力就越強,就越有能力
            成為資優的孩子。 這位母親的孩子,就屬於這種資優的孩子,他接收到了母親談話中讓他不
            舒服的意思,但他解讀不出來。而且,這個孩子不錯的地方就是,他會去問媽媽。 如果這個
            困惑解決不了的話,孩子會產生一些問題,例如不愛吃東西、睡不著覺、變得愛哭等等。 這裡
            建議父母,如果孩子發生不一樣的變化,需要去回想一下在此之前是否發生過什麼事情,有些
            可能是大人不經意做的、說的。 一般來說,大人發現自己不經意做了對孩子有傷害的事情後
            ,首先是要向孩子道歉,做錯了就要道歉,哪怕是對2歲的孩子。孩子會感受到一件很重要的
            事情,就是大人的誠意。 怎樣和孩子道歉 才是正確的? 人們去買東西的時候,如果是一樣的
            價錢,一般更願意和有誠意的人去買,哪怕這個人的價錢稍微貴一些。因為你知道買回去後,
            會有保證,還有售後服務。 開個玩笑,請問,孩子和媽媽的關係,孩子和爸爸的關係,售後服務
            有多長?太長了,一生吧!所以道歉,表示你誠意,是成功的第一步。 當孩子感受到大人的誠意
            後,他真的願意把內心的感受告訴給大人。他不會隱藏。沒有隱藏,才有解決問題的勝算。 那
            麼怎麼樣和孩子道歉,才是正確的方法呢?就直接說:「對不起,媽媽說錯了」。然後要解釋
            一下,舉一個具體的例子讓孩子更容易理解。 例如,2歲的孩子會不會去拿杯子?會不會摔
            杯子?你可以告訴孩子:其實媽媽誤解了你摔杯子,那個叫做「笨」的行為,那是因為那個杯子
            太重了,你拿不動,我錯了。 第二步,很重要,就是要有改進的具體行為出來。你要拿一個比較
            輕的杯子,倒進他喜歡喝的東西,讓孩子自己去拿,證明孩子他可以拿起杯子。這樣,孩子就
            能夠理解大人的誠意,確實是父母不經意地錯怪了自己。 嬰兒視力有多清楚? 那麼,孩子從
            什麼時候開始,如同攝像頭一樣,24小時盯著大人了呢? 這個問題非常重要,我做兒童心理
            工作已經二三十年了,發現很多父母對孩子開始盯著自己言行的時間點是無感的,這非常普遍
            ,非常多。 我經常做試驗,就是問孩子從什麼時候開始模仿大人的表情。有太多的人回答說,
            是4個月。因為孩子在4個月的時候眼睛的對焦開始完善,看東西開始清楚起來了,才可以模仿
            大人的表情。 1970年代,就有研究發現,如果孩子是吃母奶的,母親抱著他餵母奶的時候,
            媽媽眼睛與孩子眼睛的距離,就是孩子眼睛看得清楚的距離。研究還發現,孩子從出生幾天
            開始,就能看清楚外界事物了。 還有一些研究發現,有些孩子長到6、7歲的時候,會告訴大人
            :在媽媽肚子裡面的時候,我幹了什麼事,我記得什麼。 父母不要因此而緊張,好像不能犯
            錯誤。其實,父母可以做得更好、更開心。我常常鼓勵人家,從教育孩子的過程,一、可以學到
            正向的心態,二、能開發自己很多的智慧。 孩子受驚嚇之後怎麼辦? 孩子除了很小就能看清
            東西,對突然的聲響也能有反應。 每一個生命都要活下去,除了安全之外,還要有保護自己的
            能力。對於突如其來的事情,必然會有保護性的反應。我們不是鼓勵去嚇唬孩子,但在生活
            當中,如開門、拿東西、拖椅子的時候,或者有人按門鈴等等,都會突然發出聲響,這時要順便
            看一下孩子有什麼反應。 如果孩子有被嚇到的感覺,不會很誇張,也不會很厲害,因為是生活
            當中會發生的東西。 如果爺爺突然打了一個噴嚏,把孩子嚇到了,大哭起來。這時,大人就和
            孩子說,對不起,嚇到你了,爺爺不是故意的。這個驚嚇一般不會有問題,孩子哭完就好了
            。 有的孩子在驚嚇之後,在鼻子附近有瘀青,這可能是那裡堵住了。通常是哪裡發青,就要順
            哪裡,有的孩子不只是在鼻子附近。 大人可以順著發青的部位做些按摩,如果堵得比較嚴重,
            可以熱敷一下,再做按摩。把孩子負面的壓力釋放出去,同時媽媽要不斷地輕聲告訴孩子:有
            媽媽在這裡,你不用害怕,我們會保護你。母親可以增加一點抱著他的時間和次數。如果孩子
            感受到,你所說的承諾後,他就會放鬆下來,產生信任和依賴的關係了。
            '''
        ),
    )
    assert parsed_news.category == '美國,舊金山,生活嚮導,教育,家庭教育'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1575993600
    assert parsed_news.reporter == '曹景哲'
    assert parsed_news.title == '「我笨嗎?」 父母的不當言行'
    assert parsed_news.url_pattern == '19-12-11-11715330'
