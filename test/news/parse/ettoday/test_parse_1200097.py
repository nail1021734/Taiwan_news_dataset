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
    url = r'https://star.ettoday.net/news/1200097'
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
            一部好的電影,一定要有這樣幾個特徵:主角出場,過程起伏一波三折,而懸念在最後時刻才
            會宣告破解,結局又恰恰是觀眾們想看到的。6月27日凌晨,世界盃D組最後一輪,四支球隊共
            同上演了這樣一部梅西起死回生記,情節發展完全符合大片的標準,彷彿早就寫好了
            劇本。 阿根廷贏球+冰島輸球,這是主角逃出生天的前提,一切終於如阿根廷球迷所願,
            絲絲入扣,分毫不差。主角早早奠定了本片的基調,梅西(Lionel Messi)精巧的一停一帶,
            並用右腳打破僵局。另一邊,冰島人的兩次威脅射門,則考驗著觀眾們的神經,要知道,如果冰島
            拿下3分,阿根廷不光要贏,還必須比他們多拿2個淨勝球才行。 下半場,攪局的“反派”出現了,
            土耳其主裁判法基爾搶走了風頭,馬斯切拉諾(Javier Mascherano)那個在防守時很常見的
            動作,卻被極端嚴厲的判了12碼罰球,奈及利亞扳平比分,阿根廷又被吊在了懸崖邊,法基爾
            後來一度想徹底搶戲,調出VAR檢視羅霍的禁區手球,但畢竟這不符合大片的劇情發展需要,
            反派終於還是沒那個膽把自己變成主角。 奈及利亞反擊中一次次威脅阿根廷大門、但就是
            射不進,如果你是資深老影迷,肯定會產生某種熟悉的預感,主角發出致命一擊前,總會被對方
            追得抱頭鼠竄。果然,第86分鐘,羅霍(Marcos Rojo)致命一擊,觀眾高聲喝彩,這是阿根廷
            都在等待的一幕,也是精彩劇本最完美的結局。
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530064920
    assert parsed_news.reporter is None
    assert parsed_news.title == '梅西起死回生 峰迴路轉劇情就像是早寫好'
    assert parsed_news.url_pattern == '1200097'
