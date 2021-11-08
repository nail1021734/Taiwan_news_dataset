import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2013/12/28/a1032509.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            土耳其政府受到腐敗醜聞打擊,這似乎是政治鬥爭的一部分。 醜聞曝光後,民眾走上
            伊斯坦布爾街頭抗議,要求總理辭職。近年來,很多土耳其人對過度的伊斯蘭化行動越來越
            憤怒,在今年夏天發生一系列抗議活動後,有關腐敗的指控重新點燃了民眾抗議。 這次腐敗
            指控導致幾十人被捕,包括兩名內閣成員的兒子,他們涉嫌在房地產交易中提取大量現金和
            黃金回扣。 土耳其總理埃爾多安這個星期撤銷了那2位部長和另外8名官員的職務,可是這個
            行動沒有阻止要求他辭職的呼聲,事實上,一位被撤職的部長說,埃爾多安也應該
            下臺。 土耳其政府解僱了包括伊斯坦布爾警察局長在內的數百名高級警官,因為他們
            參與反腐敗調查。這個做法進一步激起了民憤。 執政12年的埃爾多安總理說,警察的
            手段“極其骯臟”。他說,警官“濫用職權”,政府有權解僱他們。 這場爭議使得埃爾多安和
            他的一位前政治盟友之間的鬥爭公開化,深居簡出的伊斯蘭神職人員法土拉•葛蘭居住在美國
            的一所私宅中,據說,他對土耳其警察和檢察部門有著很大的影響。 星期四,警官拒絕執行
            一家法庭的命令,公訴人提出不滿,隨後被調離了案子。 土耳其共和國報安卡拉辦公室的
            烏特庫•卡克羅澤爾說,削弱土耳其政府和司法部門,會讓土耳其在國內外都受到
            傷害。卡克羅澤爾說:“作為歐盟成員國的候選國,土耳其曾保證要在各個領域遵守歐盟
            準則,最重要的準則之一,就是法治、維護自由和司法體制公正。” 土耳其爭取加入歐盟的
            要求被連年擱置,這個醜聞很可能讓土耳其的申請繼續被擱置。埃爾多安總理將很難修復他
            受損的威望,尤其是如果像某些人預測的那樣,他本身也捲入醜聞的話。
            '''
        ),
    )
    assert parsed_news.category == '國際,時政'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388160000
    assert parsed_news.reporter is None
    assert parsed_news.title == '土耳其爆腐敗醜聞 威脅政治經濟'
    assert parsed_news.url_pattern == '2013-12-28-1032509'
