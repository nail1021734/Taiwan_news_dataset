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
    url = r'https://www.epochtimes.com/b5/14/1/1/n4047920.htm'
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
            在2014年元旦到來之際,英國各地數十萬民眾舉行派對,在音樂和滿天的煙花中迎來了
            新年。 在倫敦泰晤士河畔,當地居民和遊客觀賞了一場別具一格的新年焰火——人們不僅看到
            了美麗的焰火,而且還聞到了焰火中的果香。 在新年焰火施放期間,帶有蘋果、櫻桃味道的
            霧氣和帶有桃味的「雪花」或「氣泡」,飄落在5萬多狂歡者的身上,觀眾在大飽眼福之時,也
            體驗了嗅覺器官帶給人們的愉悅。 五萬多狂歡者的派對舉辦場地約有三個足球場那麼大,那裡
            的人們都可以聞到「雪花」的香味和感受到派對的熱烈氣氛。 泰晤士河兩岸擠滿了看煙花的
            10多萬觀眾。對那些無法感受「雪花」香味的沿岸觀眾來說,他們得到了彩色發光腕圈和7種
            不同味道的糖果作為補償。 在除夕夜晚上8時14分,蘇格蘭多個城市同時燃放煙花,標誌著
            蘇格蘭的迎新年活動開始。 在愛丁堡,當地的街頭慶祝活動吸引了8萬居民參加。 倫敦市長
            鮑裡斯·約翰遜說,觀賞世界上最精彩的焰火表演,是慶祝2013年和迎接新年的最好
            方式。 約翰遜在新年致辭中說,「我們向2013年道別,過去的一年對於倫敦和整個國家來說
            是令人振奮和值得懷念的一年。」 「讓我們繼續努力並且共同確保倫敦這個偉大的城市在
            未來成就輝煌。」 泰晤士河畔部分煙花是從英航「倫敦眼」觀光輪上發射。 今年在泰晤士
            河畔看煙花,人們不僅看到了美麗的焰火,而且還聞到了焰火中的「果香」。 在除夕夜晚上
            8時14分,蘇格蘭多個城市同時燃放煙花,標誌著蘇格蘭的迎新年活動開始。 北愛爾蘭首府
            貝爾法斯特市政廳的彩虹裝飾亮燈,威爾士首府卡地夫也燃放了煙花。在愛丁堡,當地的街頭
            慶祝活動吸引了8萬居民參加。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388505600
    assert parsed_news.reporter == '辛民'
    assert parsed_news.title == '英國迎來2014年新年:看焰火聞果香'
    assert parsed_news.url_pattern == '14-1-1-4047920'
