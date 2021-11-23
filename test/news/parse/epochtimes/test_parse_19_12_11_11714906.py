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
    url = r'https://www.epochtimes.com/b5/19/12/11/n11714906.htm'
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
            《快雪時晴帖》是書聖王羲之的名作之一。清高宗乾隆皇帝非常欣賞、珍愛此帖,將其與
            王獻之的《中秋帖》、王羲之族侄王珣的《伯遠帖》,一起珍藏在紫禁城養心殿的書齋,視為
            天下書蹟「三希」,其書齋也因此稱為「三希堂」。《快雪時晴帖》就是《三希堂法帖》的
            代表名帖。明代收藏家劉承禧題記為:「天下法書第一,吾家法書第一」 「帖」(音tiè,同
            餮)是寫在紙、帛上的書信、詩、文等手書墨蹟,這也是現代人常見的古人的書蹟名作的由來
            。我們現今看到的王羲之書蹟大都是唐人雙勾填墨的精摹本。晚明書家王穉登在《快雪時
            晴帖》上題跋說是手寫墨跡:「朱太傅所藏二王真跡共十四卷,惟右軍(王羲之)快雪、大令
            (王獻之)送梨二帖乃是手墨,餘皆雙鈎廓填耳,宋人雙鈎最精出,米南宫(米芾)所臨者往往
            亂真,故前代名賢不復辨論」。元代趙孟頫題跋中說「得見真跡...不勝欣幸」:「東晉至今
            近千年書跡留傳至今者絶不可得,快雪時晴帖晉王羲之書,歷代寶藏者也,刻本有之,今乃得見
            真跡,臣不勝欣幸」;元代翰林學士劉賡在帖上題跋,寫道:「快雪晴時帖墨本乃真跡」。現代
            的鑑賞者多以為本帖是宋人雙鈎填墨本。 賞《快雪時晴帖》品書情意趣 《快雪時晴帖》是
            一封非常簡短的行書體書信 ,由王羲之寫給淮陰的張姓朋友。信函紙縱 23 公分、橫 14.
            8 公分。在一個冬日裡,下了一場快雪之後,王羲之給朋友張侯寫了一封手札: 羲之頓首:
            快雪時晴佳。想安善。未果為結,力不次。王羲之頓首。山陰張侯。 全函只有二十八字,
            字字珠璣,乾隆皇帝譽為「二十八驪珠」。這二十八中,除去稱謂、問候敬語和收信者之外,
            就只有15個字──「快雪時晴佳。想安善。未果為結,力不次。」 一場快意的大雪之後,
            王羲之向友人問候,並敘及一過去事的結果「未果為結,力不次」。朋友之間的默會,盡在
            輕描淡寫間,風雪之外有深意。人間事,未能開花結果的太多了,冥冥間凡事皆有因果緣牽,
            羲之感到「力不次」,力量所不及,自有天意安排,就隨它去吧!看這一場暢快的大雪,澄淨了
            天地人心,晴朗的佳景多麼美好! 書如其人;人如其書。書法書跡就好像一面鏡子反映人的
            內心、情性,心情糾結時,為名利牽絆時,該寫不出來閑逸和暢的筆跡來。《晉書》記載王羲之
            以「骨鯁」著稱,正直聞名,看「東床快婿」故事典故反映的是羲之的灑脫率性。羲之自述
            「素自無廊廟志」,志不在名利官場在修道,雖得朝廷公卿愛其才器,屢次徵召為官,他並不為
            所動,又被授與護軍將軍,他還是推遷不拜。這樣清虛澹泊、至在無求的王羲之,怎可能因「
            未果為結」而患得患失呢? 此行書帖筆法圓渾典雅、遒美健秀,點、畫、勾、挑都不露鋒,
            結體平穩勻稱,淳正和暢,在羲之行書自然灑脫的風流中,融合質樸又閑逸的意趣。從帖的風采
            韻味所反映的心情,應該是一場爽快的大雪靜悄悄地消融了「未果為結,力不次」的悵然。
            大雪來得正是時候,去得適時!此時的心境就像是冬日「 快雪時晴」當下的爽快、豁然開朗
            ! 唐太宗親在《晉書.王羲之傳》撰讚辭,讚美王羲之書法為古今「盡善盡美」第一人!稱讚
            他的筆法點曳、文字裁成如「煙霏露結,狀若斷而還連;鳳翥(高飛之意,音助)龍蟠,勢如斜
            而反直」,玩之不覺為倦。在《快雪時晴帖》中,我們也能玩味出「狀若斷而還連」這般的
            情味和「鳳翥龍蟠」神態意興來。 三希神帖和乾隆皇帝 《書斷》評王羲之書法「千變萬化,
            得之神功」;《快雪時晴帖》被乾隆皇帝奉為「三希」之首,品為「神」品。在歷次臨池摹寫、
            御覽中,乾隆皇帝御筆題識了71則。從其中看到,乾隆帝寄寓了「盼雪」的期待》晉王羲之
            快雪時晴帖
            '''
        ),
    )
    assert parsed_news.category == '文化網,文化百科,文化博覽,神傳漢字'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1575993600
    assert parsed_news.reporter is None
    assert parsed_news.title == '「天下法書第一」王羲之《快雪時晴帖》的意趣'
    assert parsed_news.url_pattern == '19-12-11-11714906'
