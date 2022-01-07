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
    url = r'https://star.ettoday.net/news/1200278'
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
            美國與大陸角力步步進逼,中美貿易大戰已非單純的貿易戰,也不是一開始所稱的為了保護
            美國智慧財產權,與防止技術移轉的問題,反而已轉型成中美互爭全球科技領導地位大戰。
            川普的善變風格正消耗著美國的經濟與威望,加上美國已經退出TPP、巴黎氣候協定,這不僅
            宣告與亞洲盟國的關係將有所疏遠,也意味著亞洲經濟整合將趁勢崛起。慧眼看天下第11集
            邀請到台大政治系教授楊永明,與主持人黃寶慧深度分析中美角力下的全球新遊戲規則,將
            會產生什麼樣的影響。 阿爾及利亞遭控 將1.3萬難民驅逐至沙漠 歐洲難民問題日漸嚴重,
            各國一直都無法解決根本問題,而在北非的阿爾及利亞,是非洲難民前往歐洲的跳板之一,但
            阿爾及利亞卻被指控,過去14個月間將1.3萬難民趕到撒哈拉沙漠,其中還包括孕婦與孩童,
            而鄰近的利比亞也面對一樣的問題,只好祭出強硬措施防止偷渡客出海。 連續執政
            15年! 土耳其總統艾爾段連任成功 選情激烈的土耳其總統大選結果揭曉,由連續執政15年
            的現任總統艾爾段連任成功。由於此屆任期將正式進入總統制,行政上總統可以指派各部會
            首長,公布法律、發布命令不需副署,此外,總統一人即可宣布國家進入緊急狀態與解散國會,
            這也意味著艾爾段如願以償取得更大的總統實權。 「電玩成癮」者注意了! WHO正式列
            精神疾病 隨著3C普及化,放眼望去人手一台智慧型手機,網路、電玩的使用率高,不僅變成
            低頭族,有時候還會整天不做其他事,只想打電動,也因為狀況越來越嚴重,世界衛生組織WHO
            正式把電玩成癮列為精神疾病,也將通知各國政府,把電玩成癮納入醫療體系中。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530360000
    assert parsed_news.reporter is None
    assert parsed_news.title == '亞洲大崛起 國際政經新舞台'
    assert parsed_news.url_pattern == '1200278'
