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
    url = r'https://www.epochtimes.com/b5/13/3/6/n3816184.htm'
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
            晏嬰是春秋後期齊國著名的賢相,後人習慣上多尊稱他為「晏子」。春秋時魯昭公三年(西
            元前539年),齊景公認為晏嬰的住宅太差了,就對晏嬰說:「您身為宰相,不宜再住在這麼寒
            酸的房子裡了。我為你建造一座明亮高爽的住宅,如何?」 晏嬰卻堅決辭謝道:「我的房子
            是祖上留下來的,我能繼承這份家產已經很高興了,再說這房子又地處鬧市,買東西很方便。
            」齊景公聽後,知道一時說服不了他,便又換了一個話題問道:「既然您的房子靠近鬧市,那
            您是否知道物價的貴賤?」晏嬰回答說:「當然知道。」 齊景公又問:「那麼您說說,現在什
            麼東西在漲價,什麼東西在跌價?」這時晏嬰忽然想起齊景公平時濫用刑罰,砍了不少人的腿
            ,有人在街上出售假腿,就乘機勸諫道:「現在假腿的價格在上漲,鞋子的價格在下跌。」齊
            景公聽後明白自己錯了,立即下令減少刑罰。 晏嬰勸諫國君的妙語,受到了後人的稱讚。後
            來晏嬰的這句話演變成了一個成語叫做「踴貴屨賤」,「踴」是假腿的意思,「屨」是鞋子
            的意思。這個成語用來比喻嚴酷的法律。 不久後晏嬰出使晉國,齊景公便趁着晏嬰出國的
            這段時間選擇了一處好地方為他修建新宅,同時拆掉了晏嬰的舊宅,希望造成既成事實,使晏
            嬰不得不搬進新居。待晏嬰回到齊國時,看到新的晏府已經完工,自己的舊宅以及左鄰右舍
            的房屋都已被拆遷,鄰居全部搬走了。 晏子向景公拜謝以後,便拆了新居,把自己的舊宅以
            及原來鄰居的房子也全按原樣一一重修,把搬走的鄰居一家一家地請回來住。 晏子對人說:
            俗話講的好,「非宅是卜,唯鄰是卜」。(翻譯成今天的話,就是說:不用占卜住宅的吉凶,而
            是要占卜鄰居是否是好鄰居)。我與各位鄰居的關係是占卜過的,而且一直相處得很好,現在
            無緣無故地趕走他們,恐怕是不吉利的。這樣晏府又恢復了原先的樣子和布局。 但齊景公
            認為晏子掃了他面子,硬是不同意晏府的重建,君臣相持難下,後來晏子通過陳桓子從中調解
            ,景公總算勉強同意了晏子重建住宅。後人以此掌故稱頌晏嬰的清廉。 後來「晏嬰卜鄰」
            這個典故被用來指要選擇好的鄰居。另外從這個故事中又衍生出另一個成語叫作「卜宅卜
            鄰」。不過卜宅卜鄰的意思除了指遷居應選擇好鄰居的意思之外,往往還有搬遷的
            意思。 看了這個故事後,我一邊感歎晏嬰的清廉,並想到:選擇住址時,的確不僅要看房子的
            好壞,還要看周圍的社會人文等方面的環境,晏嬰卜鄰這個典故真的很有道理呀。 同時又
            進一步想到:不僅選房子是如此,在方方面面的社會關係中不也都是如此嗎?三國時諸葛亮的
            《前出師表》中不就說到要「親賢臣,遠小人」。有一個好的、向善的社會環境真的非常
            重要。 在目前這個道德水準整體不斷下滑的狀態下,當家長的一定要盡力為孩子開創出一個
            好的環境,至少是一個好的家庭環境,儘可能往孩子的頭腦、心靈中裝進好的、正的東西。
            '''
        ),
    )
    assert parsed_news.category == '文化網,文化百科,文化博覽,文化典故'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1362499200
    assert parsed_news.reporter is None
    assert parsed_news.title == '「非宅是卜 唯鄰是卜」晏嬰卜鄰的故事'
    assert parsed_news.url_pattern == '13-3-6-3816184'
