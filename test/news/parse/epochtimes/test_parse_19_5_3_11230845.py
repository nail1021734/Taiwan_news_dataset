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
    url = r'https://www.epochtimes.com/b5/19/5/3/n11230845.htm'
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
            暑期就要到來,位於新澤西的明慧學校將於6月24日到8月16日在該校開辦夏令營,精心設計
            各種文化課程並聘任專業教師執教,針對不同年齡段的學生,將文化和趣味結合起來,讓學生
            在輕鬆、愉悅的氛圍中學習中文及中華文化,並認識什麼是傳統的為人處事的理念和道義,提升
            品德和禮儀。 學習的內容從簡單易學的禮貌到良好生活習慣的養成;並以圖文並茂、音樂
            舞蹈、戲劇表演等孩子易接受的形式,將「仁、義、禮、智、信」的中華傳統道德理念,根植
            於孩子的心靈深處;通過各項團體活動,培養團隊精神及分享、奉獻精神,學習領導統御的能力
            。 同時,透過優美的詩詞、經典的古訓、動人心弦的故事,將堅韌、忠貞、自信、樂觀、豁達
            等品格,溶入孩子們的言行思維中,建立正確健康的人生觀和價值觀。尤令人期待的是,明慧
            學校特別邀請到世界一流國際藝術團的聲樂、舞蹈教師及國際器樂獲獎大師們,義務為夏令營
            的學生授課。 明慧學校校長張剛表示,明慧學校是非營利機構,以恢復和弘揚中華傳統道德
            文化為教育宗旨,面向整個社會群體,提供純正、美好的中華傳統文化學習平臺。學校在幫助
            學生學習中華傳統的漢字基礎上,進一步理解和承襲中華五千年的文化道德。學生在真正理解
            文化中的做人道義和品德後,自然會進行自我約束,做事考慮他人。這也正是美國主流社會的
            精神所在。明慧學校意欲在繼承和學習這些傳統文化的基礎上,結合美國主流社會的狀況,為
            學生未來融入美國主流,培養棟樑和精英。 夏令營招生對象:6~13歲學生,分初級、中級或
            高級班。 課程分:中華語言文化課、中華五千年歷史文化課、東西方禮儀文化課、東西方
            傳統藝術文化課和手工製作課等。 中華語言文化課——初級班有漢字基本功的學習:包括拼音
            、聲調、筆劃、筆順以及初級基本對話;中級班有漢字基本功的掌握訓練、中文閱讀能力訓練
            、寫日記及簡單敘事體文章的寫作培訓; 高級班有:流利、準確的中文表達能力訓練;詩歌、
            朗誦、演講訓練、成語、中文寫作練習等。 中華五千年歷史文化課——初級班:漢字的故事
            系列課程、中華傳統育人經典故事系列;中級班:中華傳統育人經典故事系列、中華五千年文化
            正史 ;高級班:中華五千年文化正史、中華五千年文化(古典詩、詞、名著解析欣賞)、中華
            五千年文化(著名歷史人物傳奇、故事)。 東西方禮儀文化課——基本生活自我料理、幼兒禮儀
            、學生禮儀;生活禮儀、社會禮儀初級。 東西方傳統藝術文化課——傳統繪畫、書法、工藝
            美術、中國古典舞基本功、聲樂、口琴。 手工製作課——木工課、簡單烹飪課;認知自然——
            種植課、觀察課、郊遊(騎馬、划船、農場、Street Fair、County Fair)。
            '''
        ),
    )
    assert parsed_news.category == '美國,紐約生活網,紐約新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1556812800
    assert parsed_news.reporter is None
    assert parsed_news.title == '明慧學校夏令營 開放報名'
    assert parsed_news.url_pattern == '19-5-3-11230845'
