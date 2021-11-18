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
    url = r'https://www.ntdtv.com/b5/2018/12/29/a102476332.html'
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
            中共官方28日公告,中共商務部副部長傅自應,被任命為北京政府駐澳門特別行政區聯絡
            辦公室主任,傅自應是中國國家副主席王岐山的舊部。其前任澳門中聯辦主任鄭曉松兩個月
            前墜亡,事件至今仍撲朔迷離。 根據中共人力資源和社會保障部12月28日在官網公告,
            中共商務部國際貿易談判代表、副部長傅自應,被任命為駐澳門特別行政區聯絡辦公室主任
            (澳門中聯辦主任)。 公開資料顯示,傅自應1957年9月出生於湖南嶽陽,長期在商務部
            (前身為對外經濟貿易部)工作。 2003年6月,傅自應任商務部規劃財務司司長,2003年7月
            任商務部部長助理、黨組成員,2008年3月首度出任商務部副部長、黨組成員。 2011年
            11月,傅自應出任江蘇省副省長、省政府黨組成員,2015年3月,轉任中共中央紀律檢查
            委員會駐中央宣傳部紀檢組組長。 2017年2月,傅自應再調回商務部,出任黨組副書記,
            同年3月起,出任商務部國際貿易談判代表(正部長級)兼副部長、黨組副書記。 傅自
            應被視為時任中紀委書記王岐山的人馬。傅於2015年任中紀委員駐中央宣傳部紀檢組組長。
            2016年11月還兼任第三巡視組組長帶隊對甘肅、廣西進行巡視。港媒報導說,傅自應曾助
            王岐山反腐「打虎」。 傅自應與已經落馬的前政治局委員薄熙來也有交集。 報導說,
            傅自應原是薄熙來的舊部,薄調離後數月,傅自應2008年3月升任中共商務部副部長。
            薄熙來因涉嫌政變等原因,2012年3月落馬後被判無期徒刑。 傅自應的前任、澳門
            中聯辦主任鄭曉松,於10月20日在澳門住所墮樓身亡。中共官方次日即宣布鄭曉松
            「抑鬱症自殺」,此說法引發外界普遍質疑。 隨後,有海外爆料者發布視頻稱,鄭曉松
            「實際上是被幹掉的」,並指此事件與中共前公安部副部長孟宏偉有關。孟宏偉是
            周永康舊部,已於10月上旬落馬。 爆料者還暗示,現任香港中聯辦主任王志民亦將出事。
            他還稱,「接下來很多人會跳樓、很多人自殺和被殺,特別是公檢法、中紀委」。 澳門
            自從1999年主權移交大陸後,已有5任中聯辦主任,其中過半命運不濟。 首任主任王啟人
            上任一年後,癌症複發病逝,終年60歲。 第三任主任李剛僅兩年,被傳因貪腐受查,2017年
            8月被免職,次月,中共人大網公布,李剛因涉嫌「嚴重違紀」,被責令辭去共人大代表
            職務。 第五任主任鄭曉松上任僅一年多便墜樓身亡。
            '''
        ),
    )
    assert parsed_news.category == '大陸,時政'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1546012800
    assert parsed_news.reporter == '李芸'
    assert parsed_news.title == '澳門中聯辦主任墜亡後 繼任者背景引關注'
    assert parsed_news.url_pattern == '2018-12-29-102476332'
