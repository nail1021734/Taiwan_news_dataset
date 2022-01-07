r"""Positive case."""

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
    url = r'https://www.cna.com.tw/news/aipl/201812280150.aspx'
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
            花蓮縣政府與Discovery頻道合作拍攝「分秒必爭:花蓮震災救援剖析」紀實片,呈現如何
            透過現代科技輔助,將傷亡減最低,並指成功救援2大關鍵,在生命探測器和搜救犬。 花蓮縣
            政府今年7月提出「107年0206花蓮地震紀實節目拍攝與國際宣傳服務案」限制性招標,預算
            金額新台幣1300萬元,由Discovery傳播集團得標,製作完成
            「分秒必爭:花蓮震災救援剖析」一片,將於12月29日晚間9時首播。 上午記者會播出片段,
            邀請搜救隊及民間救難英雄到場分享經驗,並請來影片主題曲的主唱「四分衛」成員阿山和
            虎神。 影片中出現花蓮義消顏勝裕自發地開著怪手,趕往倒塌的統帥飯店加入搜救行列;
            開工程行的林信昌無條件投入上百萬H型鋼和重型機具主動參與救災。此外,影片也指出,
            成功救援2大關鍵,在於生命探測器和搜救犬。 救難專家在片中表示,如果受困建築物中,
            應放鬆情緒,以維持身體循環慢一點。一般國際上,緊急救援信號SOS為
            「滴滴滴、答-答-答、滴滴滴」三短三長三短,以這節奏敲出聲響,救難團隊便可知道是
            求救信號。 花蓮縣長徐榛蔚致詞說,花蓮是地震頻繁的地方,加上交通不便,很容易變成
            孤島。十分遺憾今年2月6日發生大地震造成傷亡。今年1月消防局成立縣內第一支特搜隊,
            在整個救援過程中發揮功能;更感謝許多單位前來協助救災。 Discovery內容發行部
            資深總監馬艷華致詞說,Discovery頻道擅長以紀實方式用鏡頭說故事,這次影片除探討
            花蓮震災救援的成功關鍵,也告訴觀眾重要的救難及防災應變知識,希望透過Discovery在
            全球的影響力能幫助到更多人。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1545926400
    assert parsed_news.reporter == '李先鳳花蓮縣'
    assert parsed_news.title == '花蓮地震救援行動 Discovery剖析成功2關鍵'
    assert parsed_news.url_pattern == '201812280150'
