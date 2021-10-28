import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/202109220330.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            生產不一定會受傷,另一半也不該只是當啦啦隊,而是要當神隊友,接生近300名寶寶的
            好孕工作室負責人、醫師陳鈺萍受邀擔任中央社推出的Podcast節目「文化普拉斯」
            來賓,暢談接生的心路歷程,以及「催產素」感染產婦身邊所有人的神奇體驗。 「生產
            不應該是一場恐怖的體驗,而是幸福滿滿的派對!」陳鈺萍表示,「當醫療介入生產,現代的
            科技程序化了媽媽們的產程,在這個體制下,進醫院變得像跟團,女性成為柔弱的象徵,從妳
            懷孕起便聽從專業照表操課,生小孩這件事,只剩醫生跟護理士的角色,產婦的聲音與助產士
            的功用一樣,早已不存在。」 陳鈺萍說:「台北不缺婦產科診所,缺的是一個善待女人的
            地方。」 陳鈺萍提到,過去的生產經驗,好像產房的大門一關,伴侶就被排除在外了,什麼事
            也不能做,但其實生產是一件值得全家人參與的事,不只是丈夫,她甚至鼓勵產婦的
            小孩、父母、公婆一起來參與。 不過,陳鈺萍也強調,家人的投入,要組成的是一個
            「團隊」,而不是搖旗吶喊的「啦啦隊」,許多人覺得,只要太太生產時,伴侶在場就是
            最大支持,只要能用安全的方法生下孩子就好,無法理解在場與參與的差別,「畢竟產婦的
            心理支持是生產過程中很重要的元素,家人不能只是觀戰,而是要讓產婦覺得有人全力在
            支持。」 「生產過程是做愛的極致。」陳鈺萍提到,產婦在生產時會大量分泌
            「催產素」,使人達到生理高潮,而且不只是產婦,分泌過程同時會以費洛蒙的形式散布在
            環境中,參與的人都會受到影響,「那就像跑馬拉松的人,會產生腦內啡一樣。」 中央社
            近期推出Podcast頻道「中央社好POD」,除了文化性節目「文化普拉斯」之外,「特派
            談新事」由廖漢原和周永捷主持,邀請中央社30名特派輪流上陣談國際新鮮事;「空中
            小客廳」由張若瑤主持,以人物故事為主軸,讓聽眾貼近公眾人物檯面下有血有肉的真實面貌。
            '''
        ),
    )
    assert parsed_news.category == '文化'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1632240000
    assert parsed_news.reporter == '邱祖胤台北'
    assert parsed_news.title == '每一次接生都是幸福派對 陳鈺萍就是要女人不受傷'
    assert parsed_news.url_pattern == '202109220330'
