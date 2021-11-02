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
    url = r'https://star.ettoday.net/news/1200577'
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
            日劇《花過天晴》是改編自《流星花園》續集漫畫,開播後掀起討論熱潮,26日播出完結篇,
            男主角平野紫耀的殺青照難得網路曝光,突破傑尼斯肖像權禁令,吸引9萬多人按讚,收視率
            以9.5%作收,除了沒有突破開播以來的新高,更被網友批評「爛尾!」 《花過天晴》以10年後
            的英德學園為故事舞台,平野紫耀飾演富二代高中生,專門在校園揪假豪門,意外和杉咲花扮演
            的破產千金激出火花。不過女方早有未婚夫中川大志,三角糾葛一路持續到完結篇,兩大男主角
            公開比賽,雙方加油陣容更是旗鼓相當。 杉咲花決定只為中川大志加油,另一方面,平野紫耀
            總是意外逆轉勝,讓比賽出現不同的結局。她最終被未婚夫鼓勵,「妳今後要順從自的想法
            而活」,終於踏出追尋真愛的一步,跑向約定的惠比壽花園廣場時,男女主角都在重複一個台詞
            「それから(接著然後)」,直到最後一秒鐘,沒有再往下描述見面之後的互動,全劇畫下
            句點。 網友追到完結篇,只見男女主角OS,高甜互動都沒出現,對此輪番批評「太沒用了吧」
            、「燃燒不完全的感覺」、「不要再然後了」、「然後到我好煩」、「喊了9次就沒了」
            、「好像在演《你的名字》!」此外也有人好奇「這是要拍電影版嗎」
            、「有續集的意思嗎?」 由於《花過晴天》結局引起正反兩面議論,網友還挖出10年前
            《流星花園》結局,道明寺和杉菜的機場跑道之吻,有人大喊「我燃燒不完全乾脆拿這個
            出來蕊」、「這才叫結局好嗎!」
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530095280
    assert parsed_news.reporter == '陳芊秀'
    assert parsed_news.title == '《流星花園》續集挨酸爛尾! 「台詞鬼打牆」網友煩到炸'
    assert parsed_news.url_pattern == '1200577'
