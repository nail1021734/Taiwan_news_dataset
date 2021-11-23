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
    url = r'https://www.epochtimes.com/b5/19/12/19/n11732179.htm'
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
            斯坦福大學胡佛研究所,為於明年2月對外公開蔣經國日記,特於12月17日(週二)中午舉辦
            「蔣經國:在台灣的年代及遺續」研討會,探討蔣經國前總統在台灣的政治生涯及貢獻,邀請
            多位重量級學者與談,美國前國務卿舒玆亦親自參加。 駐舊金山台北經濟文化辦事處處長
            馬鍾麟,應邀致詞時表示,蔣經國是台灣經濟現代化的推手,他在1970年代積極推動經濟改革
            及重大建設,締造台灣經濟奇蹟,使台灣名列亞洲四小龍,之後在一代又一代台灣人民的努力下
            ,使台灣成為繁榮蓬勃的科技重鎮。 馬鍾麟說,蔣經國在其執政晚年,亦回應了台灣人民對
            民主自由的渴望,解除了執行近四十年的戒嚴令,開放黨禁、報禁,並開放兩岸探親。由於
            蔣經國此項睿智,連同許多民主鬥士的持續努力,如今台灣已被自由之家、人權觀察和無國界
            記者組織等許多國際機構,評為世界上最自由、最民主的國家之一。 此外,馬處長亦稱許,
            蔣經國日記是一份珍貴的史料,對外公開將有助於各界了解蔣經國的內心世界,一窺他在面對
            重要歷史時刻,及重大政治變革時的深層思維,有助歷史學家了解當代的許多歷史議題。 胡佛
            所副所長兼檔案館館長沃金博士(Eric Wakin)則表示,胡佛所感謝在蔣家家屬及中華民國
            國史館的共同努力下,達成協議,同意胡佛所對全世界公開蔣經國日記,進一步推動相關學術
            之研究。 與會的國史館館長陳儀深亦表示,基於學術研究的價值,在不影響兩蔣日記所有權
            訴訟案的前提下,開放蔣經國日記,將有助海內外學界對當代歷史的研究。 胡佛所檔案館所藏
            的蔣經國日記,始於1937年5月,蔣經國自蘇聯返回中國,至1979年12月底,其中1948年日記
            佚失。檔案館目前閉館整修中,明年2月重新開館後,將比照蔣介石日記模式與規範,提供讀者
            複印本閱讀。
            '''
        ),
    )
    assert parsed_news.category == '美國,舊金山,灣區新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576684800
    assert parsed_news.reporter is None
    assert parsed_news.title == '2020年2月胡佛研究所將公開蔣經國日記'
    assert parsed_news.url_pattern == '19-12-19-11732179'
