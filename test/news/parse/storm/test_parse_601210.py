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
    url = r'https://www.storm.mg/article/601210?mode=whole'
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
            看到民進黨一直在宣傳寶可夢為台灣帶來多少商機,比中客還有用等,真是令人搖頭,
            證明民進黨果然無能到了極點!其實寶可夢比中客還毒,民進黨還真當是當寶? 首先抓寶
            的人不是正常來消費的觀光客,這些人被稱為「喪屍」,因為他們不是被台灣所吸引來的,
            他們眼中只有寶物,可以24小時廢寢忘食地抓寶,完全不管交通規則以及他人安寧,不但
            帶來治安隱憂,也造成本地居民許多困擾。 此外,本地抓寶客就不提了,國外來台來抓寶以
            揹包客居多,這些人的消費能力令人質疑,除了吃喝拉撒的消費加上留下的垃圾,請問能拼多少
            經濟?民進黨政府估計一天1500元的消費,這跟中客低價團有差嗎? 何況台灣的經濟就靠
            天天抓寶?馬路上天天一群晝夜不分的喪屍,能看嗎?這樣不會反而嚇到正常的觀光客? 再來
            說中客,馬英九開放中客,被罵得最兇的就是中客的一條龍作業,從旅行社、遊覽車到特產店,
            通通被中資買去,中客來台的消費都大多被中資賺回去! 但這是馬英九時代,現在不是民進黨
            執政?為何忘了阿扁以前的「積極開放,有效管理」?民進黨明明可以防止中資一條龍的情況
            發生,執政兩年了卻無所作為,這已經不是無能可以形容了,根本擺爛! 中客也是客人,
            不是嗎?民進黨擺爛不好好管理,只會把客人拒於門外,又提不出相對的替代方案,最後不就是
            人進不來,東西賣不出去,年輕人找不到好工作只能北漂? 現在說什麼南向政策?還要騙嗎?
            事實是花納稅人的血汗錢買觀光客而已!不信去問問各大接南向的旅行社,觀光局有沒有補助
            南向旅客每人一萬?花大錢美化觀光客數字,民進黨做假政績還真拿手? 南向旅客來台有沒花
            一萬消費都不知道了,搞不好還落跑打工搶台灣人的工作,沒想著民進黨政府還補助他們一人
            一萬?執政是這樣搞的嗎? 喔,中國用中客要脅台灣必須承認 92 共識!是嗎?那為何現在來台
            的自由行與其他中客還有兩百多萬人次?沒 92 共識中客就不來了嗎? 最重要的是,蔡英文
            當選時根本不必提 92 共識這件事,提了有什麼好處都?為何沒事偏偏要捅馬蜂窩?不就是
            向獨派表態輸誠?結果獨派爽了,被中國打壓的後果卻要大家共同承擔? 台灣本來就沒被阿
            共統治,什麼共識有什麼好說的?事實怎樣就是怎樣,去跟沒有理性的阿共鬥嘴有意義嗎? 民
            進黨如果不要中客也可以,但要有替代方案!替代方案絕對不是南向那些比我們還落後的國家,
            而是開發更多高消費的歐美及日本觀光客! 台灣明明就有歐美人士最愛的陽光、沙灘還有
            離島,但民進黨執政都兩年了,墾丁還在坑丁?離島還是不能跟峇里島比?遊艇業也限制一堆?
            沒事只會炒短線的寶可夢、拼選舉、搞意識形態...,這樣的政府,要是還不下台,老百姓
            就真的要吃土了!
            '''
        ),
    )
    assert parsed_news.category == '評論,中港澳,投書,國內'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1541512800
    assert parsed_news.reporter == '路懷宣'
    assert parsed_news.title == '觀點投書:寶可夢與中客'
    assert parsed_news.url_pattern == '601210'
