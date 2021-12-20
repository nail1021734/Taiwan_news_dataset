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
    url = r'https://star.ettoday.net/news/5210'
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
            富邦台北馬拉松即將於12月18日開跑,momo購物網與主辦單位富邦人壽本月7日起搶先推出
            公益衫義賣為路跑活動暖身,momo購物網獨家銷售1,000組,為公益團體募款。 momo購物網
            每年掀起搶購風潮的限量馬拉松公益衫義賣今年邁入第三年,公益衫一組4件1,000元,單件
            購買售價350元。共分為四個尺寸:S、M、L及兒童尺寸。今年限量僅1,000組,買公益衫即
            免運費宅配到家。歡迎邀家人、朋友、同事,4人揪團作伙加入愛心公益路跑,一起
            「4放你的愛」。 富邦臺北馬拉松公益衫義賣所得金額,將全數捐予「罕見疾病基金會」
            、「雅文兒童聽語文教基金會」、「愛盲文教基金會」,捐贈收據由三個公益團體直接開立
            給消費者。
            '''
        ),
    )
    assert parsed_news.category == '民生消費'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1320408900
    assert parsed_news.reporter == "盧姮倩"
    assert parsed_news.title == '「4」放你的愛 台北馬拉松公益衫義賣'
    assert parsed_news.url_pattern == '5210'
