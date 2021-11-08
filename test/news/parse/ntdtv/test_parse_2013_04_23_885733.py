import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2013/04/23/a885733.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            美國阿拉巴馬州一對讀書普普通通的夫婦有10個小孩,透過在家自學,其中6個小孩
            在1 2歲以前讀大學,另外4個也準備在12歲時考大學。日前,這對夫婦出了一本書披露
            教子之道,他們深信,所有的孩子都能透過學習成為神童。 曾當過護士的
            蒙娜麗莎(Mona Lisa),讀書時的成績普通,丈夫奇普(Kip Harding)曾在軍中開
            直升機,25歲才大學畢業。兩人婚後連生10個孩子,蒙娜麗莎決定待在家裡,親自教育
            孩子。 哈汀夫婦並非人們眼中的天才,但他們卻培養出一群越級上大學的孩子,他們把小孩
            的成就歸功於「家庭教育」。 日前,哈汀夫婦出了一本書《12歲前上大學》披露
            教子之道。他們深信,所有孩子都能透過學習成為神童,關鍵是把這種實力給挖掘
            出來。她說,「我先找出他們的興趣是什麼,然後逐漸加快他們這方面的學習速度」,等到
            他們5、6歲時,就會將學習當作習慣了。 哈汀夫婦24歲的大女兒漢娜(Hannah)還沒
            22歲,就取得數學、機械工程和太空船設計等碩士學位,順利當上太空船設計師。22歲的
            二女兒瑟琳娜(Serennah)正在讀醫學院,即將成為美國最年輕的醫生之一。三女兒18歲當
            建築師;未滿17歲的四兒子,即將拿到電腦碩士學位;14歲的五兒子,10歲考上大學,現在是
            數學系大四生;12歲的六兒子,去年剛考上大學。
            '''
        ),
    )
    assert parsed_news.category == '奇聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1366646400
    assert parsed_news.reporter is None
    assert parsed_news.title == '神童家庭!10小孩有6個12歲前上大學'
    assert parsed_news.url_pattern == '2013-04-23-885733'
