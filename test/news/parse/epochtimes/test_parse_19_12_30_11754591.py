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
    url = r'https://www.epochtimes.com/b5/19/12/30/n11754591.htm'
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
            三退聲明 我們現在認識到了,中共是現世最大的騙子,我們從前在它的洗腦中都沒有認清它。
            經過長時間的聽聞真相,再看眼下的現實,中共確實是一個實質的邪教黑幫。鎮壓所有不聽從
            它邪說的人,妄想把所有人都變成它的邪教徒,為它陪葬犧牲。我們現在認清了中共邪教的
            惡魔嘴臉,我們要掙脫它的控制,脫離它。為此特在這裡鄭重聲明:立即退出中共的少先隊,
            及所有與中共相關的組織 。做一個正直、善良的炎黃子孫。 退黨聲明 我已經不能再跟隨
            邪惡,我已經再不能依附邪惡;以前懵懂被迫的加入,今日我醒來;卻被它捆綁而無退處。在此
            申明:退出中國共產黨。 退隊 小的時候被加入少先隊,現在
            知道了共產黨是一個邪惡的組織,幾十年來幹盡了人神共憤的事情,中國人民被奴役著,人民
            怨聲載道都期盼著共產黨倒臺!我鄭重聲明退出少先隊!要洗淨這恥辱的印記。堅信天滅中共
            !!! 退團 退隊 太坑人了,家被拆,無處
            申冤!為了生活選擇工作還被抓進監獄,沒有房可住,微薄的退休金還是最低的雙軌制,都不敢
            得病,怕死不起! 退團隊聲明 年輕時不懂,加入
            了這個邪惡組織,現在明白了,它們沒有人性。現在我退出團、隊,和它們劃清界限,找回真實
            的自己。
            '''
        ),
    )
    assert parsed_news.category == '大陸新聞,社會萬象'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577635200
    assert parsed_news.reporter is None
    assert parsed_news.title == '每日三退聲明精選'
    assert parsed_news.url_pattern == '19-12-30-11754591'
