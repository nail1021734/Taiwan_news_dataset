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
    url = r'https://star.ettoday.net/news/1200492'
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
            還記得《歌喉讚》中那位愛變魔術,最後愛上女孩艾蜜莉的憨傻男「班吉」嗎? 儘管看起來
            呆呆憨厚樣,但歌聲一出卻令人相當驚豔,本名班普拉特Ben Platt的他一家人都熱愛音樂劇
            ,但今天重點不在他,而是他的弟弟亨利普拉特Henry Platt。 他的弟弟最新和友人
            Gillian Gurney合作,重新演繹英國歌手詹姆士亞瑟James Arthur的歌曲
            〈You Deserve Better〉,兩人坐在階梯一彈一唱,渾厚的嗓音可是不輸老哥班,許多網友
            聽完後紛紛表示已被弟弟圈粉,認為普拉特一家實在太有天分,根本就可以直接出道了。 而
            不只弟弟亨利,就連班的大哥喬納普拉特Jonah Platt也是一名音樂劇演員,曾在2016年參演
            百老匯版《女巫前傳》,私下也常常PO出在家隨興演唱的影片,還是位絡腮鬍帥哥唷,來,
            追蹤請至↓ 最後當然還是要聽聽班的動人歌聲啦!
            '''
        ),
    )
    assert parsed_news.category == '民生消費'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530118380
    assert parsed_news.reporter is None
    assert parsed_news.title == '《歌喉讚》「班吉」哥哥弟弟都超會唱 聽完直接被圈粉'
    assert parsed_news.url_pattern == '1200492'
