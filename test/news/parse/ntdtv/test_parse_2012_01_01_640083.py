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
    url = r'https://www.ntdtv.com/b5/2012/01/01/a640083.html'
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
            2011年,中東、北非的民主化浪潮迎來了「阿拉伯之春」,在這個過程中,既有埃及民眾推倒
            穆巴拉克政權,軍方保持中立不開槍;也有利比亞、敘利亞軍隊屠殺示威民眾,遭到國際的
            譴責和制裁。中東、北非獨裁政權相繼崩潰,給中共專制政權敲響了警鐘。新唐人第十大年度
            禁聞,阿拉伯的春天衝擊中共政權。 突尼西亞一名大學生因為抗議城管暴力執法,憤然
            自焚,點燃了「茉莉花革命」的導火索,早已對政府腐敗、失業和高物價不滿的民眾,走上
            街頭抗議,警方開槍鎮壓造成70多人死亡,引發大規模衝突和騷亂,鐵腕統治突尼西亞23年的
            總統本.阿里1月14號出逃。 1 月17號,突尼西亞新聯合政府宣佈將國家和政黨分離,隨後
            釋放所有政治犯,解散秘密警察。本·阿里原執政黨的所有官員宣佈全體退黨,原執政黨遭到
            取締和解散。6月20號,突尼西亞法庭以挪用公款罪,缺席判處本·阿里35年徒刑。突尼西亞
            的「茉莉花革命」引發骨牌效應,自1月25號開始,埃及上百萬民眾走上街頭示威抗議,要求
            82歲的穆巴拉克總統下臺、廢除實施30年的緊急狀態法。 警察與示威民眾發生流血
            衝突,造成上百人死亡。在蘇伊士城,示威民眾放火焚燒政府大樓和警察局;在首都開羅的
            示威民眾放火燒執政黨的總部大樓。 與突尼西亞軍隊一樣,埃及軍隊在民眾抗爭的18天裡
            保持中立不開槍。 原六四學生領袖唐柏橋指出,軍隊中立保障了政權的和平過渡,對中國
            軍人是很好的啟示。 埃及總統穆巴拉克2月11號被迫辭職。8月3號,埃及法庭審判穆巴拉克
            和他的兩個兒子、以及前內政部長和6名警官,指控他們蓄意謀殺抗議者並且濫權謀私。 受到
            埃及和突尼西亞革命的影響,利比亞2月15號開始爆發大規模和平抗議示威,遭到政府軍開槍
            鎮壓,甚至動用戰機、坦克轟炸,1000多示威者被打死。 總統卡扎菲22號在電視講話中,以
            中共出動軍隊坦克鎮壓天安門學生運動為例,為自己武力鎮壓民眾辯護。在海內外中國網民中
            引起一片嘩然。聯合國安理會2月 26號通過決議,對卡扎菲及他的子女和親信實施制裁。國際
            刑事法庭發出對卡扎菲及其兒子和親信的逮捕令,指控他們犯有「反人類罪」。 利比亞內務
            部長、司法部長等多名高官相繼辭職,軍隊警察、駐外使節、卡扎菲第六子也紛紛倒戈。反隊
            派佔據了利比亞大部分地區,成立了臨時政府。 經過6個月的激戰,利比亞反對派武裝8月23號
            攻佔首都,利比亞民眾歡呼長達42年的卡扎菲獨裁政權垮臺,利比亞駐各國使領館紛紛改換
            國旗。 10月20號,卡扎菲在他的家鄉從下水道裡被拖了出來,他惶恐的喊道「不要向我
            開槍」,但最後他還是死於痛毆和亂槍之下,他的屍體被沿街拖行,民眾紛紛圍觀拍照。 旅美
            政論家 曹長青:「所有的獨裁者在它獨裁的時候,那個耀武揚威、飛揚跋扈、不可一世,好像
            是不可戰勝的。但今天我們看看,那個武力哪去了?當恐嚇、恐懼消失了之後,人們起來
            反抗,那個專制其實不堪一擊的。」 卡扎菲毛骨悚然的的屍體畫面刺激了中共的神經。多年
            以來,卡扎菲一直是中共的老朋友,是對抗西方的同盟,是第三世界概念的倡導者。中共媒體
            稱讚卡扎菲是「特立獨行的英雄」。 浙江民主黨人士 陳樹慶:「像卡扎菲這樣,利比亞人民
            是絕對不會饒恕他的,人類自有人類的正義原則。他不同的做法會承擔不同的後果,滿足人民
            的要求,那人民肯定對他多一份寬容。但是中國將來會怎麼走,那這個最重要是要靠人民的
            力量。」 新西蘭《新報》主編陳維健表示,卡扎菲「不要向我開槍」對中共和一切獨裁者
            警示:「不要向我開槍」的前提是「不要向人民開槍」。 《法國國際廣播電臺》前中文部
            主任吳葆璋呼籲,中共體制內的人像利比亞起義的官員和軍人那樣,棄暗投明,不要為最後
            一個共產帝國殉葬。
            '''
        ),
    )
    assert parsed_news.category == '國際專題,敘利亞局勢'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325347200
    assert parsed_news.reporter == '李元翰'
    assert parsed_news.title == '阿拉伯之春 敲響中共警鐘'
    assert parsed_news.url_pattern == '2012-01-01-640083'
