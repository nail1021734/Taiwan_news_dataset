import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.ntdtv
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2012/01/01/a640045.html'
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
            日本東京鐵塔旁的增上寺是跨年好去處,寺前廣場除夕夜倒數時3000個環保氣球齊放,同時
            大梵鐘和誦經聲響起,充滿日式年味。海內外人士在內,初步估計約4萬人湧進。 2011年
            除夕夜晚上,增上寺開始發放3000個用糯米材質製作的氣球,這種氣球昇到上空遇水氣就
            融化,很環保。有幸拿到氣球的人,可用寺方發的許願卡寫下新年心願。 增上寺廣場聚集了
            4萬多人,大家望著寺後方的東京鐵塔散發出橘色或鑽石紗光雕,隨著倒數時間的逼近,閃光
            爍力道更強。 當女主持人宣布凌晨12點前30秒時,民眾顯得很興奮,最後齊喊5、4、3、2
            、1,頓時氣球齊飛、大梵鐘和誦經聲響起,東京鐵塔的展望台電子光板數字由2011轉為2012,
            高喊「新年快樂」的聲音此起彼落。 日本人過年,寺廟會發出撞鐘聲,聲響次數與象徵人類
            有108種煩惱的數字一樣,撞鐘表示祈求煩惱盡消,以清心迎接新年。增上寺的大鐘1次由4人
            敲,今年共有432人上鐘樓敲鐘。 另外,很多民眾將舊物拿來委託寺方焚燒處理,這稱為
            「淨焚」,可隨民眾心意付費。 遊客還爭相購買小龍吉祥物,木製的「不倒龍」、守護矢、
            護身符等賣況好。很多遊客在倒數之後,還湧進大殿進行新年的第一道參拜。 一位穿和服
            的女生表示,希望新的一年日本民眾尤其是東北災區的民眾能幸福。穿著連身青龍裝搞笑的
            男子山本憲志則說,希望新年是個運氣如龍翔的好年。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325347200
    assert parsed_news.reporter is None
    assert parsed_news.title == '迎新年 日增上寺3000氣球齊飛'
    assert parsed_news.url_pattern == '2012-01-01-640045'
