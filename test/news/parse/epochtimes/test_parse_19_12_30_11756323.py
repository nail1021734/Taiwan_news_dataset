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
    url = r'https://www.epochtimes.com/b5/19/12/30/n11756323.htm'
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
            清代一個住在北村名叫鄭蘇仙的人,一天晚上夢見自己到了冥府,看見閻羅王正在登記審判剛
            抓到冥界之人。其中一個鄰村的老婦人來到大殿後,閻王一改嚴肅的面容還向其拱手,並賜了
            一杯茶,然後下令冥吏將她送到一個好人家轉生去。 鄭蘇仙十分不解,就私下問冥吏道:「
            這位農家老婦,究竟有何功德?(居然得到這樣的待遇)」冥吏說:「這位老婦人一輩子都沒有
            損人利己之心啊。說到利己之心,即便是賢德的士大夫也不能保證沒有。然而利己者必損人,
            是以各種各樣的巧詐因此產生,各種各樣的冤怨也由此造成,甚至遺臭萬年、流毒四海,都是
            因為這一念帶來的。這位老婦人能克制自己的私心,就連讀聖賢書的儒生們面對她時也不免
            慚愧,大王對其施禮當然也就不奇怪了。」 聽了這一番話,鄭蘇仙心中一驚,有所醒悟。 在
            農家老婦人見閻王前,鄭蘇仙還見到一個身著官服的人昂然進入冥府,他自稱在世時不論走到
            哪裡,都只喝老百姓的一杯水,所以自覺無愧鬼神。 閻王哂笑道:「朝廷設立官員管理百姓,
            下至管理驛站、閘門的小官,在處理事情時,都要按照朝廷之法權衡利弊。如果說不要錢就是
            好官,那麼將木偶放在公堂上,它連水都不喝,不是更勝你一籌?」 官員辯解道:「我雖然沒
            什麼功勞,但也沒有罪過啊。」 閻王說:「你為官處處求的就是保全自己,在這個和那個案子
            中,你為避嫌疑而保持沉默,這不是有負於百姓的信任嗎?還有在這件和那件事上,你因為畏懼
            麻煩而沒有上報朝廷,這不是有負於國家對你的信任嗎?為官者,通常三年考察一次政績,無功
            就是有罪矣。」 聽到閻王如此評判自己的功過,官員在恭敬下又有些不安,剛來時的銳氣頓減
            。閻王注意到官員的變化後,笑著說:「(剛才說那番話)只是怪你太盛氣凌人罷了。平心而論
            ,你還算得上三四等的好官,來生還是會獲得功名的。」隨即讓冥吏將他送到轉生的地方
            。 紀曉嵐記錄此事後,感慨道:人心中哪怕細微的念頭,甚至是那些晦暗不明確的想法,鬼神
            都能夠窺見。即使是賢者一念中的私心,也不免要受到責備。這樣的事情在我們身邊確實存在
            啊。
            '''
        ),
    )
    assert parsed_news.category == '文化網,文明探索,前世今生,善惡有報'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577635200
    assert parsed_news.reporter is None
    assert parsed_news.title == '清朝人冥界見聞:人心生一念 天地盡皆知'
    assert parsed_news.url_pattern == '19-12-30-11756323'
