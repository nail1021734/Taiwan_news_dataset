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
    url = r'https://www.epochtimes.com/b5/19/10/25/n11611601.htm'
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
            楚漢之爭的時代,項羽的旗下,有個重信諾的季布將軍。季布重信諾在當時就非常有名,太史公
            《史記.季布欒布列傳》記載,楚國有一句俗諺:「得黃金百(斤),不如得季布一諾。」就是
            讚揚他的。楚國遊士、辯士曹丘生在各地方遊走時,也廣傳了季布重諾行誼。楚國稱讚季布的
            那句俗諺,就是後代成語「一諾千金」的根源。宋代楊萬里《答隆興張尚書》中,有「一諾
            千金,益深謝臆」的詞語。「一諾千金」也作「千金一諾」。 季布是出身楚國的俠義人士,
            有擔當講信用,樂於助人,馳名楚地、梁地。人生有起、有落,當季布遇難時,有人出身相護、
            有人相挺,這些人非常珍惜講信諾的人,寧願為保護信諾之人而獻出生命,千金也不能動搖他們
            的心性。我們就來看看這「一諾千金」引起的力大無比的效應展現。 秦朝末年,楚漢之爭中,
            季布在項羽的陣營將領士兵,數度圍困了漢王劉邦。後來,項羽戰敗在烏江結束了一生,劉邦
            開漢朝,懸賞千金要捉拿季布,且昭告說如果有人敢藏匿他,一律論處,罪及三族。 在這樣的
            危險氛圍中,對於輔助項羽、重諾的大丈夫季布,還是有不少俠義之士不怕死地維護他,第一位
            是濮陽人士,重義氣甚於生命的周氏。 季布亡命天涯之時,先是藏匿在周氏家中。有一天,
            周氏告訴他尊敬的將軍季布說:「漢朝急於用錢買將軍的命,就要追到臣的家中了。將軍如果
            能聽臣的話,臣就能獻出計謀;如果將軍不想聽,臣願意先自行剄頸自殺。」 季布應允了周氏
            所獻的計策。於是周氏將季布裝扮成罪犯,剃去他的頭髮,在他的脖子箍上鐵圈,並且為他換上
            粗布衣,送上了運棺柩的大車。那大車將季布連同家僮數十人運送到魯地,到知名的遊俠朱家
            那兒求售。 朱家是第二個幫助季布的俠義之士,他是讓季布的人生起死回生的關鍵人物。他
            心裡明白,那個貌似獲罪服雜役的人其實是大名鼎鼎的項羽的將軍季布,於是買了下來,讓他
            去耕田;他告誡兒子說:「田地裡的事都聽這個奴僕的,你要和他一起用餐。」 然後,他乘著
            輕便馬車上了洛陽,為季布鋪展起死回生的路。 朱家到了洛陽,冒著死亡的風險,找到貼近
            高祖的重量級人士夏侯嬰--汝陰侯滕公。夏侯嬰是劉邦的同鄉、少年好友,同時又是漢朝的
            開國功臣。 朱家先問說:「季布犯了什麼大罪?為何皇上急急切切要捉拿他?」 滕公答說:
            「因為他數度為項羽圍困過皇上,皇上怨恨他,所以一定要捉拿到他。」 朱家接著試探滕公說
            :「公覺得季布是怎樣的人呢?」 「賢人。」滕公答說。 朱家心裡篤定了,於是開始據「理」
            與「利」為季布求情,說道:「臣各自為其主盡心盡力,季布為項氏所用,為他盡力乃是職責
            所在。難道項氏的臣下都要趕盡殺絕嗎?再說,皇上剛得天下,就因一己的私怨懸賞千金捉拿此
            一人,不就是昭示天下不能廣容異己嗎!季布賢能,在漢朝的逼迫之下,可能北走胡地或南走
            越地,這不是讓壯士去資助敵國嗎?這是國之大忌啊!昔日伍子胥鞭楚平王之墓,殷鑑在前。
            公何不從旁勸誘皇上呢?」 汝陰侯滕公心中明白朱家為季布請命,也知道季布應該是藏匿在他
            那裡,乃許諾了他。他日,汝陰侯滕公趁機進言給劉邦,劉邦乃赦免了季布,並且召見他,授職
            郎中。 華夏之邦原是千金不換的信諾之鄉,大唐詩仙李白詩中說「一諾輕黃金」 ,重信
            諾的德性得到代代珍惜!「一諾從來許殺身 」,讓氣節之士連生死都不怕,信諾義行力大
            無比!重信的一諾感動人、保障人,將會招來更多的信諾,「一諾百金」、「一諾千金」,環環
            相扣,千金不「壞」。講信用、重信用的人多了,更能形成一個確保生命安全的環境! 轉個身
            看當今的中原大地,蒙塵何等深刻!爭利忘義的行徑正在毀滅華夏子民重信諾的基因,上下
            交爭利,正在自掘墳墓,毀滅己身安全的生存環境。人人推波助瀾,「打造」無信之國,人人
            自危,絕對不是妄語。 註釋 李白《經亂離後天恩流夜郎憶舊遊書懷贈江夏韋太守良宰
            》詩。 唐代 戎昱 《上湖南崔中丞》
            '''
        ),
    )
    assert parsed_news.category == '文化網,文化百科,文化博覽,文化典故'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1571932800
    assert parsed_news.reporter is None
    assert parsed_news.title == '「一諾千金」 讓人生死相許!'
    assert parsed_news.url_pattern == '19-10-25-11611601'
