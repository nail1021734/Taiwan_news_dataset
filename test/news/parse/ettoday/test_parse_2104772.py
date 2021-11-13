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
    url = r'https://star.ettoday.net/news/2104772'
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
            在哥倫比亞的馬格達萊納河邊,有著約80頭來自非洲的野生河馬,牠們是大毒梟艾斯科巴
            (Pablo Escobar)生前蓋的私人動物園裡所養的寵物後代,因此被當地人稱為
            「古柯鹼河馬」;近年來這些河馬快速繁殖,政府雖已著手對牠們採取絕育措施,但專家仍
            擔心,大量的河馬糞便會危害自然生態,並進而影響人類。 根據《衛報》報導,艾斯科巴
            生前透過特殊管道,非法引進了4隻非洲河馬,在他被哥倫比亞軍警擊斃之後,私人動物園
            轉交由政府管理,由於河馬的體型過大而難以運輸,因此被放生於原地,結果牠們展現了超強
            的生命力,從最初的4頭繁衍長大到超過80頭;而勢力越來越大的「古柯鹼河馬」們,
            漸漸的危害到了當地居民的安危,也破壞了自然環境,因此近期政府正對牠們進行消毒與
            絕育措施。 專家們認為,河馬糞便對於水中的含氧量有著負面的影響,不僅會危害魚類生態,
            最終可能影響到人類的健康,甚至藉由河馬將潛在的疾病傳染給人類;另一方面,廣泛遍布且
            沒有天敵的河馬,已成為了當地的外來入侵物種,應該積極對牠們進行化學閹割,
            哥倫比亞國立大學的生物學家恩里克·澤爾達·奧爾多涅斯(Enrique Zerda Ordóñez)
            也表示,「化學閹割是必經的過程,但要對體型龐大的河馬進行絕育並不是一件容易的事。」
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634637480
    assert parsed_news.reporter == '江珮妤'
    assert parsed_news.title == '4頭→80頭!「古柯鹼河馬」遭放生樂活南美洲狂繁衍 專家憂生態'
    assert parsed_news.url_pattern == '2104772'
