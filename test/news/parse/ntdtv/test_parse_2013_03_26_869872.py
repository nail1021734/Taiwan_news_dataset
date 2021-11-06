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
    url = r'https://www.ntdtv.com/b5/2013/03/26/a869872.html'
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
            湖南上千名軍轉幹再次遊行到長沙省委信訪局陳情,要求省委和省政府落實他們被剝奪的
            “一身份、兩待遇”。 星期二上午,大約上千名從排級到副師級的軍轉幹部,冒雨從
            長沙市軍轉幹培訓中心出發,步行大約3公里來到省委信訪中心,要求省委和省政府落實
            他們的“幹部身份,政治和生活待遇”(“一身份、兩待遇”)問題。 軍轉幹陳情近10年 問題
            仍未解決 軍轉幹王季雲説:“(身份就是)國家幹部身份,待遇就是政治待遇和生活待遇
            。(政府)不是沒有落實,而是剝奪了我們的身份。幹部都作為工人退休了。我們的訴求就
            主要是這兩個方面。” 從2004年開始,湖南的軍轉幹以大規模的陳情行動,提出恢復他們被
            剝奪的“一身份、兩待遇”的政治訴求,但是,他們每一次的陳情,問題都得不到解決
            。湖南省委有關部門告訴他們,軍轉幹問題,是一個全國問題,需要中央統一下發文件,
            省政府才能落實和執行。 昔日軍官幹部 今朝社會底層 在中國,凡是在軍中服役過的
            排級以上軍人,在退役、轉業到地方企事業單位後,可按有關規定享受幹部身份,以及與
            軍中對應的政治和生活待遇。但是中國的經濟改革打破了國企的鐵飯碗,一些軍轉幹和
            其他人一樣下崗或失業,生活面臨困難。 為了解決一些軍轉幹人員的生活困難,中國政府
            2002年和2003年相繼下發了82號和29號文件,規定以當地企業最低的平均工資水準,
            發放給那些下崗或失業的軍轉幹人員。不過,陳情的軍轉幹人員對此並不認同。 有了
            幹部身份 就有了一切 軍轉幹人員劉偉巨説,部隊幹部有包括兵役法,國防法,現役軍官法
            等四部法律保護他們的身份。但是,他們的轉業到地方企業後,幹部身份被剝奪後,也因此
            就喪失了政治待遇和經濟待遇。他説,只有給他們落實了幹部身份,才能繼續享受政治和
            經濟待遇。 他説:“我們都是一些老同志了,遇到了很多生活上的困難,卻得不到解決。
            我們的訴求就是要解決身份問題。解決身份才能夠解決一切問題。” 這次的軍轉幹人員
            陳情過程中,沿路除了一些警察維持秩序外,遊行和陳情在和平的氛圍中進行。 與對待
            一般市民陳情不同,長沙政府部門沒有對陳情的軍轉幹人員採取打壓,或拘留帶頭“鬧事者”
            ,而是由信訪局長親自出面接待,聽取他們的訴求。在中午時分,政府有關部門還向這些
            陳情人員提供了快餐食品。 劉偉巨説,他們這些軍轉幹希望以習近平為首的新一代領導人
            能聽到他們的訴求,從政策面解決他們的問題。 截止到發稿時,數百名軍轉幹還在
            省信訪辦大廳裏,等候向省委主要領導人表達他們的“一身份、兩待遇”的訴求。
            '''
        ),
    )
    assert parsed_news.category == '大陸專題,中國人權'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1364227200
    assert parsed_news.reporter is None
    assert parsed_news.title == '湖南上千軍轉幹陳情求待遇'
    assert parsed_news.url_pattern == '2013-03-26-869872'
