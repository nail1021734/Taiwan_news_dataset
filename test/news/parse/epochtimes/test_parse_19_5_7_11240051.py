import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/19/5/7/n11240051.htm'
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

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            近日,紐約州奧伯尼市市長凱西‧施翰(Kathy M. Sheehan)宣布2019年5月13日為奧伯尼
            市「世界法輪大法日」。 褒獎令譯文如下: 紐約州奧伯尼市市長辦公室褒獎令鑒於,2019年
            5月13日,約一萬人將從世界各地聚集紐約市慶祝世界法輪大法日,暨這一全球最受歡迎的打坐
            修煉方法洪傳二十七周年;並且 鑒於,自1992年,全世界一億多人通過修煉法輪大法,變得
            更加健康、快樂、利他。世界法輪大法日是對這一偉大修煉方法造福社會的肯定;並且 鑒於,
            法輪功,也稱法輪大法,是由五套功法組成的祥和的靈修方法。其修煉者在日常生活中遵循
            「真、善、忍」原則;並且 鑒於,法輪大法根植於古老中國傳統文化,由李洪志先生創立並於
            1992年在中國公開傳出。口耳相傳,數千萬民眾通過修煉,身心受益極大。今天,世界上有
            一百多個國家、不同年齡、不同背景的民眾修煉法輪功。法輪大法一直是義工免費教功,既
            可以自己煉功,也可以集體煉功;並且 鑒於,全世界法輪大法修煉者投入無數小時,致力於組織
            社區免費教功班、推廣中國音樂、舞蹈文化並參加社區活動。他們同時還致力於和平制止在
            中國對法輪功的迫害,為世界人口最多的國家帶來美好的未來;並且 鑒於,所有這些和更多
            原因,李洪志先生曾四次獲得諾貝爾和平獎提名。 鑒於此,我,施翰(Kathy M. Sheehan),
            紐約州奧伯尼市市長宣布:星期一,2019年5月13日為奧伯尼市 「世界法輪大法日」我懇請
            奧伯尼市居民和我一起,肯定這一和平的靈修方法,祝願所有法輪大法修煉者世界法輪大法日
            快樂,生活健康愉悅。 作為憑證,在2019年3月20日我親筆簽名如下
            , Kathy M. Sheehan 市長
            '''
        ),
    )
    assert parsed_news.category is None
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1557158400
    assert parsed_news.reporter is None
    assert parsed_news.title == '紐約州奧伯尼市長宣布5月13日法輪大法日'
    assert parsed_news.url_pattern == '19-5-7-11240051'
