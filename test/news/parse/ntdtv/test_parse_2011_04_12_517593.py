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
    url = r'https://www.ntdtv.com/b5/2011/04/12/a517593.html'
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
            芬蘭是一個民主共和國,她的議會是全體人民的代表,議會由200名議員組成,議會選舉每四年
            進行一次。今年四月十七日,全體芬蘭公民將用自己的選票選出新的議員代表自己說話。請看
            本臺記者來自芬蘭的報導。 今年春天是芬蘭議會換屆的時候。大街小巷,公車地鐵,到處都是
            候選者們的個人廣告。無論是聯合政府中的執政黨黨還是唱反調的在野黨,都走上街頭,走向
            媒體,使出渾身解數拉選票。 2007年選出的本屆聯合政府中的政黨包括芬蘭中間黨,國家
            聯盟黨,綠黨和瑞典民主黨。反對黨則是社會民主黨,左翼聯盟黨,基督教民主黨和真正
            芬蘭人黨。今年的競選中各黨在諸多問題如稅改問題,核電問題,財政支援葡萄牙,歐盟等問題
            上均有分歧。民粹黨“真正芬蘭人黨”異軍突起,他們以反對移民,要求廢除芬蘭第二官方語言
            瑞典語等政治立場著稱。 除了公開自己的政見,各黨還公開本黨的競選資金來源以及
            去向。 第一次投票已經於10號開始,有些公民包括芬蘭總統等都提前投了票。全國正式
            投票日是在下4月17日。新的議會成立後,他們將代表芬蘭人民選出下一屆芬蘭政府。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1302537600
    assert parsed_news.reporter == '施萍,高磊赫爾辛基'
    assert parsed_news.title == '芬蘭議會大選在即 各黨爭拉選票'
    assert parsed_news.url_pattern == '2011-04-12-517593'
