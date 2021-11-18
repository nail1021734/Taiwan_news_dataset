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
    url = r'https://star.ettoday.net/news/2085868'
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
            喜愛南洋料理嗎?快來看看哪裡有好吃的河粉、蝦餅吧
            ! CHOPE CHOPE EATERY 台北市/信義區 連續兩年榮獲米其林餐盤
            推薦的新加坡創意料理餐廳!美祿恐龍由冰淇淋、美祿cream與巧克力布朗尼組合而成,
            整體味道偏甜,是新加坡的國民美食!也推薦金杯粿,將薄餅製成杯狀再依喜好加入佐料
            ! 鴻公公越南河粉 台南市/南區 鴻公公販售美式越南河粉,Q彈河粉搭配真材實料
            熬煮的蔬果大骨湯頭!總共有 7 種料跟 7 種湯頭可以選擇,叻沙、香茅、椰奶都有!怕吃
            老肉的人可以點生牛肉,在湯裡涮幾下就可以吃啦!小菜好吃又開胃,價錢也很親民哦
            ! 武鼎越豐越南麵食館 台北市/信義區 販售多種越式乾米粉、河粉、烤肉排飯等,
            越式料理走清爽、不辣路線,若想要吃點辣可點泰式酸辣湯頭!必吃越式火車頭河粉,火車頭
            就是所有料都有!牛肉丸、生牛肉片、熟牛肉、牛肚一次滿足,湯頭清甜,擠上檸檬後味道
            提升層次! 星馬廚房 新北市/板橋區 致理科大附近的平價星馬料理,店內餐點均
            不超過150元!必吃星馬參巴飯,經典辣味參巴醬搭配燒雞腿、其他配料與泰國米製成的
            薑黃飯!燒雞腿外皮微酥脆、肉質軟嫩!印度拉茶包裝上有小乳牛的圖樣,甜度較高剛好可以
            解辣! 小陳故事多 台中市/北區 販售源自馬來西亞的娘惹咖哩,老闆為了
            台灣人口味稍加調整成微辣!牛肋條咖哩飯跟雞腿肉咖哩飯的肉質都非常嫩且入味,幾乎
            一咬下就化開!再用奶油烤餅沾上咖哩醬口味很不錯!低消每人一份咖哩,僅供現場候位哦
            ! 面對面 FACE TO FACE NOODLE HOUSE 台北市/中山區 販售口味道地又平價
            馬來西亞料理!砂朥越叻沙、檳城炒粿條、乾撈老鼠粉都是很經典的大馬料理!麵條手工製作,
            Q度很高!老鼠粉的口感極似米苔目,第一次來可以嚐嚐!必喝三色奶茶,加入綠色的
            斑蘭葉糖漿,喝起來非常爽口解膩! LOWCA 勞咖 台中市/北區 販售早午餐、下午茶
            甜點等!南洋咖哩雞是一道偏前菜的餐點,⁣帶有椰漿香氣的南洋風咖哩,香料味十足!⁣酥脆的
            法國麵包片沾附著吃很搭!⁣勞咖燒肉蛋法國麵包的歐姆蛋軟嫩,西多酥奶奶由土司搭配奶酥、
            煉乳及奶油,甜甜的超好吃! 小翠越南美食阿嘉耕逃 屏東縣/恆春鎮 恆春必訪
            大份量平價越式料理!首推月亮蝦餅,現點現煎需等候 30 分鐘!蝦餅超厚超浮誇,外皮酥脆、
            內部的魚漿又香又Q!裡頭的蝦肉也很多!咖哩法國麵包的雞肉給得很大方、肉質香嫩,椰奶香
            咖哩搭上酥脆法國麵包非常完美! MAMAK檔 星馬料理 台北市/大安區 你想吃的
            南洋料理這裡幾乎都有!必吃辣死你媽仁當雞,將椰汁煮至收乾,味道濃郁道地!還有多人必點
            香酥塔餅,超高的塔餅光是上桌的氣勢就非常驚人,本身帶有甜味,沾著一旁醬汁吃又有不同
            風味! 池先生 KOPITIAM 台北市/中正區、大安區 台北知名馬來西亞料理餐廳,
            每道餐點都充滿著濃濃的大馬風味!米飯加入椰奶熬煮,有濃郁的椰香!炸雞皮薄脆、肉鮮嫩!
            叻沙麵的重口味湯頭帶點椰奶香,最後可以再來份烤加椰醬吐司,鹹甜的滋味非常涮嘴!
            '''
        ),
    )
    assert parsed_news.category == 'fashion'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1632821820
    assert parsed_news.reporter == 'MENU美食誌'
    assert parsed_news.title == '全台南洋料理TOP 10名單!恆春必吃超厚蝦餅、星馬參巴飯150元有找'
    assert parsed_news.url_pattern == '2085868'
