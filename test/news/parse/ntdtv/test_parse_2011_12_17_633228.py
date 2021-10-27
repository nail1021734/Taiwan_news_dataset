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
    url = r'https://www.ntdtv.com/b5/2011/12/17/a633228.html'
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
            中國駐洛杉磯總領事館在當地時間星期五下午驚傳槍擊事件。據館方和警方對外發布僅有
            信息可知,一名65歲亞裔男子從車上朝著中領館大門連開數槍,隨即向警方繳槍自首,駐館
            人員無人傷亡。 駐洛中領館遭遇槍擊後,直到當地15日深夜,當地媒體從駐洛中領館和當地
            警局所得到信息仍相當有限。 根據警方提供書面材料,下午2點15分,一名65歲亞裔男子朝著
            駐洛中領館開槍,嫌犯已向警方繳槍自首。 案發後第一時間趕赴現場了解情況的僑界人士
            表示:「目擊者即是中領館的警衛,警衛說開槍的那名男子曾經在中領館前抗議,帶來抗議
            布條寫的是英文,警方不對外透露這名男子究竟是哪一族裔,也沒有說明嫌犯是否為
            華裔。」 這起槍擊案的消息在晚上六點過後傳遍當地,並震動華裔社區。從網上得知消息,
            趕往駐洛中領館察看的僑界人士進一步說,到了現場,館方已升高警戒,也拉起封鎖線,無法
            看出館方建築受損程度。 她說:「現場整個被封鎖,媒體記者在那裏苦等,中領館館方在
            第一時間也未說明到底發生何事。警方則說開槍的嫌犯是一名65歲男子,駕車來到中領館前,
            對著領館開十幾槍之後,就駕車離開現場,他連開了很多槍。」 案發之後,曾與館方取得聯系
            的媒體工作人員則說,館方對外說明的口徑一致,語多保留,僅強調已按照程序通報警方和
            美國涉外單位,駐館人員受到驚嚇,但全數平安。 媒體工作者絲汀.江說:「中領館特別強調,
            雖然發生槍擊事件,但館內並無人員受傷,全數安全。他們希望借此事件突顯外館維安之必要,
            希望美方給予進一步保護,也希望不要再發生類似事件。」
            '''
        ),
    )
    assert parsed_news.category == '國際,時政'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1324051200
    assert parsed_news.reporter is None
    assert parsed_news.title == '駐洛杉磯中領館遭槍擊 亞裔嫌犯案後繳槍自首'
    assert parsed_news.url_pattern == '2011-12-17-633228'
