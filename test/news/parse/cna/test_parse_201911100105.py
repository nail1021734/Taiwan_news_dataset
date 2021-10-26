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
    url = r'https://www.cna.com.tw/news/aipl/201911100105.aspx'
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
            冰島7年級學生莉亞(Lilja Einarsdottir)今天和同學來了趟不尋常的田野之旅:他們
            一同測量索爾黑馬冰川過去這一年間縮減了多少,親身見證氣候的變遷。 莉亞說:「很漂亮,
            但看到冰河消融了這麼多,也覺得很難過。」 2010年起的每年10月,現已退休的教師
            史提凡松(Jon Stefansson)都會帶60公里外村落霍爾斯沃德呂爾(Hvolsvollur)的13歲
            學生,前來測量索爾黑馬冰川(Solheimajokull)的演變。 他們的測量結果讓人不寒而慄:
            過去10年間,夾在兩大山坡間的索爾黑馬冰川,每年平均縮減40公尺。 在這個起了大風
            的10月天,學生們帶著全球定位系統(GPS)、捲尺和兩面黃旗,冒著強風,徒步在不同的
            地點間計算距離。 算完之後,一些學生再跳上小艇,滑過冰川融化後形成的咖啡色湖水,
            來到陡峭的冰壁旁,看看這裡距離去年學生手繪的記號多遠,就知道過去這一年冰川消融了
            多少。 莉亞說:「(第一批學生)開始在這裡測量時,看不到任何的水,所以(冰川)一開始
            非常的大。」 冰島境內約1成1面積是冰川,其中包括歐洲最大的
            瓦特納冰川(Vatnajokull);但過去25年間,冰島的冰川消失約250立方公里,相當於
            總體積的7%。 而學生們測量的索爾黑馬冰川因距離冰島首都雷克雅維克(Reykjavik)最近,
            僅150公里,是相當受歡迎的旅遊景點。它長約10公里,寬2公里,是冰島第4大冰川
            米斯達爾冰川(Myrdalsjokull)的冰舌(冰川分支)。 在學生們測量的這將近10年間,
            索爾黑馬冰川縮減了380公尺。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1573315200
    assert parsed_news.reporter == '冰島維克'
    assert parsed_news.title == '冰島冰川融多快 學生實地測量第一手直擊'
    assert parsed_news.url_pattern == '201911100105'
