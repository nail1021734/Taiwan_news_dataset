import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201803060174.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            台北米其林指南發布前一週,米其林今率先公布榮獲「必比登推介」的美食餐廳,有36家店家
            及餐廳入選,其中10家來自夜市,包含陳董藥燉排骨、施老闆麻辣臭豆腐等。 「台北米其林
            指南」將於14日出刊,在出刊前一週,米其林官方今天率先公布「必比登推介」美食餐廳
            名單,「必比登推介」是米其林評審員頒給餐飲業者的一項殊榮,代表這些餐廳供應物超所值
            的美味佳餚。 在「必比登推介」的名單中,有5間餐館屬台式料理,分別為茂園、美麗餐廳、
            My灶、我家小廚房及雙月食品;另有8家牛肉麵入選,包含永康牛肉麵、牛店精燉牛肉麵、
            劉山東牛肉麵、林東芳牛肉麵、廖家牛肉麵、老山東牛肉家常麵店、建宏牛肉麵及擁有
            60多年歷史的清真中國牛肉麵食館。 此外,有10項是來自於台北夜市的街頭美食獲選,
            包含來自饒河夜市的陳董藥燉排骨、福州世祖胡椒餅、施老闆麻辣臭豆腐,南機場夜市、
            寧夏夜市、臨江街夜市也都各有2間入榜,觀光客最愛的士林夜市則只有海友十全
            排骨入榜。 米其林指南國際總監米高.艾利斯(Michael ELLIS)說,米其林指南的評審員
            深入挖掘台北美食各式各樣的風貌和精緻美味,其中也包含了當地的特色佳餚,例如牛肉麵、
            豬腳、花枝丸等等,全都是味美價廉的餐點。 他特別提到,這次夜市挑選出來的風味小吃
            則是包括了健康養生的麻油雞、豬肝、豬肚湯、雞雜滷味、海帶、鴨翅,還收錄了一間
            供應素食臭豆腐的店家,是台北人氣無敵的平民美食。 除了台式料理外,「必比登推介」
            的名單也選了江浙菜、上海菜、粵菜、北京菜等特色料理,包含台灣第一家四川素食餐廳
            祥和蔬食、江浙餐廳點水樓、上海菜鼎泰豐及點心類的阜杭豆漿等。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1520265600
    assert parsed_news.reporter == '吳欣紜、陳葦庭台北'
    assert parsed_news.title == '2018米其林必比登推薦美食 10家來自夜市'
    assert parsed_news.url_pattern == '201803060174'
