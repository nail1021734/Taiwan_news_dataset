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
    url = r'https://www.epochtimes.com/b5/19/2/1/n11017679.htm'
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
            儘管工資增長緩慢,油價下跌,房市疲軟,加拿大中央銀行對全國經濟形勢依然看好。央行高級
            副行長卡羅琳·威爾金斯(Carolyn Wilkins)本週四(1月31日)在多倫多發表講話時表示,
            加拿大經濟經過一番「曲折」(detour)後,預計將在第二季度出現增長。 加拿大統計局本週
            四公布的最新GDP數據顯示,全國經濟放緩,去年 11月份經濟萎縮了0.1%,工資增長率也低於
            央行預期。金融市場一直有人猜測今年加拿大經濟有可能出現衰退。但加拿大央行對這個猜測
            並不買帳。 威爾金斯說:「我們預計經過這次『曲折』後,經濟將會再次增長。」 威爾金斯
            刻意使用「曲折」這個詞 ,這是央行的一個新詞,意在強化他們對加拿大經濟總體樂觀的看法
            ,暗示加拿大經濟目前的疲軟是暫時的,為今年某個時刻提高利率做好鋪墊。 儘管央行對
            加拿大經濟看好,但對下一次利率的走勢方向和時機依然保持謹慎態度。威爾金斯表示增息和
            減息「兩個方向都存在風險」。 加拿大央行原計劃將關鍵利率提高到「中性利率」水平。
            所謂「中性利率」就是既不會使經濟升溫,也不會使經濟放緩的利息水平。與美聯儲一樣,
            加拿大央行擱置了這個計劃。也就是說目前央行利息水平依然有助於經濟增長。自2017年
            年中以來,央行已經五次提高關鍵利率,將其提高到1.75%,但自去年10月以來,提息的步伐
            暫時停下來。 據《環球郵報》報導,加拿大帝國商業銀行(CIBC)經濟學家羅伊斯·門德斯
            (Royce Mendes)表示,威爾金斯的評論表明,加拿大央行對經濟格局的看法比美聯儲更為
            樂觀。這可能意味著今年晚些時候將再次加息。 去年加拿大工資增長率約為2.5%。 威爾
            金斯說根據就業市場基本情況,工資年增長率應該約為3%。工資增長低於預期是央行暫緩加息
            的另一個原因,因為這意味著經濟仍然處於低迷狀態。威爾金斯承認,工資增長的速度沒有
            央行預期的那麼快。目前全國接近充分就業,失業率僅為5.6%,處於自20世紀70年代中期
            以來的最低水平。 加拿大皇家銀行(RBC)在本週分別的一份報告說,工作流失緩慢是工資
            增長緩慢的主要原因。 皇家銀行經濟學家內森·楊森(Nathan Janzen)表示,嬰兒潮可能
            不太願意在臨近退休年齡時轉換工作。 儘管如此,依然有跡象表明人們利用當前勞動力緊張
            的時機進行討價還價,這將推動工資增長。 皇家銀行和威爾金斯都預計今年工資增長將加速。
            '''
        ),
    )
    assert parsed_news.category == '加拿大,溫哥華,新聞,加拿大新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1548950400
    assert parsed_news.reporter == '曲深'
    assert parsed_news.title == '加央行看好經濟 預計二季度反彈'
    assert parsed_news.url_pattern == '19-2-1-11017679'
