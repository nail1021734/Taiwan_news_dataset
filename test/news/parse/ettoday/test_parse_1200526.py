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
    url = r'https://star.ettoday.net/news/1200526'
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
            半小時後要跟主管報告業績?你該做的可能不是拚命翻資料,而是先去附近快走或騎自行車
            一圈。 《神經心理學(Neuropsychologia)》期刊一項研究指出,只要運動10分鐘,就能在
            短時間內增強腦力。 先前研究指出,長期、規律的身體活動能幫大腦更健康;也有研究說,
            運動20分鐘以上會對認知功能產生直接影響。加拿大西安大略大學神經科學教授希斯
            (Matthew Heath)率團隊測試14名健康年輕人,讓一組人坐下來看雜誌;另一組則用中
            等速度騎固定式腳踏車10分鐘。測試結果發現,自行車組的認知表現比運動前提高14%;坐著
            閱讀組則沒有差別。 研究團隊指出,現在還不知道這種「腦力爆發」可以持續多長時間(試
            驗是在運動後17分鐘內進行認知測試);也還需要進一步測試觀察,比這次對象更年長或更不
            健康的人做了短時間運動後,能獲得多少好處。不過有一點倒是可以大膽建議,希斯說:「如
            果想表現得讓人眼睛一亮,先走出門吧!」
            '''
        ),
    )
    assert parsed_news.category == '健康'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530142080
    assert parsed_news.reporter == '陳俊辰'
    assert parsed_news.title == '想變職場紅人?開會前先運動10分鐘'
    assert parsed_news.url_pattern == '1200526'
