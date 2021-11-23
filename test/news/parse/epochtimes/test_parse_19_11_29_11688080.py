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
    url = r'https://www.epochtimes.com/b5/19/11/29/n11688080.htm'
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
            那年你帶我上太平山頂,我的眼裡是維多利亞港的醉人景觀,你的眼裡是對九七後的茫然與
            期盼。隔年你來台北,我帶你上陽明山,雙城都有美麗的山,親吻我們的風,後來卻很不一樣
            。 在那個網路還沒發達的年代,我已不記得是誰先停筆,一疊航空信成了記憶。前人拚下的
            靜好歲月,默默伴我成家立業,香港,我想你了。 景觀依舊醉人的維多利亞港外,一波波驚濤
            衝岸比執著,一朵朵浪花像有話要說。我看著你們,百萬人走上街頭和平示威,政府不理會。
            我看著你們,前仆後繼迎戰催淚彈,政府不手軟。絢爛煙花已失色,讓槍火彈幕在這城市飛舞
            有何不可。 香港,你會好起來嗎?你們為何日子不好好過,不珍惜所擁有。甚至有人說你變壞
            了,你收錢了,但我看到,幾名武裝警察壓制其中一個你,你毫不遲疑走過去,自己的肚子卻挨
            了一槍。誰能告訴我,你到底收了多少錢,值得賣命成這樣。誰能告訴我,你到底變得多壞,不
            管爸媽有多愛。 香港,你會好起來嗎?在街頭上被打的、受傷的,或許還算幸運吧,至少你還活
            在鏡頭下。被帶走的、被消失的,沒有編號的蒙面黑警會讓你,後悔不知死活。那是集體而
            平庸的邪惡,警隊標語「We Serve with Pride and Care」,中文似乎是「我包你痛徹
            心扉」。你們掙扎「We Fight with Blood and Tear」,狂飲熱血,醉成含淚顛沛。 香
            港,你會好起來嗎?那一發發槍彈,一道道水柱,那是扣下扳機的手;擲回催淚彈,扶起倒臥血泊
            中的手足,那是撐著雨傘的手;誰能告訴我,哪一邊的手心是冷的,哪一邊的手心是熱的? 香港
            ,你會好起來嗎?我不知道你們怎麼撐下來,更不知道還要撐多久?半年來,警棍槍彈水砲沒有
            把你們打退,面對高大堅硬的牆,你們依然像一顆顆雞蛋,誰能告訴我,你們為何一直要去撞牆
            ? 香港,你會好起來嗎?與惡的距離,與魔鬼的交易,在瀰漫火光煙霧的暗夜校園裡,我看著
            你們,努力撐著那面黑旗,困難的呼吸,勝過卑微的喘氣。我看著你們,撐著旗的手在發抖,青春
            在眼前燃燒,可還記得上次的微笑。孩子們,我好想叫你們回家,正義,也要留著命才要得回去!
            孩子們,你們不想未來被淪落,平安,卻是你們對家人的承諾! 香港,你會好起來嗎?我不和
            他們爭論自由,不和他們爭論是暴警或暴民的錯,他們看見你們,後來的暴力,我看見政府一直
            以來的暴力,他們看見你們,打砸燒毀,被自殺、被輪暴的你們,他們沒看見,瞳孔無法照遍角落
            ,雙眼相信什麼,靈魂就是什麼。 香港,你會好起來嗎?你挺在槍彈水柱,不懼逮捕羞辱,東方
            明珠更加璀璨,東方明珠的傳說,不再是那搖身成為迷人的五光十色,而是不做那苟且偷安、
            任由碾碎的粉末。 香港,這幾年我一直在找你,你和你的孩子平安嗎?如果,這個命運在我面前
            墜落,不知道我和孩子是不是會軟弱;盼望,你們激起大時代的驚濤,最終不會化為泡沫。 香港
            ,我錯看了你,原以為你只愛虛華功利,自由,才是你夢想的錦衣,你對夢想的堅持讓我,刮目
            相看、不可思議。 香港,你會好起來,我想再帶你來陽明山走走,希望雙城的秋風,同樣溫柔
            地親吻兩片天空。 香港,你會好起來,太平山頂的星星會繼續為你閃爍,走過風雨,迎接光輝,
            更堅強的你我,總會重逢在世界的角落。香港,你會好起來,我不是若無其事的旁觀者,你不是
            孤獨一個,我會盡力為你做點什麼。
            '''
        ),
    )
    assert parsed_news.category == '感悟隨筆'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1574956800
    assert parsed_news.reporter is None
    assert parsed_news.title == '香港,你會好起來嗎?'
    assert parsed_news.url_pattern == '19-11-29-11688080'
