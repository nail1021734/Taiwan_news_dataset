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
    url = r'https://star.ettoday.net/news/8565'
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
            英國「E奶女神」凱莉布魯克(Kelly Brook)參與演出《Heavy Metal》的劇照近日在
            網路上瘋狂留傳,她穿著一身黑色緊身皮衣,火辣的身材曲線一覽無疑,但皮衣設計不貼身
            加上她上圍豐滿,其中一張劇照側面角度更讓她有疑似露點的嫌疑。 凱莉布魯克在新片身穿
            皮革爆乳戰衣,手持雙槍的殺手造型相當吸睛,當然也不能因為皮衣遮住她的好身材,上圍
            還故意做不貼身設計,讓雙峰在她激戰移動的瞬間成為片中亮點。 網路上近日留傳
            凱莉布魯克的新片劇照,其中一張側身角度的照片更讓她有露點嫌疑,事實上,她曾在電影
            《3D食人魚》中全裸露3點,展露34E、25、35魔鬼曲線,畫面獲選「年度最佳裸戲」
            ,這次當然也不能因為貼身皮衣遮掉她的好身材。
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1322067000
    assert parsed_news.reporter == "林孝庭"
    assert parsed_news.title == '「E奶女神」凱莉布魯克爆E乳 劇照曝光見奶香四溢!'
    assert parsed_news.url_pattern == '8565'
