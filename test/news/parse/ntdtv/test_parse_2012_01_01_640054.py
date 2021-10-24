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
    url = r'https://www.ntdtv.com/b5/2012/01/01/a640054.html'
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
            新年在即,不同國家、不同地區的人們採取了不同的方式迎接2012年的到來。這其中有充滿
            高科技色彩的絢麗焰火,也有注重祈福消災的傳統儀式,各有特色的新年活動折射出不同文化
            在過去一年中的感受以及對嶄新一年的期盼。 悉尼是世界上最早跨入新年的城市之一。今年
            在海港大橋上舉行的跨年焰火表演吸引了來自世界各地150萬的遊人。焰火表演的主題是
            「夢想時刻」(Time to Dream),用四種顏色所代表的「無盡彩虹」來展示。燈飾為標幟,
            紫色代表社區,藍色代表海港和對未來的展望,綠色代表環境,黃色體現樂觀和幸福。人們隨著
            表演進入高潮而盡情歡呼,希望在新的一年中也能充滿活力地度過每一天。 對日本人來說,
            新年是一年中最重要的節日。在東京,數千人聚集在擁有數百年歷史的增上寺,以同時放飛氣球
            的方式慶祝新年的到來。而寺院也在新年即將到來之際,按照傳統敲響108下新年鐘聲。關於
            108下鐘聲的涵意有不同的說法,然而無論哪一種都體現出日本人希望借新年鐘聲驅除煩惱和
            霉運,祈求神佛保祐的願望。2011年對日本來說是多災多難的一年,因此很可能會有更多的
            日本人在新年假期裡前往各地的寺廟為新的一年祈福。 在2012年即將到來之際,大量的印度
            國民和外國遊客湧向著名的泰姬陵,希望伴隨著那裏的美景度過一個難忘的新年,一些年輕
            人更在夕陽下頗有興致地彈起樂器來。 入夜之後,燈火輝煌的泰姬陵在絢麗焰火的照耀和
            粼粼水面的映襯下,顯得美不勝收,怪不得有遊客說,儘管年年來看泰姬陵,卻總是看不厭這裡
            的美景。 新年在即,對於剛剛推翻獨裁統治的埃及人來說,他們有著不同的感觸。12月31
            日深夜,人們再次聚集在首都開羅的解放廣場,唱著愛國歌曲,舉著國旗,同時點燃蠟燭,為在
            民主抗爭過程中遇難的同胞們祈禱。 在充滿希望但卻仍然飄蕩著悲傷的氣氛中,埃及人迎來
            了新的一年。
            '''
        ),
    )
    assert parsed_news.category == '法輪功,各界恭賀李洪志先生新年好'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325347200
    assert parsed_news.reporter == '倩雅於淼,任浩'
    assert parsed_news.title == '科技傳統美景 各地迎接新年特色不同'
    assert parsed_news.url_pattern == '2012-01-01-640054'
