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
    url = r'https://www.epochtimes.com/b5/19/12/23/n11739348.htm'
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
            《新聞拍案驚奇》獲授權獨家首發:《願榮光歸香港》全新台語歌詞、CSM重唱團「六重唱」
            台語演唱,台灣知名「音樂製作人J」台北錄製! 台語歌詞: 啥事這土地目屎流? 奈何咱眾
            人攏悲恨? 城門攑起頭,列邦聲喧透, 望自由歸佇咱兜。 啥事這驚惶趕袂走? 怎樣為信念
            攏無退後? 雖罔血咧流,前進聲愈響透。 守民主光照香港! 佇星辰墜落絕望暗暝, 雺霧中,
            遠遠遐傳來哨角聲: 「為自由!同齊來出聲! 全力來拍拚! 勇氣、智慧,永遠無煞!」 黎明
            來到,欲光復咱香港。 眾人兒女,為正義時代革命, 懇求民主佮自由,萬世久長流, 我願榮光
            歸香港。 懇求民主佮自由,萬世久長流, 我願榮光歸香港。
            '''
        ),
    )
    assert parsed_news.category == '新聞拍案驚奇'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577030400
    assert parsed_news.reporter is None
    assert parsed_news.title == '《願榮光歸香港》全新台語歌詞'
    assert parsed_news.url_pattern == '19-12-23-11739348'
