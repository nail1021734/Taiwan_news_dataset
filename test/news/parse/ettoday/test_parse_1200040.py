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
    url = r'https://star.ettoday.net/news/1200040'
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
            加州19歲網紅蜜葵拉(Lil Miquela)在IG上擁有120萬粉絲,不僅熱愛流行文化,參加許多音
            樂節,她也關注時事,為黑人族群發聲,然而,她4月時坦承,「我不是人類,我是一個機器人。
            」事實上,她僅是由電腦軟體製成的虛擬人物,如今已引發部分消費者不滿。 據CNN報導,蜜
            葵拉的社交帳號在2016年推出後,受到越來越多粉絲力挺,可以看到她穿著Coach、巴黎世家
            等名牌,她總是綁著莉亞公主頭,臉上有著雀斑,還曾推薦髮型產品,讓她的秀髮更加柔順。
            但自從她的團隊公開承認她是虛擬人物後,有網友不禁質疑,既然不是真人,怎麼能有資格稱
            讚產品。 長相甜美的蜜葵拉由洛杉磯新創公司Brud設立,該企業致力於發展人工智慧與機
            器人,背後有幾家風險投資廠商支持。就像真實的部落客般,蜜葵拉也會推薦品牌,但這些貼
            文是否涉及業配,Brud拒絕回應。 對於部分網友的反彈聲浪,曾跟蜜葵拉合作貼文的尹安
            (Yoon Ahn)表示,許多IG上的模特兒也「進場維修」,藉著亮麗的外表來銷售物品,這跟
            蜜葵拉的行為沒什麼差別,「你在IG上看到多少東西是真實的?」 具有AI功能的營銷平台,
            Influential的執行長萊恩(Ryan Detert)也說,就像人體模特兒已經存在100年,都是
            為了宣傳美以及背後的理想,這跟蜜葵拉被設計出的想法一樣。 事實上,虛擬人物對一些公司
            特別有吸引力,因為正如蜜葵拉有團隊在操作,她不會像真人一樣犯罪或罵髒話。不過,
            哥倫比亞大學商學院的市場營銷學教授奧立佛(Olivier Toubia)則說,虛擬人物會讓
            消費者感到混淆,應該讓粉絲搞清楚,真實的界線到底在哪。 雪城大學紐豪斯學院的社交媒體
            教授珍妮佛(Jennifer Grygiel)也強調,蜜葵拉身為虛擬人物,但並未在頁面清楚註明,
            「當我長大時,至少我知道芭比是個娃娃。現在2年多了,可能有人,特別是青少年,會以為
            蜜葵拉是真人。」她說,合作的品牌必須公開、透明,才不會讓這名虛擬女孩被利用於人類的騙局中。
            '''
        ),
    )
    assert parsed_news.category == '新奇'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530087720
    assert parsed_news.reporter == '丁維瑀'
    assert parsed_news.title == '粉絲破百萬!19歲雀斑妹每天曬名牌 自爆「我不是人」'
    assert parsed_news.url_pattern == '1200040'
