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
    url = r'https://www.epochtimes.com/b5/19/12/22/n11738876.htm'
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
            10年前在拘留所被打殘的遼寧凌源法輪功學員李亞君,於2019年7月5日被凌源市國保警察
            連抬帶拽塞進轎車,送到朝陽市看守所,被拒收。 近日,明慧網報導,7月5日上午9點多鐘,
            李亞君的家裡突然闖進凌源市公安局國保大隊七個年輕警察,把李亞君強行從三樓折騰到離家
            很遠的地方,塞進他們的車裡,綁架到公安局的國保大隊,並搶走她家中的法輪功書籍等物品
            。 在審訊室裡,李亞君沒有按照他們的要求坐在被審的位置上。她說:「那不是我們好人坐的
            地方。」警察在電腦前問她叫什麼、多大歲數?李亞君說:「今天如果不是在這個場合,我會
            告訴你們,你們也不用往下問了。」 警察在電腦上操作了一會兒,然後打出單子來,李亞君
            不知道上面寫的是什麼。 報導說,在她遭到極大冤屈的情況下,依然按照修煉人真、善、忍
            標準要求自己,善心對待警察,不停地給他們講法輪功真相,不要迫害好人等。 大約下午2點
            多鐘,警察讓李亞君上警車,告訴她是去朝陽市看守所,兩百多里路程。途中李亞君一直給警察
            講真相。 到朝陽市中醫院體檢後,警察開車把她拉到朝陽市看守所。兩個警察一邊一個攙扶著
            她走進接待大廳。那裡的醫生一看李亞君身體這樣,當場拒收。 當日,警察從上午9點多到
            晚上8點一直劫持著李亞君,將她整整折磨一天。 在中共迫害法輪功長達20年的迫害過程中,
            李亞君曾遭受一次非法傳喚、四次非法拘留、二次綁架、一次被判勞教1年(勞教所拒收)、
            兩次流離失所共4年。 在這麼多年中,李亞君的家沒有過上幾天安穩的日子,她本人更是幾次
            被迫害到死亡的邊緣上。 在拘留所裡,警察在扭打她的過程中,她由外傷引起頸椎神經受損,
            即中樞神經損傷,引起「高熱抽搐」,造成她長期高位癱瘓,脖子一下沒有知覺,生活不能自理
            。這給她及其家庭帶來了巨大的磨難。 即使這樣,至今警察還不放過她,還企圖非法關押她、
            起訴她。 7月5日李亞君遭受的這次綁架,給她及她的親人身心帶來很大的傷害,同時她的家人
            和周圍鄰居百姓們都親眼目睹了,在光天化日之下,凌源市國保警察用暴力抓一個10年都不能
            出樓的人,見證了中共邪黨對法輪功迫害的邪惡。
            '''
        ),
    )
    assert parsed_news.category is None
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576944000
    assert parsed_news.reporter is None
    assert parsed_news.title == '被打殘 遼寧法輪功學員李亞君再遭迫害'
    assert parsed_news.url_pattern == '19-12-22-11738876'
