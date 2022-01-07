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
    url = r'https://www.epochtimes.com/b5/13/3/1/n3812338.htm'
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
            想學習新的語言,研究莎士比亞,探索浩瀚寰宇就非得搭飛機到國外留學嗎?如果
            你以為買iPad、iPhone或是iPod Touch純粹就是跟流行、耍時尚、打電動嗎?那就大錯特錯
            了,蘋果這些智慧裝置,只是提供一扇前往寶庫的大門,讓博學多聞不再是個夢想,
            因為 iTunes U 收錄超過 500,000 種免額外付費課程講座、影片、書籍與其他資源,涵蓋
            數千種主題,剛剛還宣布下載數突破十億次。 iTunes U 上集合了超過一千兩百所
            學院、大學及中小學, 包括美國史丹佛、耶魯、麻省理工學院、 英國牛津及加州柏克萊等
            名校共濟一堂,還有其他聲譽卓著的機構,例如紐約現代博物館、 市立圖書館等,目前已有
            超過二十五萬名學生下載使用這些免費課程,其中百分之六十是來自於美國以外的
            學生。 蘋果公司表示,iTunes U 有獨步業界的筆記功能,方便提綱挈領,而且作業
            井井有條。當觀看影片、聆聽上課錄音或閱讀書籍時,只要點按「加入附註」按鈕,即可開始
            鍵入你想記下的內容。 iTunes U app 會追蹤影音檔案或文字資料中留下的筆記,方便日後
            尋找或回憶課程內容。 用戶一旦選修 iTunes U 課程,系統還會主動跟催進度,上過的課程
            需要在完成後予以勾銷,講師會不定期發送訊息或指定新的作業,隨時注意你有沒有跟上,比
            緊迫盯人的助教還會纏人。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1362067200
    assert parsed_news.reporter == '江啟明'
    assert parsed_news.title == 'iTunes U 名校免費課程下載破十億次'
    assert parsed_news.url_pattern == '13-3-1-3812338'
