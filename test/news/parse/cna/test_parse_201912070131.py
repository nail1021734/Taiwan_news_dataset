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
    url = r'https://www.cna.com.tw/news/aipl/201912070131.aspx'
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
            由義大利神父羅德信1968年撰寫「澎湖:風和沙之島」遊記叢書,被鎖在羅東聖母醫院史蹟館
            半世紀後,澎湖縣文化局今天辦理中文版新書發表,讓民眾從中回憶50年前的
            澎湖風情。 新書發表會今天在文化局圖書館新知講堂舉行。澎湖文化局長王國裕表示,
            「澎湖:風和沙之島」一書,由當時負責澎湖天主教的神父羅德信(Antonio Crotti)
            在從事宣教時所寫,1968年於義大利出版。這次是因天主教惠民醫院長陳仁勇在宜蘭羅東聖母
            醫院服務時意外發現,擔心書中澎湖的故事隨時間流逝而遺忘,洽詢澎湖文化局促成譯成
            中文版發行。 王國裕表示,全書可說是羅神父在澎湖服務所見所聞的遊記,記載澎湖40、50
            年代的事物,迄今變成了一部珍貴的歷史,深具歷史文化的意義與價值。今天發表會中
            也致贈與會者人手一冊。 陳仁勇出席新書發表會表示,「澎湖:風和沙之島」透過輔仁大學
            義大利文學系廖心慈等協助翻譯與澎湖許玉河老師等人校閱後出版,是澎湖第一本由義大利
            文譯的叢書。 陳仁勇認為,羅德信等5名傳教士,在民國41年(1952年)由於共產黨迫害當時
            在中國的外籍傳教士,因而輾轉來到台灣,並選擇宜蘭和澎湖落腳,也印證天主教惠民醫院在
            這2縣市偏鄉服務當地民眾。 陳仁勇說,在澎湖服務長達18年的羅神父對於澎湖的印象是
            「那裡風很大、沙很多、但充滿著希望」;書中提到「我的心留在過去傳教過的地方,包括
            在台灣、雲南、泰國、印度和馬達加斯加,但大部份都在澎湖」,可見對澎湖有著
            深厚的感情。 陳仁勇表示,羅神父對歷史有獨特的見解,他認為300多年來朝代輪替對
            台澎歷史的影響,澎湖確有其存在、戰略與國際化的意義,按當時的說法「誰擁有澎湖,
            就擁有台灣」。 依文化局資料,羅神父1915年生於義大利聖馬丁諾,25歲晉鐸為神父,
            31歲帶6名靈醫會士到中國雲南宣教,38年因共產黨迫害在中國的外籍傳教士,而輾轉來到
            台灣,1987年病逝,享年72歲。 羅神父可說是惠民醫院和馬公天主教堂的創建者,在書中
            看到作者描寫靈醫會在澎湖從事許多社區建設,例如協助碼頭、防波堤建設,在各村落成立
            巡迴醫療站和幼稚園,甚至幫助蓋了惠民新村、惠民二村給離島的貧民。 羅神父學的是歷史,
            在二戰期間曾被分派到羅馬協助聖嘉民歷史的撰寫。這樣的背景,使他不只積極參與
            社區活動,也想要徹底瞭解澎湖,他查閱文獻,詢問政府官員和各行各業的專家,也和漁民、
            販夫走卒深入攀談,甚至比許多澎湖人更瞭解澎湖。
            '''
        ),
    )
    assert parsed_news.category == '文化'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1575648000
    assert parsed_news.reporter == '澎湖縣'
    assert parsed_news.title == '風和沙之島 首部義大利版譯文遊記澎湖發行'
    assert parsed_news.url_pattern == '201912070131'
