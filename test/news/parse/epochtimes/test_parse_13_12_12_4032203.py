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
    url = r'https://www.epochtimes.com/b5/13/12/12/n4032203.htm'
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
            近年來,中國大量文獻資料透露,中國「文工團」女團員的重要功能之一,就
            是進中南海和中央首長「共舞」。 韓國媒體報導,落馬的朝鮮第二號人物張成澤和銀河管
            絃樂團女團員鬼混,是他的罪狀之一。朝鮮政府日前公佈撤除張成澤職務和開除出黨時,其
            中一項罪名是「與多名女性保持不正當關係並飲酒作樂」。 韓國報章引述消息靈通人士稱
            ,朝鮮當局所指的是「今年8月被處決的銀河管絃樂團女團員」。該報稱,在受朝鮮最高領導
            人金正恩指示重新開業的迎日飯店包廂裡,張成澤大辦宴會,過程中,銀河管絃樂團還過來助
            興。 報導說,還有傳聞,張成澤經常跟銀河管絃樂團女團員混在一起,從海外購買數百瓶香
            水送給她們做禮物。 據報導,張成澤與銀河管絃樂團有牽連一事,是在朝鮮人民保安部竊聽
            和暗訪拍攝色情錄影帶的銀河管絃樂團的過程中被爆出來的。當時團員曾說「李雪主(金正
            恩的夫人)以前也像我們這樣玩兒」。結果有9名團員被公開處決。 此外,據說張成澤在招
            聘職員的過程中還算命,深陷迷信,他也喜歡抽價值上千美元的最高級雪茄等,生活放蕩。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1386777600
    assert parsed_news.reporter == '李文慧'
    assert parsed_news.title == '中朝文工團異曲同工 傳張成澤與女團員鬼混'
    assert parsed_news.url_pattern == '13-12-12-4032203'
