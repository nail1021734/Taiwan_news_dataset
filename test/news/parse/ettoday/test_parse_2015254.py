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
    url = r'https://star.ettoday.net/news/2015254'
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
            雲林縣救難協會昨日執行民眾失聯協尋任務,2名隊員王男與黃男於10時組隊騎乘水上摩托車
            下水後失聯16小時,今(25)日凌晨近2時許平安尋獲,兩員自行走到海巡署第四岸巡隊隊部
            報到,人員均無受傷,不須送醫,僅說只想回家休息。 海巡署第四岸巡隊22日獲報有一名
            74歲李姓老翁挖蛤蜊失蹤,隨即派遣搜救人員及通報雲林縣消防局支援找尋,雲林縣救難協會
            與紅十字會雲林水上救難隊獲知消息也投入人力協助尋找遇難者。雲林縣救難協會2名王男
            與黃男於約10時組隊騎乘一部水上摩托車穿著橘紅色上衣及救生衣、未攜帶無線電機具和
            手機便出海搜尋。 不料2人在24日下午15時仍未見返隊報到,研判可能遇上退潮擱淺或水車
            故障而受困失聯,經徹夜緊急增援搜尋,兩人在今(25)日凌晨約2時10分許,自行平安走到
            海巡署第四岸巡隊隊部報到,人員均無受傷,不須送醫,表示只想回家休息。 據了解,兩名
            失蹤人員執行協尋任務後,在濁水溪河口因摩托車故障,受困在河口的沙洲,因現場草叢密集
            ,搜尋人員才未發現,該處距離泊地逾4公里遠,兩人將摩托車暫時放置在安全的灘地,再
            自行沿著灘地慢慢走回泊地,搜救人員一發現,隨即將兩人送回岸上,兩人未受傷只是長時間
            涉水步行、游水,顯得疲憊。 平安返隊王、黃兩人表示,非常感謝雲林縣救難協會的隊員們,
            不好意思讓各位隊員們膽心,因一時疏乎開水車出任務忘了帶手機、對講機出勤而造成失聯,
            真的很抱歉,希望這是最後一次,給各位隊員們做個借鏡,不可再犯同樣的事情,再次由衷
            感謝也辛苦大家了。 其中黃姓隊員是水林鄉灣西村長黃常,已擔任32年村長的他熱心公益,
            樂善好施鐵漢柔情,為無血緣關係的獨居老人備三餐換尿布、隨傳隨到溫柔至極,將村民視為
            家人,受到許多村民依賴,昨是一度失蹤失聯,消息傳回村里無不為他擔心祈禱,所幸最後
            平安歸來,黃常說,真的非常不好意思,急著想救人,卻讓大家擔心,未來不會再發生這種
            狀況了。
            '''
        ),
    )
    assert parsed_news.category == '社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1624581060
    assert parsed_news.reporter == '蔡佩旻'
    assert parsed_news.title == '雲林「2救難員」找到了 失蹤16小時上岸:忘記這事很抱歉'
    assert parsed_news.url_pattern == '2015254'
