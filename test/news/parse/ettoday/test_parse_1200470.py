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
    url = r'https://star.ettoday.net/news/1200470'
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
            台灣人對於羊肉的初步印象,應該都是在羊肉爐或是炒羊肉等等台式料理,但對於外國人來
            說,羊肉本身具有相當高的營養價值,而且料理的方式很多元,屬於相當高檔的美食。 《美
            國肉協》將美國超鑽級羊肉自2017年引進台灣,以純天然養殖無施打賀爾蒙的方式,經過有
            機飼育的方式,創造出肉質鮮嫩多汁無羶腥味的特色羊肉,讓許多饕客們趨之若鶩! 但因為
            產量少出口也僅1%的稀少數量,所以想在台灣品嚐真是難上加難。不過,如今已經能在台北
            美福飯店能享用到這項美食,特別邀請來自義大利的名廚採用米蘭羅馬的傳統料理手法,將
            美國超鑽級羊肉料理成獨一無二的「雙味美國法式羊排」,令挑剔的味蕾得到最大的
            滿足! 用餐的地點在台北美福飯店的GMT義法餐廳,參與活動的美食家相當地多,本身用餐環境
            極佳而且料理手法一流,在此除了義式的雙味羊排套餐之外,還有日式的乾煎羊小排套餐與中式
            料理的孜然羊肋排套餐,讓喜愛羊肉美饌的朋友,可以嚐到不同風味與部份的羊肉料理。 開
            放式的廚房令人印象深刻,它讓來此用餐的食客可以清楚地看見廚師們製作料理的作業流程
            ,而且也能觀察到料理環境的乾淨程度,讓人很享受等待上菜前的過程。 當日Wisely嚐到的
            是GMT義法餐廳推出的雙味義式羊排套餐,從前菜、主菜到甜點等等,每項都是令人嚐過後回
            味無窮的料理,嚐過之後真的是充滿幸福感! 一開始,品嚐的是餐前麵包佐橄欖油醋醬,兩種
            不同的麵包口味香氣特有特色,沾著醬料品嚐更有味道,並且讓人更加開胃! 其特色在於將
            油炸的義大利麵,包住52度低溫真空烹調兩小時的羊肉包在裡頭,再以青蔬香料等做精細的
            擺盤,讓視覺感受上更加滿足~實際品嚐後,酥脆的麵衣與香軟的羊肉相互幫襯,而獨特的肉
            汁也是獨樹一格。 最先品嚐的,是以羅馬傳統料理的戰斧牛料理方式,將迷迭香與蒜頭將羊
            排調味後,再慢火香煎處理,最後加入白酒提升香氣。 品嚐時,軟嫩的羊肉一刀劃開,其微微
            粉紅的七分熟是最佳的品饌,豐厚的肉汁鎖在裡頭,沾著白酒醬汁更是令人讚不絕口;無羊膻
            味的羊排十分香甜,而且口感軟嫩,每一口都有不同的感受,是品嚐過之後還會念念不忘的美
            味。 另一項是採用米蘭炸牛排的手法,先將羊排肉裹上麵包粉去油炸,讓羊肉的味道經過高
            溫處理後呈現更加香甜的滋味,酥脆的麵衣讓肉汁變的更加好吃,而且沾著芥末醬品嚐,不僅
            是去除多餘的油膩滋味,也豐富了羊排肉的味道! 飯後的甜點是GMT特製的提拉米蘇佐鮮果
            粒,其具有咖啡香氣的滋味,配上溫潤的香甜可可,還有酸甜的果粒相互結合,讓飯後的味蕾
            有個很棒的結尾。 飲料的部份我和朋友挑選了冰熱皆宜的拿鐵,搭配著提拉米蘇品嚐相當
            地合拍! 品嚐美味的「美國超鑽級羊肉」料理之後,讓我對於羊肉的滋味有著不同的改觀評
            價! 營養的羊肉好吃而且熱量又低,本身含有豐富的omega-3脂肪酸和α亞麻油酸,其含量甚
            至超過同份量牛肉的五倍。並且,嚴格品管及提供多樣天然食物的的飼養方式,讓食用者可
            以更加安心地大快朵頤,也是愛好美食的朋友,絕對不可錯過的美味選擇。 Wisely 一個記
            錄美食、旅遊與生活的雙魚男, 喜歡在平凡的日子裡去寫下生命中的點點滴滴。 總是嚮往
            著許多人們豐富精彩的故事, 所以也很認真地在網誌裡留下自己的生活點滴, 讓生命裡曾
            經歷和摸索過的足跡,不止存在於腦海裡。
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530176400
    assert parsed_news.reporter is None
    assert parsed_news.title == '無羶腥味又多汁!台北美福飯店吃得到美國超鑽級羊肉'
    assert parsed_news.url_pattern == '1200470'
