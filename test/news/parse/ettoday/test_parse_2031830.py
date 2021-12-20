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
    url = r'https://star.ettoday.net/news/2031830'
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
            Q:自上周開始航運股一反之前上漲走勢,萬海因為5月獲利不如預期率先回檔,長榮又因
            再度入監市場買賣不易,利空消息拖累整個航運股,特別是在7月13日三大巨頭又以
            跌停作收,市場殺聲隆隆,接下來怎麼看待航運股? A:自航運股下修以來,這已經是面臨到
            第二次跌停危機,在多頭市場中,只要價格是急漲噴發,就會伴隨急跌修正,特別是航運股中
            當沖比例高達一半以上,表示市場投機狀態已經形成,股價劇烈波動會成為接下來的常態,
            操作難度極高。 一般來說,跌停需要足夠時間去消化市場情緒,就七月十三日跌停鎖單量
            來看,其實佔個股成交量並不大,萬海二千多張、陽明一萬多張、長榮二萬六千張左右,
            這表示急著想賣的人並不多,跡象顯示後續會震盪,但直接跳空鎖停不太容易發生
            。 從國際局勢來看,拜登打壓航運公司消息似乎已經證實為誤傳,美國海運龍頭馬士基
            股價有回穩現象,因為塞港、缺船、缺工這些基本狀況並沒有緩解,所以長線來看,航運股
            還是有機會。 從大盤角度來看,加權指數雖然上攻萬八,但沒有站穩跡象,前期領漲的航運股
            如今出現跌停,短期若沒有新題材續接,大盤要一舉上攻難度較高,接下來如果航運股止跌或
            電子股成交佔比提升,才能有較大機會。 技術面來看,由於航運三雄股價都已跌破十日均線,
            短線走回調,但離下方支撐還有空間,K線上也尚未有止跌訊號,所以想要撿便宜的投資朋友
            還需要等待。 整體而言,大盤短線攻高不易,類股沒有領頭羊,建議手中有持股的投資朋友
            酌量減倉,想長線投資航運股的朋友等待止跌訊號再開始介入。
            '''
        ),
    )
    assert parsed_news.category == '財經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1626358260
    assert parsed_news.reporter == '方鈞'
    assert parsed_news.title == '航運股集體翻船 逃命還是等待低接?'
    assert parsed_news.url_pattern == '2031830'
