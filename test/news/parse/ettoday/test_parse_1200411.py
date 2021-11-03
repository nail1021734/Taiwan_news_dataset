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
    url = r'https://star.ettoday.net/news/1200411'
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
            韓國花草系咖啡廳正當紅,位於彰化員林市的《右舍咖啡》不僅周遭被綠意包圍,玻璃窗外
            的整面藤蔓綠牆療癒人心,右舍咖啡其實已有10年歷史,是當地人都知道的老牌咖啡店,改裝
            後明亮時尚的空間,讓人經過都忍不住打開門進去待上一會兒。 《右舍咖啡》是當地的人
            氣咖啡店,結合了老宅、咖啡甜點集與藝術人文,建築本身為老屋改建,一、二樓為咖啡廳用
            餐區,三樓則是展演空間每月固定展出不同靜態作品。樓梯是老舊的復古磨石子,挑高明亮
            的空間與大面玻璃窗任陽光恣意灑進,坐在裡頭喝杯咖啡也變得氣質了起來,館內也會不時
            舉辦講座、旅遊交流分享會、音樂活動等,大力推廣在地藝文風氣。 除了提供好咖啡豆讓
            「懂」咖啡的人都能喝上一杯精品級的好咖啡外,老闆也很要求店內的氣氛營造,不少傢俱
            都是特地找回來的古物,堅守老靈魂精神,且堅持不擺放過多桌椅讓空間變擁擠,甚至霸氣貼
            文公告「無法接待每組超過六位以上的團體」不是太跩而是座位真的不夠,下次想要內用在
            大片玻璃窗前放空曬太陽,只能看看當天有沒有撞見小確幸了。
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530145800
    assert parsed_news.reporter is None
    assert parsed_news.title == '6人團體不招待!彰化花草系老咖啡館有個性 在地人都知'
    assert parsed_news.url_pattern == '1200411'
