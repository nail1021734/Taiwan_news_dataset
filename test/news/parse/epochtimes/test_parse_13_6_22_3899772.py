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
    url = r'https://www.epochtimes.com/b5/13/6/22/n3899772.htm'
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
            清代有個縣令,在寶山縣任職時,有一位過往的客商前來報案,說他被人搶了財物,事情就發
            生在江邊的一個碼頭。 縣令接到案子,就親自到那裡去調查。他發現從這裡走水路可以直
            通縣城,但是乘船的客商卻總要在這裡卸貨,再僱用腳夫,從陸路把貨物運往縣城。縣令心想
            :這其中必有蹊蹺,就向那裡的人詢問原因,但被問的人,都支支吾吾,不敢說出真相。 正好
            有一位當地駐軍的把總(職官名)前來晉見,縣令問他,為什麼客商到了這裡,卻不走水路而改
            走陸路? 把總說:「從這裡乘船,原是可以直通縣城的。現在客商到了這裡,就要卸下貨物,
            而從陸路運貨,都是因為碼頭附近的百姓太窮,他們全靠挑擔的收入來維持生計;因此,商船
            到了這裡,就叫他們卸貨。」 縣令又問起有人搶劫客商財物的事,把總說:「這事小人不敢
            說,除非老爺寬恕小人之罪,小人才敢開口。」 縣令說:「本朝的律令,不是有自首就能免罪
            的條款嗎?你向我報告實情,就可算作自首,你還顧慮什麼呢?」把總聽了縣令的話,這才戰戰
            兢兢地說道:「那些搶劫財物的人,都是把持一方的惡棍,小人的兒子,也是其中的一個惡棍
            。上個月,有一位客商經過這裡,見水路可通縣城,不肯靠岸卸貨,因此發生爭吵,被這幫惡棍
            毒打一頓,還被搶走了財物。這事確實是有的。」 按照乾隆三十年朝廷頒布的新例,凡朝廷
            命官拿獲強盜者,一律破格​​升遷。這個縣令根據把總所講的情況,便抓獲了有關人犯,在給這
            宗搶劫案定罪時,縣令一心想著升官,竟具文向上司呈報,說自己拿獲了強盜,又說把總知情
            不報,按照窩藏盜匪有罪的條例處決。一起被殺頭的,共有六人,都懸竿示眾。而縣令因為獲
            盜有功,被破格升為安慶知府,六年後,又升職做了道台。 不久,這位道台(即以前的縣令)出
            巡沿海,來到寶山縣當年發生搶劫案的碼頭。只見那裡依然豎著六根竿子,上面掛著六具骷
            髏,就問隨從的官吏:「前面那竿子頭上,一顆顆掛的是什麼東西?」隨從的官吏連忙答道:「
            這是大人您當年砍下的六個強盜的人頭呵,大人因此而升遷,難道您忘啦?」 道台一聽,立即
            毛骨悚然,十分驚惶,怒罵道:「該死的奴才!誰教你把我帶到這地方來的?快回府!回府!」說
            著就又氣又惱地回到了衙門。 道台剛踏進衙門的後宅,就一​​眼瞥見以前的那位被自己騙殺
            的把總,坐在他的​​內室裡。於是大罵守門人:「混帳!這裡是官衙的內室,你竟敢讓這個把總
            擅自進來,真是該死!」 道台的罵聲剛落,突然間,他就大叫背上疼痛!家人朝他背上一瞧,只
            見長了一個大膿瘡,周圍有六個膿頭,好像都在圍著膿瘡啃咬。道台的家人,知道這是不祥之
            兆,連忙燒紙錢,磕頭祈禱,又請來高僧,誦經懺悔,但都無濟於事。 那道台從此一病不起,日
            夜疼痛,叫苦不止,在悲慘惶恐中死去。
            '''
        ),
    )
    assert parsed_news.category == '文化網,文明探索,前世今生,善惡有報'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1371830400
    assert parsed_news.reporter is None
    assert parsed_news.title == '詐騙枉法升官 惶懼遭報慘死'
    assert parsed_news.url_pattern == '13-6-22-3899772'
