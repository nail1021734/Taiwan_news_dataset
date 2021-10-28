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
    url = r'https://www.cna.com.tw/news/aipl/202110070162.aspx'
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
            重陽節將到,金門縣金湖鎮公所今天發放敬老紀念酒。延續去年「福」字主題酒,今年
            推出「祿」字主題酒,並預告明年祭出「壽」字主題酒,集成「福祿壽」3瓶,更有收藏
            價值。 14日是重陽節,金湖鎮長陳文顧與鎮民代表會主席蔡乃靖今天率公所人員到各里
            辦公處關心發放敬老酒作業情形,提前致贈重陽敬老酒給長者,希望貼心的服務可讓長輩感受
            溫馨祝福,祝賀長輩佳節快樂。 陳文顧表示,慶賀110年重陽節,金湖鎮公所特別委託全國
            唯一官窯金門陶瓷廠設計以「福祿壽」系列美瓷加美酒的重陽敬老紀念酒,向轄區長者
            賀節,紀念酒內裝600毫升、58度金門高粱酒。 陳文顧指出,今年敬老主題酒,特別設計
            以「祿」字為主題,代表幸福祥瑞,祝賀每個資深鎮民福如東海、壽比南山;「葫蘆」瓶身
            寓意延綿結果,祝福長者多子多孫,並為表彰資深鎮民對金湖鎮的貢獻。 代表會主席蔡乃靖
            說明,今年敬老主題酒由資深畫師董加添設計繪畫,承續去年推出「福」字主題酒,今年推
            出「祿」字主題酒,並預告明年會推出「壽」字主題酒,到時將可組成「福祿壽」3瓶一組
            主題酒,更添紀念意義和收藏價值。 金湖鎮致贈重陽敬主題酒,對象為年滿65歲以上且於
            109年10月14日前設籍金湖鎮鎮民,共有4497人符合資格;其中有171人年滿90歲,可另外
            獲贈縣政府贈送的重陽紀念酒。
            '''
        ),
    )
    assert parsed_news.category == '地方'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1633536000
    assert parsed_news.reporter == '黃慧敏金門縣'
    assert parsed_news.title == '重陽節將到 金門金湖發放敬老紀念酒'
    assert parsed_news.url_pattern == '202110070162'
