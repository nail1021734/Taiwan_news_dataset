import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ettoday


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='東森')
    url = r'https://star.ettoday.net/news/2000123'
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

    parsed_news = news.parse.ettoday.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            大S(徐熙媛)5日單方面拋出離婚宣言,原因和汪小菲針對兩岸時事發表激烈言論有關,夫妻
            為此大吵一架,消息一出震撼眾人,就有網友翻出男方昔日上節目受訪的片段,當時主持人
            蔡康永曾好奇提問,夫妻倆是否會為了要住北京或台北而爭吵,令在場的小S瞬間變臉、趕緊
            出面幫姊夫擋下犀利提問。 在2015年底時,汪小菲曾上節目《康熙來了》受訪,當時坦言
            因為工作關係經常,需要飛去北京處理,但通常最常只會去4天就回台北,「我一離開我就是
            很不放心,所以就特別累,我可能有時候搭最早的飛機走,然後有時候夜裡就回來。」然而,
            每次剛走大S就會打來關心「老公你什麼時候回來」,他因此坦言:「我無形中心理有些
            壓力。」 節目上,蔡康永先是好奇提問,「所以他們兩個起可愛的小爭執的時候,會冒出
            『那離婚好了』這句話嗎?」立刻被小S狠瞪阻止,讓他慌張笑回:「妳不要我問我就不問,
            妳為什麼要勾引我問呢。」小S接著也笑說,「我姊滿愛撂狠話的。」汪小菲聽完則表示,
            認為大S對小S很好、幾乎從來不對妹妹撂狠話,面對小S好奇「所以你跟他吵架時,你們兩個
            撂過最狠的話是什麼?」他則以「想不起來了」淡淡帶過。 不久後,蔡康永又向汪小菲提問
            :「會不會發生你要她(大S)陪你回北京去,然後她寧願留在台北這種事?」讓小S立刻再度
            變臉瞪向他,讓他無奈直呼:「這個也不能問嗎!到底有什麼可以問的!」一旁的陳漢典也
            笑虧「地雷太多了」,最後小S不好意思地坦承:「這也是他們常常小爭執的一些。」
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1622936160
    assert parsed_news.reporter == '劉宜庭'
    assert parsed_news.title == '脫口汪小菲、大S爭吵內幕! 蔡康永好奇問一句話...小S慌張秒變臉'
    assert parsed_news.url_pattern == '2000123'
