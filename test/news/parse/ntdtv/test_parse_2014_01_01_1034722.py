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
    url = r'https://www.ntdtv.com/b5/2014/01/01/a1034722.html'
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
            南蘇丹總統基爾以及反政府武裝領人馬查爾的代表抵達埃塞俄比亞,就結束血腥的內亂開始
            會談,可是在南蘇丹的一個主要城市的暴力衝突仍然在持續。 星期二,基爾和前副總統
            馬查爾都派遣代表前往埃塞俄比亞首都亞的斯亞貝巴為結束這個月初發生的戰鬥而展開
            談判。 丁卡族的基爾總統指責前副總統努爾族馬查爾試圖發動政變,隨後爆發了南蘇丹
            的民族流血衝突。 聯合國表示戰鬥導致1000多人喪生,成千上萬人流離失所。 儘管雙方
            同意舉行談判,戰鬥仍然在瓊萊省的主要城鎮博爾持續。馬查爾和他的支持者表示效忠
            他的武裝重新奪回了這個城鎮。反政府武裝曾經於這個月初短暫地控制了這個城鎮。 目前
            南蘇丹政府尚未就反政府武裝是否奪回了博爾鎮發表評論。 早些時候,基爾和馬查爾原則上
            同意舉行會談。可是,政府拒絕了馬查爾提出的條件,其中包擴要求釋放在危機發生的初期
            被關押的馬查爾的政治同盟人士。 紐奧特是參加和平談判的馬查爾代表團的一名代表。
            星期二在肯尼亞舉行的一個新聞記者會上,紐奧特再度敦促南蘇丹政府釋放被關押的
            人士。 非盟也敦促基爾政府釋放被拘禁的政治領導人,並警告說,那些繼續煽動暴力的人
            將受到制裁。 紐奧特也表示,馬查爾的代表團願意誠摯地進行談判。 路透社報導說,
            “政府間發展組織”表示,星期二雙方同意停止敵對行動。至於何時停火開始生效不得而知。
            '''
        ),
    )
    assert parsed_news.category == '國際,時政'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388505600
    assert parsed_news.reporter is None
    assert parsed_news.title == '南蘇丹政府,反政府武裝開始談判'
    assert parsed_news.url_pattern == '2014-01-01-1034722'
