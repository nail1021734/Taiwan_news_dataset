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
    url = r'https://www.epochtimes.com/b5/13/6/6/n3887756.htm'
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
            輪迴轉世的記載,在世界各地都有很多。清代文人李慶辰就曾記錄過這樣一則真實的輪迴案
            例。在粵東地區,也就是廣東省的東部,有位士人娶了一位儒生的女兒,生了三個兒子:長子
            十九歲,次子十七歲,第三個兒子六歲,長子和次子都是書生,刻苦攻讀,唯獨第三個兒子自出
            生以來從未開口說話,因此大家都認為他是個聾啞兒童,也就沒有教他識字。 一天這位士人
            給他的兩個兒子布置了作文題目後就走親戚去了,兩個兒子在家反覆構思,也沒有寫出文章
            來。這時他們六歲的弟弟突然開口向兩個哥哥說,這題目的要點是在何處,文章該如何如何
            寫。兩個哥哥聽了大驚失色,弟弟不是聾啞兒嗎?怎麼說話了?弟弟告訴他們:不要驚慌,我只
            是記得前世罷了,請把筆墨給我,讓我替你們寫這篇文章吧!兩個哥哥相信了弟弟的話,只見
            弟弟運筆如飛,一篇佳作就這樣完成了。 士人晚上回來檢查兒子的功課,讀了文章後感歎道
            :此文才思敏捷,讀著只覺得像你們外祖父的文風,你們應該寫不出來這種文章吧,老實告訴
            我,你們究竟是抄襲誰的文章?兩個兒子見瞞不過去,就向父親坦白是弟弟寫的。 士人非常
            驚奇,反覆詢問六歲的幼子。幼子先不說話,後來才不得不開口道:我忍耐數年不說話,今天
            卻一時興起寫了文章,看來不得不告訴你們實情了。唉,我前世就是你的岳父啊。當年我也
            沒有什麼大病,一天在床上躺著午睡時,元神卻起身離開了肉身,信步向女婿家走去。不料剛
            進門就跌倒了,只覺渾身發冷,睜眼一看自己居然是赤條條的一個初生嬰兒。又見女兒正躺
            在產床上休息,當下明白自己原來已經死了,現在又投胎轉世了,頓時大哭起來。後來自己慢
            慢也想通了,生老病死,實乃人之常理。然而難堪的是前世的女婿、女兒竟成了今生的父母,
            前世今生的倫常關係竟顛倒過來了,故而一直不願開口叫人,以致被人當成啞巴。說完孩子
            便悲痛地大哭。士人震驚無比告訴了妻子,妻子核對了幼子出生的時間,竟然正是自己父親
            去世的日子,頓覺悲痛。 後來這個孩子告訴士人夫妻,他希望出家為僧,擺脫這種前世今生
            倫常關係顛倒的生活。夫妻二人最終同意了孩子的請求。李慶辰記錄這件奇事的時候,這孩
            子已過而立之年,正在寺廟中努力修行呢!
            '''
        ),
    )
    assert parsed_news.category == '文化探尋'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1370448000
    assert parsed_news.reporter is None
    assert parsed_news.title == '輪迴記載:外祖父轉生成外孫'
    assert parsed_news.url_pattern == '13-6-6-3887756'
