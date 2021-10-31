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
    url = r'https://star.ettoday.net/news/1200001'
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
            一勝難求的上屆亞軍阿根廷,在世界盃D組最後一輪對上奈及利亞,爭取
            最後的出線資格,上半場梅西踢進本屆第一顆進球,下半場雖被奈及利亞靠12碼罰球追平,但
            靠著羅霍致勝進球,終場以2比1奪勝,驚險晉級16強。《ETtoday新聞雲》現在就帶您回顧此
            戰完整精華! 此戰阿根廷大幅換將,5名先發球員出現變動,其中表現不佳的門將卡巴萊羅被
            換掉,改由阿爾瑪尼先發。第14分鐘,梅西接獲長傳後突入禁區,直接右腳爆射,打入球門左
            側,踢進本屆賽會第一顆進球,替阿根廷先馳得點。 下半場易邊再戰,隊長梅西在進場前給
            隊友精神喊話。第49分鐘,奈及利亞左路角球,馬斯切拉諾禁區內拉倒了巴洛根,被裁判給了
            黃牌,並判罰12碼罰球,莫塞斯騙過了門將,輕鬆踢破阿根廷大門,也助球隊扳平比數。 阿根
            廷本場比賽必須奪勝,如果和局收場將遭到淘汰,時間所剩不多的阿根廷,在第86分鐘終於再
            次敲開對手大門,前插的羅霍在禁區12碼起腳破門,這顆進球幫助阿根廷以2比1拿下關鍵勝
            利,賽後阿根廷全體球員擁抱,慶祝本屆世界盃第一場勝利。 晉級16強淘汰賽的阿根廷,下
            一戰將於台灣時間30日晚間10點強碰奪冠大熱門法國隊,但根據過去世足賽對戰紀錄,阿根
            廷2次對戰法國都取得勝利,且最終都挺進到冠軍決賽。
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530054000
    assert parsed_news.reporter is None
    assert parsed_news.title == '梅西進球阿根廷險勝奈國晉級'
    assert parsed_news.url_pattern == '1200001'
