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
    url = r'https://www.ntdtv.com/b5/2011/12/25/a636878.html'
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
            「2011年美食食品展覽」是馬來西亞第一個最大型食品消費展,於12月16日至18日一連
            三天在吉隆坡太子世界貿易中心舉行。首次舉辦就得到超出預期的人潮,佳績可喜。 為期
            三天的食品消費展成功吸引了逾10萬人參觀,超出了主辦方預期的人潮。首次舉辦這項
            展覽會就獲得如此好的佳績,令主辦方驚喜萬分。 宣傳經理李榮倫指出, 其實在馬來西亞
            著名的食品展有好幾個,但是那些主要是針對貿易展,然而有如這麼大型,走消費路線的
            食品展在馬來西亞可以說是第一個。他們用了大概一年的時間來籌備這次的
            展覽會。 李榮倫: 「我們全公司的整六個成員都做的很辛苦,而且我們遭遇很多商家的
            拒絕,始終他們對我們的認識不深,但是我們真誠去感動他們。」 市場經理封雪婷:「對,
            剛剛開始他們(商家)對我們沒有信心,但是我們有我們的市場策略跟他們去談,跟他們去
            交流,一直跟他們跟進,所以才有今天的成績。我們希望明年會做的更好。」 在這三天的
            展覽會中,主辦方安排了多項豐富節目,包括烹飪示範、健康講座、還有來自美國印地安人
            音樂家威爾森.樂馬(Wilson Lema)的清新獨奏,以及由法輪功修煉團體組成的腰鼓隊和
            天國樂團所呈獻的精彩表演,使民眾為之讚歎。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1324742400
    assert parsed_news.reporter == '謝岫芳在馬來西亞吉隆坡'
    assert parsed_news.title == '馬來西亞最大型食品消費展'
    assert parsed_news.url_pattern == '2011-12-25-636878'
