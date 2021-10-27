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
    url = r'https://www.ntdtv.com/b5/2011/07/27/a565336.html'
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
            台資企業大潤發和法國歐尚集團合資的「高鑫零售」,今天正式在香港聯合交易所掛牌。
            高鑫以港幣7.2元(約新台幣26.6元)上市,開盤即跳升至9.05元港幣(約新台幣
            33.5元)。 高鑫股價隨後在港交所上午盤中期間,普遍以高於掛牌價3成交易,高鑫執行
            董事兼大潤發(中國)董事長黃明端對首日上市股價表現認為,股價是一時,經營是長期,股價
            表現顯示投資者還是肯定高鑫。 對於外界質疑潤泰集團需要現金,會否影響高鑫的營運,
            黃明端指出集團營運資金充裕,增資後會更充裕,集團運作不會受到影響。 高鑫上市比原定
            時間晚了12天,集團首席執行官兼歐尚(中國)董事長梅思勰(Bruno Mercier)表示,從股價
            表現看,上市過程還是很成功。梅思勰說,歐尚和大潤發在大陸合作超過10年,早已習慣彼此,
            雙方會繼續合作。 至於大潤發和歐尚共同持股高鑫的股權分配爭議,黃明端說,從經濟角度
            來看,大潤發仍是大股東,上市後新股東增加,股權結構改變,「還得再算」。 高鑫零售原定
            7月15日在香港上市,但由於大潤發股權今年由1股分拆至26股,稀釋後的股份與高鑫零售
            重組後的股數計算錯誤,導至每股盈餘(EPS,Earnings Per Share)出現誤差,港交所
            擔心投資人被錯誤資訊誤導,要求延後上市。 高鑫零售6月公開定價後,獲得散戶41倍及
            機構投資者15倍認購的佳績,延後掛牌散戶認購受到影響。
            '''
        ),
    )
    assert parsed_news.category == '財經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1311696000
    assert parsed_news.reporter is None
    assert parsed_news.title == '高鑫香港掛牌 股價走高3成'
    assert parsed_news.url_pattern == '2011-07-27-565336'
