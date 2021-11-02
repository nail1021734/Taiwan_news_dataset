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
    url = r'https://star.ettoday.net/news/1200478'
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
            HBO科幻美劇《西方極樂園》(Westworld)第二季已正式完結,最終集第十集
            「The Passenger」解釋不少這一季的問題,卻也留下諸多疑問。除了接近尾聲時揭露
            另一名臥底在人類之中的接待員,在跑完演職員名單後的片尾更讓劇情出現驚人轉折,為第三季
            埋下伏筆。 以下內容有《西方極樂園》第二季劇情 《西方極樂園》第二季最終集第十集
            片尾,黑衣人威廉進入熔爐(the Forge)看到的不是觀眾預期的伯納與迪樂芮,而是他的女兒
            艾蜜莉,兩人上演著第四集「獅身人面像之謎」(The Riddle of the Sphinx)中年輕威廉
            反覆測試詹姆斯狄洛斯的橋段。 主創之一的麗莎喬伊(Lisa Joy)向好萊塢報導者解析這段
            片尾,她說:「在遙遠的未來世界產生鉅變,呈現出殘破的景象。威廉死去女兒的形體現身對他
            說話,他發現自己已經陷入永無止境的迴圈。類似情景本季也出現過,每一次的重覆都在測試
            所謂的『真實性』或是偏差值。你明白這樣的測試將會一直持續下去,預告我們接下來會到
            另一個時間領域,我們會看見更多,他們如何到達那個地方,以及測試什麼。」 此前年輕威廉
            也屢次測試詹姆斯狄洛斯的「真實性」,檢視植入人類心智的接待員是否能和人類一樣正常
            運作,當時測試的結果不太順利。而片尾這一幕的威廉是否真的是接待員?若是的話他的開發
            版本已經接近成功了嗎? 麗莎喬伊表示:「這一幕的黑衣人不是他的原始化身,而是某個版本
            的黑衣人。說他是接待員不太公平,接待員是指迪樂芮那樣的造物,從零到有打造出來的純粹
            的認知。」 針對此議題,主創之一的強納森諾蘭向美國娛樂周刊透露:「他們明確地表示他們
            不在系統裡,我們也看見背景的殘骸,這的確暗示他們身處未來。我們常說我們想要探討地球
            新型態生命的起始、中間與結束,這一季很多東西的發展是以此為基礎。」 強納森諾蘭接著
            說:「這一季有個重大轉變,當你開始知道更多黑衣人的的背景故事,很多人應該會質疑...
            我們看到艾蜜莉的屍體、黑衣人身處危險邊緣但還沒死亡,我們探索了詹姆斯狄洛斯的重大
            錯誤-他生命中決定性的一刻作的抉擇...我們也看到熔爐的作用,你會想要回頭一看再看這些
            關鍵性的時刻。」(collider) 《西方極樂園》第三季已正式獲續訂,根據主創四月時受訪
            透露,很有可能2020年才會回歸。
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530097200
    assert parsed_news.reporter == 'DramaQueen電視迷'
    assert parsed_news.title == '《西方極樂園》第2季完結! 解密片尾驚人轉折'
    assert parsed_news.url_pattern == '1200478'
