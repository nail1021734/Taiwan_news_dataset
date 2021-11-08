import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2018/11/21/a1400130.html'
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
            2014年香港佔中運動的幾名組織者在11月19號出庭受審,一百多名支持者前去聲援。
            評論認為,這是一場政治檢控,如果「佔中九子」真的因此獲罪,會開一個很壞的頭,
            使得「政治檢控」在香港蔓延。 一百多名支持者11月19號聚集在香港西九龍裁判法院門口,
            聲援當天受審的「占中九子」。 2014年8月,中共人大出臺有關香港政改的決議,讓港人
            真普選夢碎,隨即引發了自1997年香港主權移交以來最大規模的「公民抗命」——占中運動。
            超過十萬港人走上街頭,要求真普選。 11月19號,受審的九名占中運動組織者,包括
            香港大學法律系副教授戴耀廷,香港中文大學社會學系副教授陳健民,基督教新教牧師朱耀明,
            以及立法會議員陳淑莊及邵家臻等人。 「占中九子」分別被控煽惑他人作出公眾妨擾等
            罪名。九名被告在庭上否認全部控罪。 香港工黨副主席李卓人表示,幾名組織者在
            占中運動期間已經表示會承擔法律責任。但這次顯然是政治審判。 香港工黨副主席李卓人:
            「我們是公民抗命,我們知道法律是什麼,然後我們也願意付出這個代價。
            但是問題就是現在罪名不是公眾遊行的罪。現在罪名是一個很模糊的『煽動他人煽動公眾
            妨擾』罪。這個普通法也沒有一個準則,是什麼罪名?所以我們覺得這個完全是個政治
            檢控。」 香港前立法會議員,社民連成員梁國雄當天也去聲援。他表示,「煽動他人煽動」
            罪在澳洲因為違憲已經被取消,但香港卻以此起訴他們。 香港前立法會議員,社民連成員
            梁國雄:「審判他們不是單單審判他們九個人,是審判雨傘運動,也是審判香港人,
            也是在考驗香港的司法機構。若是這一次法庭用這樣的荒謬的罪名去判他們刑,
            那當然是香港言論和集會的自由受到進一步的打壓。」 案件預計審訊20天,如果九人
            被判有罪,個人可能面臨最高七年的監禁。陳建民在當天聆訊結束後會見記者,擔心案件
            對香港未來造成影響。 占中發起人陳建民:「即是此案成立的話,在香港會產生寒蟬效應,
            甚至可利用來清洗香港反對力量。」 香港工黨副主席李卓人則擔心,案件會開一個很壞的頭,
            使得「政治檢控」在香港蔓延。 李卓人:「當開始政治檢控之後,就一直會下去都是這樣。
            因為大家都知道在大陸當然很多是政治檢控。但是在香港我們理論上有法治,應該是有我們的
            自由,我們的《基本法》保障。但是現在都沒有了。這個對香港來講是非常的擔心。」 案件
            也引發國際關注,英國下議院多名議員提出動議,譴責香港特區政府起訴占中參與者。美國
            國會上星期也發表報告,批評香港法治和言論自由持續被侵蝕。 但香港特首林鄭月娥則聲稱,
            這是干預香港內部事務。 李卓人:「這個通常什麼『干預內部』都是中共政府外交部的講法。
            他們都變成了中共外交部的發言人,這個是很危險的,因為這樣的話就是更給人家覺得,香港
            已經不是香港。」 李卓人表示,從根本上來說,這不是香港前途的問題,也不是占中者被檢控
            的問題,而是一國兩制的問題。香港人已經明顯感到,自由越來越受到「一國」的威脅,而
            「兩制」開始蕩然無存。 《自由亞洲電臺》引述美國律師的警告,說:審訊結果可能引起
            美國國會更大反應,而重新審視香港的地位。
            '''
        ),
    )
    assert parsed_news.category == '港澳台專題,香港佔中爭普選,雨傘運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1542729600
    assert parsed_news.reporter is None
    assert parsed_news.title == '占中九子受審 港人憂政治檢控'
    assert parsed_news.url_pattern == '2018-11-21-1400130'
