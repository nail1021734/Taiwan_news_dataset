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
    url = r'https://www.ntdtv.com/b5/2011/12/31/a639655.html'
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
            俄羅斯2012年總統大選候選人日里諾夫斯基20日針對金正日死亡消息評論說:“不要期待
            朝鮮會發生變革,除非中共倒台和莫斯科的民主發生變化。” 俄羅斯媒體近日均報導了關於
            朝鮮領導人金正日死亡的消息,俄評論界圍繞金正日死後的朝鮮及東亞局勢展開討論。有評論
            擔心,朝俄關係可能會發生變化,朝鮮19 日進行導彈試射顯示,朝鮮半島局勢可能惡化
            等等。 還有評論稱,獨裁者金正日死後,將會給朝鮮帶來實施民主變革的難得機遇。不過,
            俄羅斯自由民主黨主席,2012年總統大選候選人日里諾夫斯基19日針對關於朝鮮將發生變革
            的猜測評論說:“不要期待朝鮮會很快發生變革。” 俄羅斯“重要評論”網站在20日刊登
            日里諾夫斯基評論說:“在北京和莫斯科還沒有真正民主的時候,很難令人相信北朝鮮會成為
            民主社會。” 日里諾夫斯基還預測說,北朝鮮民主的到來是要等待中共的倒台。他說:“朝鮮
            的老百姓早就對當局共產陣營那一套感到厭惡,都很樂意加入到韓國。只要中國共產黨政權
            一倒台,我們國家的民主一改善,北朝鮮肯定會發生民主變革。” 這位曾多次參加俄羅斯總統
            大選,並將在2012年繼續角逐俄羅斯總統的自民黨領袖,一直是共產黨和共產主義的嚴厲
            批評者。他在11月30日的一次對全俄羅斯播放的電視辯論中再次強調說:“共產主義早就
            沒人信了。” 他說:“當年就連不敢說反共兩個字的俄羅斯人,也沒人信共產主義和列寧了,
            俄羅斯人都痛恨共產黨黨組織,黨中央,黨的領導人逝世,我們都偷偷高興, 20年前蘇共倒台,
            沒有人出來為他們辯護,而都希望將共產黨領導人送上法庭。今天一些人仍在打著共產主義的
            旗號,他們自己也早應該同列寧的屍體一樣被埋葬了。” 據朝鮮媒體對外宣布消息,執政超過
            17年,69歲的金正日於17日8時30分在外出視察途中由於過度勞累,在列車上逝世。克里姆林宮
            新聞局19日發布消息說,俄總統梅德韋傑夫已就朝鮮領導人金正日去世向金正恩致慰問電。朝鮮
            駐莫斯科大使館在20日舉行了金正日逝世悼念儀式,但記者們被拒絕進入。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325260800
    assert parsed_news.reporter is None
    assert parsed_news.title == '俄總統候選人:中共不倒台 朝鮮不會變革'
    assert parsed_news.url_pattern == '2011-12-31-639655'
