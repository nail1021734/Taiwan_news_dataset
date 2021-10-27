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
    url = r'https://www.cna.com.tw/news/aipl/201603130226.aspx'
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
            為了讓不同民族的幼兒教育能夠發展出自己獨特的樣子,財團法人至善基金會以及
            資深幼教專家蔡延治帶著3位泰雅族媽媽前往中國大陸雲南,與當地老師幼兒交流互動
            。 即便是在雲南的深山裡,主流、強勢文化的衝擊依然讓少數民族的傳統文化逐漸消失
            ,因此,今年2月,至善帶著台灣原鄉幼兒教育經驗前進雲南山區,由台灣養老部落的3位
            泰雅族媽媽老師游素美、羅蘋萍及何淑雲向雲南的少數民族老師示範如何將泰雅文化融入
            角落教學中。 為了這次的交流,泰雅媽媽們特地設計了4種課程,包含紋面、弓箭、編織以及
            陷阱。蔡延治表示,從一開始的醞釀、修改教案到示範推演,為了找出不足的地方
            ,花了一兩個月的時間。 教學的對象從小孩子變成了大人,媽媽們都直呼好緊張,「很怕
            他們不知道我們為什麼這麼做」。何淑雲說,當初在設計課程時,常會有為什麼要教這個的
            想法,擔心雲南的老師會跟以前的自己一樣,覺得課程內容沒什麼好教的。 從在紙上描繪
            紋面的花紋,到親手做弓箭及陷阱、編織,泰雅媽媽們用了許多的道具來示範如何將泰雅文化
            融入教材之中,每個來研習的老師無不瞪大眼睛仔細聆聽,對於泰雅媽媽們的做法,也都感到
            新奇及驚嘆。 「從來沒有想過可以這樣做」,雲南省玉龍縣幼兒園教學副園長和紅菊說。和
            紅菊也認為,從老師角度,可以感受到泰雅媽媽們對教學的積極及熱情,這次當小朋友學習時
            ,如此特別的經驗會支持他們去做想的事情,也想把雲南納西民族的文化融入教學裡,能參與
            這次的交流覺得很開心且很有收穫。 「當老師必須學習把自己文化精彩的部分傳遞給孩子」
            ,蔡延治表示。她也認為,看著部落媽媽們從非常沒有自信到現在,這次給了他們一個突破的
            機會,希望能夠變成種子教師,讓泰雅文化能夠透過自信的表現傳達出去。 除了透過
            文化交流做師資培訓,至善也會繼續引進台灣角落教學的專業資源,協助玉龍縣各鄉鎮幼稚園
            創建具有自己民族和地方文化的特色園所,也希望募集教具教材資源,開展少數民族幼兒
            多元學習的機會。 每天新台幣20元,每月600元,讓至善陪你長大。請支持雲南幼兒
            照顧計畫,愛心捐款專線:02-23889118。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1457798400
    assert parsed_news.reporter == "吳欣紜台北"
    assert parsed_news.title == '幼兒教育無國界 兩岸原民齊交流'
    assert parsed_news.url_pattern == '201603130226'
