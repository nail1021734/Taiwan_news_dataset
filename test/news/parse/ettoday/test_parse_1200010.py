import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ettoday


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='東森')
    url = r'https://star.ettoday.net/news/1200010'
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

    parsed_news = news.parse.ettoday.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            新竹縣中古車行老闆陳明義今年5月酒後駕駛價值百萬的MINI Cooper外出,卻撞死77歲的吳
            姓婦人,還「掛屍」拖行3公里。新竹地檢署檢察官認為,陳男在第一時間矢口否認不知道有
            撞到人,一度躲回自己經營的車行企圖湮滅證據,因此決定依酒駕致死及肇事逃逸等罪起訴,
            同時建請法官從重量刑。 吳姓婦人今年5月23日清晨和丈夫外出運動,行經新和路路口時遭
            陳男駕駛的車輛撞上,力道之大導致她整個人倒插卡在破裂的擋風玻璃上,還遭一路拖行3公
            里,最後拋飛在路邊。丈夫目睹車禍瞬間嚇得趕緊追上去,但等到找到人時,妻子早已倒臥在
            血泊之中毫無反應,送醫急救仍因傷重宣告不治。 警方當時循著行車路線追查,沒想到竟然
            在地上撿到掉落的車牌,這才找到肇事後躲回中古車行的陳男。更誇張的是,陳男看到警方
            找上門還裝傻,頻頻強調不知道有撞到人,直到被監視器畫面打臉才認了當天凌晨有跟朋友
            聚餐喝酒,同時供出藏匿肇事車輛的地點。 這些話聽在死者家屬的耳裡相當於是二次傷害,
            吳婦的兒子氣憤地說,「不曉得撞到人怎麼可能,那麼大的撞擊,整個擋風玻璃都碎裂了。」
            而陳男坦承犯行後仍不斷哭窮,聲稱自己家境清寒,開的雖然是價值百萬的名車,卻是2年前
            在新豐鄉做中古車買賣得到的,內部都壞得差不多了。 檢方認為,陳男酒駕肇事,明知撞到
            人還執意繼續前行,並利用急速轉彎將掛在擋風玻璃的受害人甩落,事後又躲回車行裝沒事,
            第一時間也矢口否認犯行,事發至今1個月依舊堅稱沒有要求好友幫忙作偽證,企圖湮滅證據
            脫罪,可見根本沒有反省之意,因此依酒駕致死及肇事逃逸等罪起訴,並建請法官從重量刑。
            '''
        ),
    )
    assert parsed_news.category == '社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530055140
    assert parsed_news.reporter is None
    assert parsed_news.title == '酒駕百萬MINI撞死老婦「掛屍」3公里 車商盧1個月還想脫罪'
    assert parsed_news.url_pattern == '1200010'
