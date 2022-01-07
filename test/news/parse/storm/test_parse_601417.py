import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.storm


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='風傳媒')
    url = r'https://www.storm.mg/article/601417?mode=whole'
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

    parsed_news = news.parse.storm.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            當台灣即將成為垃圾島的消息蔓延時,有一群人默默的以自身的力量,希望一點一滴的改變
            環境污染的現狀.「Story Wear 」一個以零廢棄及回饋在地理念的品牌,由七年級生與
            台灣街角裁縫師結合,新舊世代撞擊出燦爛火花,讓時尚增添溫暖. 你知道嗎?時尚產業是
            既石油產業後「全世界第二大」污染源.全台灣每年丟棄衣物約7萬2千噸,相當於每分鐘丟掉
            438件衣服.而至今仍有超過「1.7億兒童」在為時尚產業工作. Story Wear 創辦人說
            「走訪世界各地,台灣一直有一種很迷人的特質,就是台灣獨有的「台灣精神」賦予誠信、
            腳踏實地、吃苦耐勞、不忘初衷的韌性,而 Story Wear 就是創始於這樣的精神而來. 結合
            傳統在地裁縫師、結合升級再造設計、落實循環經濟、社會企業,三個元素結合「這是
            新世代的台灣精神」 Story Wear 商品全部以回收衣物、布料製作,而生產線堅持跟
            在地裁縫師、非營利組織合作,「一件衣服得來不容易」一個惜物的概念是品牌希望推廣給
            消費者的理念. 生產線其中一位裁縫師--秀惠說:「可能上輩子我太不愛讀書了,這輩子老天
            爺要我好好再讀一次書」秀惠的孩子是腦性麻痺的身障兒,從上學的第一天,媽媽就需要陪著
            兒子讀書,從翻課本、抄筆記等,你跟我認為平凡的動作,在他們身上顯得不簡單.因為需要陪
            伴孩子,秀惠無法正常上班,於是練就了一手非常好的縫紉工藝,而製作有質感的商品帶給她不
            只是經濟上的支援、更是一種成就感、一個喘息的機會. 製作 Story Wear 的裁縫師中,
            有中高齡失業、二度就業困難、街角裁縫師,因為世代的轉變,反而成為被社會忽略的一群人
            ,他們的豐富經驗、熟練工法,締造了過去的台灣,更能成就現在的社會. Story Wear 每一
            個商品上都有一個專屬的 ID ,透明公開的告知原料、生產單位、甚至裁縫師的手工簽名.
            而因為原料來源不同,每一個商品都是獨一物二的產物.如果你看到縫紉師欄位上簽署著一個
            「mycpboy」,這就是我們可愛的秀惠製作的包包,而「CP」代表著腦性麻痺
            的意思 Story Wear 不是一個傳統的服飾品牌,我們以零廢棄的概念,每一件商品都是客人
            下訂單後才開始製作,如此不會枉費製作人的心血、更不會造成垃圾.讓時尚多一點溫暖
            ,讓製造者說出他們的故事,讓你瞭解妳購買商品賦予的意義.每一件商品製作時,便回饋
            著需要幫助的人,而帶給這些婦女們不只是經濟上的支柱,那般自信是無價的。
            '''
        ),
    )
    assert parsed_news.category == '品味生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1541446500
    assert parsed_news.reporter == '上晴Talk編'
    assert parsed_news.title == '零廢棄時尚的溫暖 蔓延著台灣每個角落'
    assert parsed_news.url_pattern == '601417'
