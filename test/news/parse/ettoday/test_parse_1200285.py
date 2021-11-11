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
    url = r'https://star.ettoday.net/news/1200285'
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
            作為2018年俄羅斯國際足協世界杯TM官方指定啤酒贊助商,百威啤酒在6月22日~6
            月23日於台北市ATT4FUN前廣場舉辦「最強射門大挑戰」,請到知名直播主擔任「百威足球
            女孩」,現場民眾興奮地秀出自己的足球技巧,開心贏得世足賽必備加油物品! 為了帶給台
            灣球迷難以忘懷的體驗,百威在全台打造6間FIFA期間限定酒館,並將在16強、冠亞賽期間,
            於台北及台南各舉辦一場百威FIFA直播派對,為球迷及酒友們準備豐富的現場互動活動及限
            量小禮,同樣邀請到知名直播主擔任「百威足球甜心」親臨現場與觀眾玩遊戲,一起為各自
            支持的球隊加油吶喊,創造美好回憶。 此外,在8強賽時,百威將在高雄啤酒節首次舉辦連續
            兩日的的狂歡派對「百威FIFA之夜」,以300吋超大螢幕直播八強賽事,並且為高啤晚間唯一
            不熄燈不停業的酒館,等著你與百威一起嗨整夜!現場預計設立大型百威酒館,在啤酒節整整
            三日中帶來豐富的活動,必備的手足球台以及百威吧台之外,「最強射門大挑戰」讓大家挑
            戰足球射門,踢中就有機會獲得限量加油神器「卡西羅拉」。全台灣通路皆已推出百威FIFA
            贈品活動,包含FIFA國家收藏杯及世界杯,高質感抱枕及官方聯名FIFA後背包等,設計有不同
            國家風格與文化元素,讓球迷可以蒐集自己所支持的國家球隊。
            '''
        ),
    )
    assert parsed_news.category == '民生消費'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1529989500
    assert parsed_news.reporter == '百威啤酒'
    assert parsed_news.title == '世足期間限定 挑戰最強射門贏好禮'
    assert parsed_news.url_pattern == '1200285'
