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
    url = r'https://www.epochtimes.com/b5/14/1/1/n4048468.htm'
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
            英國各地人們歡樂地迎來了全新的2014年。這一年將在英國歷史中成為重要的一年,因為
            蘇格蘭將在9月舉行全民公投,以決定是否繼續留在英國。首相卡梅倫在新年寄語中對
            蘇格蘭人表示「我們希望你們留下」。 卡梅倫在新年寄語中強調了9月18日蘇格蘭全民公投
            的重要性,表示它「對於我們所有的人都很重要」。他說:「今年,英格蘭、威爾士和北愛爾蘭
            對蘇格蘭的每個人想要表達的是:我們希望你們留下。」他說,這次全民公投不是事關未來
            幾年,而是可能永遠的改變英國,是蘇格蘭將會做出的最重要的一個決定。 蘇格蘭第一部長、
            民族黨領袖薩蒙德則在他的新年寄語中表達了完全相反的觀點。他表示,選擇獨立將會使一代
            人的母親享受到普及育兒服務,能夠重返工作,使蘇格蘭成為世界上最合適養家的
            國家。 卡梅倫還在新年寄語中再次強調經濟的重要性,承諾會使英國的經濟為勤奮工作的人
            帶來回報。他表示英國的經濟已經出現轉折,政府不僅將會堅持經濟計劃還會加倍努力實現
            所有的計劃。 他說:「我們將會繼續盡一切努力幫助勤奮工作的人,使他們在經濟上有安全感、
            削減收入稅收、凍結燃油稅。我們已經對福利封頂、削減移民,今年我們將會繼續為勤奮工作
            和遵守規則的人建設經濟。最後但同樣重要的是,我們將會繼續為孩子們和年輕人提供最好的
            學校和技術,這樣當他們畢業的時候將會有確實的機會開始人生。」 9月18日,蘇格蘭人將
            面對決定歷史的一天。所有年齡達到16歲或者以上的人需要回答「你是否同意蘇格蘭應該成為
            一個獨立的國家?」這個問題。1706年英格蘭和蘇格蘭簽署《聯合法案》,1707年蘇格蘭成為
            大不列顛王國的一部份。 2014年對於英國各主要政黨也將是重要的一年,因為2015年5月將
            舉行大選,這一年各黨派的表現將對大選中獲得的選票起決定性作用。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388505600
    assert parsed_news.reporter == '周成英國,馬千里'
    assert parsed_news.title == '英國首相新年寄語 希望蘇格蘭不要離開'
    assert parsed_news.url_pattern == '14-1-1-4048468'
