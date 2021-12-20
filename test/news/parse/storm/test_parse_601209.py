import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.storm


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='風傳媒')
    url = r'https://www.storm.mg/article/601209?mode=whole'
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

    parsed_news = news.parse.storm.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            同志在明年五月以後就可以結婚,已經成為定局,只有訂定專法與直接入民法的差異,任何公投
            結果,都不能阻擋同志結婚。所以,認為公投通過以後,就會導致孩子喜歡同性、台灣一片
            大亂、以後不曉得怎麼稱呼阿姨的老婆、台灣以後沒人生小孩、人跟摩天輪以後就可以結婚、
            外國人會進來台灣享用台灣健保資源等等的人,請不要關心這些公投,因為結果都一樣。上面
            擔心的結果,明年五月以後,自動會發生。 那麼,我們到底在辯論什麼?坦白告訴你,支持
            同志的異性戀也好,自己就是同志的朋友也罷,這些人都在支持基本人權,或者說,反對一種
            「某些人是人,某些人則是把人當人看」的態度。但是這與同志結婚,一點關係也沒有。 這次
            的公投明明就不是在表決同志能不能結婚,而是表決要用平等的方式,還是踐踏人權的方式
            結婚,這些人為什麼就是不把焦點放在入民法或是立專法上,而是一再討論同志結婚後,會有
            多麼禍國殃民?真的,我很遺憾的告訴反對派,禍國殃民已經確定,不要去領票,你會比較開心
            。那麼,阻擋入民法總可以吧? 專法派可以問問自己啊!阻擋入民法的目的是什麼?還不都是
            婚姻嗎?不過就是專法婚姻與民法婚姻的差異,大家都是台灣人,幹嘛分這麼細呢?因為,你不
            能跟我用一樣的制度,你要用別的制度。可是異性戀瑞凡,我們回不去了,因為制度都一樣,
            只是一個在民法,一個在專法。即使是專法的婚姻制度,也得要跟民法一樣,否則就會違反大
            法官會議解釋憲法的意思。 可能進一步的專法派疑問就是,既然都一樣,那麼你們這群支持
            同志的異性戀,還有同性戀,你們不分性別在反對什麼?那就滿足專法派一點卑微的需求,立
            專法不是很好,又可以弭平社會地方傳統壓力? Hello?同性戀與異性戀一樣,真的不是每個
            人都非常渴望婚姻制度,有些深受其害者,還會鼓吹大家不要進入這牢籠,以免早晚還是要讓
            呂律師賺取律師費。有了不一定要用,重點不是結婚,重點是平等。就像是有些支持民法派的
            異性戀會說,拜託,我們是在「幫」你們耶,怎麼這麼不知好歹? 幫什麼幫!你是在幫自己。
            當同志婚姻已經成為事實,民法平權就會是義務。有人受壓迫,有人就要反抗,這些人已經不被
            當作人看太久,將來如果不想讓自己以後被壓迫時沒人出手,現在是不是該動手?當你投下
            民法派這一票,不是因為你支持同志婚姻,畢竟這是大法官做的決定,你無權改變。這一票,
            是因為你支持人權、支持平等理念、支持核心價值,所以你才投票支持民法派。怎麼會是
            「異性戀」幫助「同性戀」?還一副我都施恩給你,你得感激涕零的樣子?你是給自己一個
            交代,為自己之所以為人的價值負責。 只有入民法,才能讓他們發現,自己原來跟其他人
            一樣,重點從來就在於平等,而不是婚姻。不能適用同一套法律,哪來的平等? 你沒看過地獄,
            就別急著以為自己可以寫神曲。不談同志婚姻,因為已經是事實,雖然人權不應該公投,
            但是你的這一票,將決定這些台灣人「口口聲聲認定的親愛同胞」,是「把他們當人看」,
            還是「他們本來就是人」。
            '''
        ),
    )
    assert parsed_news.category == '風生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1541445480
    assert parsed_news.reporter == '呂秋遠'
    assert parsed_news.title == '同志已確定能結婚,為何堅持要用民法?呂秋遠:差在「把你當人看」還是「你本來就是人」'
    assert parsed_news.url_pattern == '601209'
