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
    url = r'https://www.ntdtv.com/b5/2011/12/30/a639608.html'
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
            印度內政部長齊丹巴蘭今天表示,造成兩名台灣人受傷的去年9月舊德里賈瑪清真寺槍擊案是
            伊斯蘭激進組織「印度聖戰士」所為,當局將在逮捕所有涉嫌人後將全案起訴。 印度內政部
            12月例行記者會,於傍晚在中央政府辦公大樓新聞署簡報室舉行,由齊丹巴蘭
            (P. Chidambaram)對媒體簡報本月內政安全情勢並接受提問。 齊丹巴蘭回答中央社記者
            有關去年9月19日舊德里(Old Delhi)賈瑪清真寺(Jama Masjid)槍擊案偵辦進度時指出,
            內政部認為案子是「印度聖戰士」(Indian Mujahideen,IM)所為,也已破獲做案的
            IM分支。 他說,「但我們仍在搜捕其他人,當所有嫌犯都遭逮捕,(政府)才會起訴。不過
            我們認為案子就是『印度聖戰士』幹的」。 他表示,只要案子一起訴,所有偵辦資料都會對外
            公開。不過齊丹巴蘭未針對警方是否正式宣佈破案的提問作出回應。 德里警察局1日表示,
            破獲印度聖戰士1個分支,逮捕6名嫌犯,分別涉及去年普恩(Pune)德國麵包店、班加羅爾
            ( Bangalore)辛納斯瓦米體育館(Chinnaswanmy Stadium)兩起爆炸案,以及舊德里
            賈瑪清真寺槍擊案。 儘管如此,警方遲未宣佈破案。德里警方在中央社記者詢問時,也不願
            說明相關細節。 去年9月19日上午,在賈瑪清真寺3號門外作業的台灣TVBS電視台
            「食尚玩家」節目外景隊1行6人,不明原因遭騎1部機車的兩名蒙面歹徒開槍掃射,造成兩名
            攝影師受傷,其中1人在3天後離印,另1人經緊急開刀取出右腹部子彈,住院9天後出院返台。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325174400
    assert parsed_news.reporter is None
    assert parsed_news.title == '印度:聖戰士犯下槍擊台灣人案'
    assert parsed_news.url_pattern == '2011-12-30-639608'
