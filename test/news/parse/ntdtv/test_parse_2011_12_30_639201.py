import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.ntdtv
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/12/30/a639201.html'
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
            隨著朝鮮獨裁者金正日的葬禮結束,他17年的鐵腕統治也宣告落幕。引起全世界關注。12月
            29號舉行的金正日追悼大會,宣佈他的小兒子金正恩是黨政軍「最高領袖」,正式開啟了
            「金正恩時代」。與此同時,圍繞朝鮮半島的外交戰全面展開。 29號的金正日追悼大會在
            平壤市中心廣場舉行,約有10萬朝鮮軍民參加。朝鮮最高人民會議常任委員會主席金永南在
            悼詞中說,金正恩為「黨、國家和軍隊的最高領袖」,是唯一的領導體制。 在28號的遺體告別
            儀式上,朝鮮電視臺直播了金正恩等新領導班子步行護送靈車的場面。朝鮮領導層則通過黨報
            《勞動新聞》,向金正恩宣誓效忠。聯合國總部按慣例也降了半旗。 當天,靈柩車隊在平壤市
            內巡遊,綿延40公里的數十萬朝鮮民眾冒雪送行,呼天哭地。山東大學退休教授孫文廣表示,
            這與1976年中共獨裁者毛澤東去世的場面相似。 孫文廣:「他們把金正日宣傳作『偉大的
            領袖、人民的救星』,那麼在這樣一種教育、灌輸之下,很多民眾覺得金正日去世了,天都
            塌下來了,悲痛萬分。和1976年的中國基本上是一樣的,它是多年進行迷信教育、把領袖神化
            所造成的一個結果。」 金正恩將傚法金正日,為亡父守孝三年。金正日的遺體將作防腐處理,
            安放在錦繡山紀念宮的水晶棺內,與父親金日成遺體一同,供公眾憑弔。 中國作家、前
            《方圓》雜誌記者謝朝平表示,這本身是一種封建體制的傳統。 謝朝平:「事實上,那也是
            封建殘餘的一種表現。你看社會主義國家或者共產主義國家的人都喜歡那樣搞,比方列寧、
            我們國家、還有朝鮮他們都這樣做,這還是一個制度不同的原因吧。」 中共國防部長梁光烈等
            軍方高層27號前往朝鮮駐華使館弔唁。中共國防部發言人28號在記者會上,否認有關中國
            軍隊已派兵進入朝鮮境內的報導。 朝鮮《勞動新聞》說,金正日留下的最大遺產就是核武器
            和衛星。 28號,朝鮮電視臺播放了2009年4月朝鮮試射遠程導彈的畫面。因為那次行動,
            聯合國加強了對朝鮮的制裁,朝鮮退出六方會談。 金正日鐵腕統治朝鮮17年,上世紀90年代
            發生嚴重饑荒,200多萬人餓死。聯合國指出,朝鮮目前仍有三分之一的人口約610萬人急需
            糧食援救。 韓國《朝鮮日報》29號發表題為「南朝鮮如何評估金正日?」的社論,指出金正日
            在憲法中刪除了「馬克思列寧主義和共產主義」用語,甚至摘下社會主義的招牌,將主體思想
            視為唯一思想,將金日成擁戴為朝鮮的始祖。 《朝鮮日報》說,金正日在去世前,希望以中止
            鈾濃縮設施,換取美國24萬噸營養援助。訪問美國的六方會談韓方團長林聖男28號表示,韓美
            雙方就重啟與朝鮮的對話,達成了共識。 《韓聯社》報導,中國將在年初向朝鮮緊急提供50萬
            噸糧食援助。日本將在韓美日協商的框架內擴大對朝鮮影響力,俄羅斯也在調整加深對朝鮮
            問題的介入力度。隨著金正日追悼期結束,圍繞朝鮮半島和六方會談的外交全面展開。
            '''
        ),
    )
    assert parsed_news.category == '國際專題,朝鮮半島局勢'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325174400
    assert parsed_news.reporter == '秦雪,李元翰,孫寧'
    assert parsed_news.title == '铁腕统治落幕 金正恩主掌朝鲜'
    assert parsed_news.url_pattern == '2011-12-30-639201'
