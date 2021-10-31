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
    url = r'https://www.ntdtv.com/b5/2018/12/10/a102462948.html'
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
            香港北角今日(10日)下午接近2時,發生一起嚴重車禍。一輛接載孩童的娃娃車在英皇道與
            長康街斜坡路上,疑駕駛下車未拉手煞車,直衝近百米,衝入熙和街猛撞一家店舖門。目前
            已知2人不治身亡,另有12人在救治中。 從現場行車記錄器畫面,涉事娃娃車事發前正停在
            路邊,保母車突然往前滑行,剛下車的司機嘗試在車頭阻止,但未成功,反被車子撞倒並輾過
            拖行,倒在15米路外,此時娃娃車繼續往前高速衝下斜路,橫越英皇道分隔行車線,衝入熙和街
            撞倒多名路人,猛撞一家店舖門後才停了下來。 事發後,消防當局出動9輛消防車、15輛
            救護車,消防坍塌搜救專隊亦奉召到場救援,行動中共派遣82名消防及救援人員到場。 香港
            《蘋果日報》引述目擊者表示,當時經過現場,突然聽到「嘭」一聲巨響,轉頭一看,
            便見到娃娃車衝上行人,「不少人被車撞倒,有的好似傷得好重!」。 事發時,一輛的士
            剛巧駛過,司機吳先生說,當時正開車到了路口,期間娃娃車失控衝前撞到的士車身,
            幸好只有左邊的後視鏡損毀。 的士司機形容當時情況「太混亂」,保母車衝前後,
            「就看到一個人躺在地下」。 另外,事發後,一輛電車車長說,電車開過時時已經發生車禍,
            警方正在封鎖現場,但消防及救護員尚未到場。他說,「車底起碼有4、5人!有些人躺在路邊,
            受傷的人流好多血。」 受交通意外影響,英皇道來回方向近熙和街的全線現已封閉;
            由信德街至北角道之間的來回方向的電車服務暫停;受影響巴士路線須改道行駛。 下午
            17時許,警方表示,意外共造成2死12傷(22至89歲),死者包括83歲男子及80歲女子。 涉案
            司機62歲,今天早上7時開工,事發時正準備收工,交車給下一班的司機。事發時,司機
            因一度嘗試在車頭擋車,但不成功,司機被拖行20米,頭、頸及背部多處受傷,現留醫
            治療。 娃娃車隨後沿長康街往英皇道衝下後,撞到熙和街一家店舖才停了下下,期間輕微
            撞到2輛的士,另有2男一女被困車底,消防員花約20分鐘將他們救出。 警方表示,初步
            調查後,相信司機事發前「未拉或未全拉手煞車」肇禍,意外現場斜度約8度,從附近店舖
            的閉路電視攝得當時情況,警方將會調查意外是否涉及人為疏忽或機件故障,如受傷司機
            情況許可,警方將會向他錄取口供,或會作出拘捕。案件交由港島交通部特別調查隊跟進。
            '''
        ),
    )
    assert parsed_news.category == '港澳'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1544371200
    assert parsed_news.reporter is None
    assert parsed_news.title == '香港娃娃車衝下斜坡 司機阻車遭輾釀2死12人傷'
    assert parsed_news.url_pattern == '2018-12-10-102462948'
