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
    url = r'https://www.ntdtv.com/b5/2013/08/19/a951813.html'
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
            埃及政府公布的資料顯示,8月14號對抗議者的清場過程中造成638人死亡,4千多人受傷。
            而目前埃及的動盪更是延續到了全國,全世界都在關注埃及的發展。有人把埃及軍方的
            行動比作是「六四」翻版,那麼,二者能進行模擬嗎?請看報導。 埃及前總統穆爾西被
            趕下臺後,穆斯林兄弟會和他們的支持者一直抗議,要求穆爾西複職。14號,埃及官方清除
            穆斯林兄弟會示威者佔據的兩個場地過程中,造成數百人死亡。 根據埃及衛生部公布的
            數字,從16號以後的暴力衝突中,又有近2百人傷亡。 埃及駐美國大使陶菲克
            (Mohamed Tawfik)接受美國《外交政策》期刊的採訪,他認為,將埃及清場比作「六四」
            天安門屠殺完全不對。 陶菲克指出,中國沒有21家警局警察遭到襲擊,也沒有43名警察
            被殺,更沒有7座教堂被焚毀和警察被殺後遭虐屍。並且,他認為,大部分死傷是穆兄會襲擊
            平民、政府建築物和教堂時發生的。 美國中文雜誌《中國事務》總編輯伍凡:「表面上看,
            都死了人了,軍隊開槍了,但實質上,一個是北京軍方主動開槍,埃及軍方是被動開槍;並且兩方
            的訴求都不一樣:學生訴求是和平,而埃及的穆斯林兄弟會他們要求是推翻政府,要求
            暴動。」 時政評論家伍凡表示,應該用和平的方式解決衝突。 《變局策》作者
            李一平:「中共是一個國家政權對要求民主的、要求自由的老百姓、知識份子,對他們進行
            血腥鎮壓,在埃及所發生的事情,可以把它理解為兩種文化相互之間的衝突。」 曾經撰寫
            論述中國未來發展的《變局策》一書的作家李一平認為,衝突的原因是伊斯蘭原教旨主義者
            想通過民主消滅民主制度,而溫和的世俗教派和軍方則不同意。但他不認同暴力鎮壓的
            做法。 穆兄會首領穆爾西執政一年以來,伊斯蘭勢力在國會佔了多數,新憲法有把埃及
            變成伊斯蘭教國家的傾向,加上埃及經濟惡化,高達13%的失業率,2200萬人簽名要求
            穆爾西下臺。 旅美學者曹長青撰文指出,埃及軍方迎合民意而罷黜了穆爾西,是個
            正確決定,如果中東人口最多的國家——埃及成為「伊朗第二」,後果更不堪設想。 據
            英國《路透社》的引述,70%的埃及人反對穆斯林兄弟會。 憲政學者陳永苗:「穆斯林兄弟
            會實際上有點像希特勒的納粹黨。希特勒的納粹黨在憲政史上製造了一個
            很大的危機,就是它通過民主的手段實現憲政,而且實現獨裁和專政。實際上穆斯林兄弟會
            做法是非常像的。」 中共喉舌《環球時報》16號社評聲稱,這場流血衝突只能被當成
            埃及走向民主的「陣痛」,還警告,埃及要為此付出慘痛代價。 15號的文章更繼續
            宣揚「埃及清場悲劇再次驗證民主困境」的論調。 伍凡:「共產黨這些人他為甚麼
            不想想,他49年前,毛澤東、劉少奇、周恩來在當年反對蔣介石的時候,他們不也是喊
            民主嗎?他們把自己的話全忘得光光了。」 1943年7月4號,作為中共當時的
            機關報《新華日報》,發表了社論——《民主頌——獻給美國的獨立紀念日》,盛讚美國
            民主。文章肉麻的寫道:中國人對美國的好感,是發源於從美國國民性中發散出來的
            民主的風度,博大的心懷。 陳永苗則指出,民主化帶來的陣痛是舊的專制制度帶來的,就像
            生病的人要治病,打針吃藥都是痛苦的,而民主越成熟越穩定,越長治久安,相反專制
            只會帶來動盪、崩潰和內戰。
            '''
        ),
    )
    assert parsed_news.category == '大陸專題,六四事件'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1376841600
    assert parsed_news.reporter is None
    assert parsed_news.title == '埃及清場是中國六四翻版嗎?'
    assert parsed_news.url_pattern == '2013-08-19-951813'
