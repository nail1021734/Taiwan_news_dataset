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
    url = r'https://www.epochtimes.com/b5/20/1/1/n11760836.htm'
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
            山東濟寧人邵士梅,字嶧暉,是順治己亥年的進士。他的一生很平凡,讀書、婚娶、科舉、做官
            。他的一生也異於尋常人,因他記得自己的前世以及轉生的經歷,因此得以和前世的妻子和
            孫女再續前緣。 邵士梅自稱前世是棲霞的處士(隱居不出仕,具有很高德行的人),有四個兒子
            ,六十多歲去世之際,他的四個兒子都正好外出,沒能待在他的身邊,惟獨孫女哭著與他訣別
            。 帶著前世記憶 轉世接親緣 處士去世後,看見有一青衣差吏帶他去見冥王。冥王一番話就
            把他後世命運都安排妥當了,他說:「你轉世後,仍是男身,日後高登乙榜,官至縣令。」處士
            轉生到邵家。邵士梅將前世的記憶帶到今世,前世種種依然歷歷在目,全都記得。 他受到鄉里
            的推薦,到青州任文教官,恰逢棲霞缺文官,於是前去赴任,同時也想去尋找前世的故居。因為
            前世的記憶並沒有抹去,他依然清楚地記得大街小巷及自家門庭。 邵士梅到了故居,前世的
            四個兒子都已經去世了,惟有孫女健在寡居,頭髮都已經花白了。邵士梅向她道及來此地的
            原因,並將前世的生活以及臨死之前的場景娓娓道來,說得全都不差。 孫女實在太貧窮,
            邵士梅取出自己的俸銀送給她。他在吳江做官不到三個月,就卸職回家,自稱冥數如此,不可
            違背,不能長久待在官場。 邵妻預言轉世地點 再續前緣 邵士梅的妻子某氏雖是普通民婦,
            卻有未卜先知的能力。她在臨死前,曾預言:「我們兩人會做三世夫妻,我再次轉生後,必會
            降生館陶縣的董家。董家居住在河邊,即河道彎曲處第三家。夫君那時已罷官,獨自借宿於
            蕭寺,當你翻閱佛經時,就會想到我,那就到那個地方去找我。」 後來,邵士梅到登州府任
            教授,升為吳江知縣不久後就稱病回家。當時,邵士梅有一同年在館陶縣作縣令,邵士梅取道去
            探訪他,並在蕭寺借宿。 蕭寺有一部藏經,邵士梅取來翻閱,這時忽然回憶起妻子臨終前所說
            的話,於是沿著河邊尋訪董家。果真位於河曲的第三戶民家姓董。 董家有一個女兒,還沒有
            出嫁。邵士梅向董家說明他的來意,並且懇求縣宰為他作媒,娶下董女,和前世的妻子再續前緣
            。 人身真像一件衣服,元神脫下這件衣服,再穿上另一件衣服時,從外表看就成了另外一個人
            。難怪歷代有不少人稱人生如戲,裝扮一番,粉墨登場,隨著戲裡的台詞演繹一生。當鑼鼓聲落
            ,人生的劇目也隨之落幕。 這樣看來,有多少人曾經是我們前世的兄弟姐妹、父母兒女。若
            能以善待人,對待那份不泯的親恩因緣,使它長久地維繫下去,而不侷限在今生今世,讓愛維繫
            前世的恩,讓愛牽起下世的緣。當胸懷寬廣到能愛天下之人時,就能從恩怨私念中超脫。
            '''
        ),
    )
    assert parsed_news.category == '文化網,文明探索,前世今生,輪迴轉世'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577808000
    assert parsed_news.reporter is None
    assert parsed_news.title == '他將前世今生的愛 又帶到了妻子的來世'
    assert parsed_news.url_pattern == '20-1-1-11760836'
