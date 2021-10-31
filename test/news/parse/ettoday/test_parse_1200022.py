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
    url = r'https://star.ettoday.net/news/1200022'
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
            即將於稍晚在北京發表的美圖中階旗艦機「美圖T9」,在日前官方自爆產品外觀與規格之後
            ,目前正式手機介紹官網已經上線,產品定義為「我的智慧攝影師」,在中國大陸的上市情報
            也已經公開,確認今晚9點開賣。 該款手機將會配備5.99吋三星 AMOLED 螢幕,解析度
            FHD+,搭載高通Snapdragon 660 處理器,預計提供 4GB RAM/64GB ROM與 6GB RAM/
            128GB ROM兩種版本,拍攝規格應該跟美圖V6 相同,自拍鏡頭採用1200萬畫素雙像素+副
            鏡頭500萬畫素,後置主鏡頭採用1200萬畫素雙像素(SONY IMX362)+副鏡頭500萬畫素,
            搭載的是 Android 8.1 Oreo 作業系統,搭配建立自《美圖秀秀》大數據基礎之上AI 臉部
            拍攝,官方強調該款手機「更懂得你要的好看」,電池容量3100mAh ,共有漿果紅、仙蹤綠、
            星雲粉、湖光藍四款。 除此之外,該款手機同時著重遊戲體驗跟音效,除了加入遊戲勿擾模式,
            音效方面也因為導入AKM4376獨立Hi-Fi晶片,搭配SLS雙喇叭,提供Waves音效,滿足女性
            用戶聽音樂的需求。 在AI功能方面,美圖T9全新加入語音助理 Miga,只要說一聲“Hey,
            Miga!”,語音助手 Miga 就會協助用戶設定鬧鐘、找美食、查資訊等服務,拍照時更導
            入微軟語音聲控技術,支援聲控拍照、開關閃光燈、虛化調節等指令,至於這些功能到台灣會
            以什麼形式呈現,則需要再做觀察。 至於手機代言人方面,為了宣傳電視劇《我的真朋友》,
            代言人Angelababy 已經率先在 5 月公開該款手機的實機外觀,而上市情報方面,現在在
            中國官網已經可以看到該款手機將會提供 64GB 跟 128GB 兩種版本,售價分別為 3399 元
            人民幣、4199 人民幣,折合新台幣約 1.5 萬,6 月 27 日晚上 9 點在中國大陸開賣。
            '''
        ),
    )
    assert parsed_news.category == '3C家電'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530053340
    assert parsed_news.reporter == '洪聖壹'
    assert parsed_news.title == '美圖T9售價近台幣1.5萬!配備前後雙鏡頭、導入語音助理Miga'
    assert parsed_news.url_pattern == '1200022'
