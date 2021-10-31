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
    url = r'https://star.ettoday.net/news/1200012'
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
            上海黃姓男子去年9月帶著于姓女子到賓館開房間,雖然兩人是婚外情關係,但他熱情邀請
            一起去吃晚餐,沒想到接連遭拒絕,房間都開了兩個小時卻連親熱都不行
            ,這才氣到直接在賓館走廊開打,導致對方肋骨斷了4、5根;後續的官司打到今年6月才能稍
            微喘一口氣,他一審則被依故意傷害罪判處有期徒刑9個月,緩刑1年。 影片中,只見黃男和
            于女在賓館走廊互相拉扯,他一氣之下先是甩了一巴掌,接著出拳毆打又用腳猛踹,過程中女
            方的高跟鞋掙扎到掉落,他乾脆撿起來當成「武器」,狠狠地朝頭部連擊4下,就算人已經倒
            地還縮在牆角,依舊不放過,扯住頭髮繼續痛揍。 事後,于女到醫院檢查發現肋骨被打斷4、
            5根,頭臉部更是多處挫傷。黃男坦言,當天兩人在賓館開房間,他先是邀請一起去吃晚餐,遭
            拒絕後只好自己一個人外出吃飯,回來時想發生性關係,結果親熱又遭拒絕,「如果一開始就
            要走幹麻開房?她自願開房都2小時了,我澡也洗了,說走就走不是耍我嗎?」 不過,黃男對於
            自己一氣之下動手暴打于女也感到很後悔,事發5天就主動向警方自首。上海徐匯法院今年6
            月做出一審判決,黃男除了必須賠償于女28萬人民幣(約130萬元台幣)的醫藥費外,還被依故
            意傷害罪判處有期徒刑9個月,緩刑1年。
            '''
        ),
    )
    assert parsed_news.category == '新奇'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530064800
    assert parsed_news.reporter is None
    assert parsed_news.title == '情婦同意開房拒親熱 人夫抓狂高跟鞋巴頭:我澡都洗了'
    assert parsed_news.url_pattern == '1200012'
