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
    url = r'https://star.ettoday.net/news/1200017'
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
            歷經了前2戰12次射門全部落空,球隊陷入淘汰邊緣後,梅西(Lionel Messi)在對奈及利亞的
            關鍵戰役中,只花了14分鐘就破門,替阿根廷點燃了晉級的希望,最後探戈軍團神奇地以2比1
            氣走對手晉級16強,賽後梅西獲頒單場最佳球員終於露出久違的笑容,他坦言這一勝對全隊
            來說是「極大的解脫」。 在阿根廷首戰遭冰島1比1逼平後,梅西被拍到在第2戰面對
            克羅埃西亞賽前,眉頭深鎖還用手指按著額頭,神情看起
            來相當痛苦,他所承受的壓力旁人難以想像,結果在隊友再次「零支援」之下,他次戰僅觸球
            49次、射門1次,球隊下半場被猛灌3球,最後以0比3慘敗,1敗、1和積分僅1分,掉入淘汰邊緣
            。 最後一輪的比賽,阿根廷不僅得贏奈及利亞,還要視另一場克羅埃西亞對冰島的比賽結果
            ,才能確定是否可以晉級。雖然希望渺茫,但總是能帶來奇蹟的梅西,再次挺身而出,他只用了
            14分鐘就取得進球,他在禁區內巧妙以左膝停球,左腳調整後起右腳完成射門,打破了對手的
            大門。 這一腳射門行雲流水,這是大家所熟悉的梅西,嬌小的身軀永遠比對手跑得更快,各種
            不可思議的動作在他身上看起來都很合理。這顆進球不僅讓他終結了
            長達662分鐘的進球荒,更大大振奮士氣低迷的阿根廷,而奇蹟再次於比賽第86分鐘降臨,當
            時雙方1比1,羅霍(Marcos Rojo)射入了致勝球。 最終阿根廷以2比1力克奈及利亞,從賽前1
            分積分變成4分,取得D組第2晉級16強,而梅西也獲得單場最佳球員的肯定,他露出久違的笑
            容,他坦承過去這段時間非常痛苦,「這場勝利對我們而言,是極大的解脫,我們從沒想過我們
            會遭遇這麼多苦難。」 雖然前2場都沒能贏下來,讓梅西遭致各種辱罵,但他仍
            感謝阿根廷國內球迷和到俄羅斯現場替球隊打氣的球迷,「阿根廷的戰袍高於一切,我知道
            上帝站在我們這邊,所以我們不會被淘汰。」 談到16強賽將強碰陣容堪稱本屆最豪華的法
            國,他不諱言將是艱難的戰役,但他們會做好準備,「我們看了每場法國的比賽,他們是一支
            強大的隊伍,陣中的球員都有極為出色的個人能力,他們有速度非常快,能在關鍵時刻發威的
            球員。毫無疑問,這會是一場艱難的比賽。」
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530052620
    assert parsed_news.reporter == '游郁香'
    assert parsed_news.title == '獲單場最佳展笑顏 梅西談奇蹟一勝:極大解脫'
    assert parsed_news.url_pattern == '1200017'
