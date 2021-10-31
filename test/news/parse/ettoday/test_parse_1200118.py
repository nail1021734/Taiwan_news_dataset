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
    url = r'https://star.ettoday.net/news/1200118'
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
            奈及利亞與阿根廷的比賽一開始雙方就大起大落非常激烈,是一場雙方都想拼下來的比賽。
            最終憑藉羅霍(Marcos Rojo)的絕殺,阿根廷2比1戰勝非洲雄鷹挺進16強,雖然比賽中出現了
            失誤,但中場悍將馬斯切拉諾(Javier Mascherano)同樣功不可沒。 比賽剛開場10分鐘,馬
            斯切拉諾後場傳球失誤送給奈及利亞球權,不過他隨後立即上前追鏟拿回了球權。下半場51
            分鐘,馬斯切拉諾失誤為對手送上12碼罰球,致使阿根廷被扳平。但事實上從慢鏡頭的來看,
            這是否是一粒12碼罰球其實有待商榷,馬斯切拉諾本場比賽貢獻高達83次傳球,3次抄截成功
            ,3次解圍,1次過人的數據。雖然偶有失誤,但傳球成功率還是達到了87%,抄截成功率達到了
            100%。 馬斯切拉諾利用自己充沛的體力在比賽臨近結束的20分鐘時間內,保護著身後阿根
            廷的防線,彷彿又讓人們看到了利物浦時期的他。比賽結束前,馬斯切拉諾居然在拼搶中撞
            到頭部後依然不離場繼續比賽,完全展現硬漢本色。從鏡頭中我們可以看到小馬哥頭上受傷
            後的血漬,但是在這場事關生死的比賽中,他將個人的疼痛放在第二位,破了相的小馬哥來不
            及顧忌個人形象了,血染賽場仍舊英勇奮戰,在比賽的最後時刻,馬斯切拉諾與梅西
            (Lionel Messi)相擁慶祝。
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530067440
    assert parsed_news.reporter is None
    assert parsed_news.title == '鐵血硬漢!為國拼到流血破相 今夜他也是英雄'
    assert parsed_news.url_pattern == '1200118'
