import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/13/1/5/n3769045.htm'
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

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            過去的12個月對微軟((US-MSFT))來說充滿了挑戰。該公司發表了 Windows 8,但銷售狀況
            差強人意。 此外,雖然它推出了 Windows Phone 8,但智慧型手機市場的市占仍低於 4%。
            在進軍雲端、硬體、線上娛樂市場,其表現也是跌跌撞撞。別以為微軟會這樣就認輸,其管
            理人才深不可測,且現金滿手。 《InformationWeek》指出,下文所述,是微軟今年為了提振
            營收,能夠做的一些事。用戶經驗 操作介面的改變,比方說取消開始鍵及新的 Metro 介面
            ,讓愛的人很愛,不習慣的人就是不習慣。某些第三方程式如 Win8StartButton,讓用戶也有
            了開始鍵的功能,不過微軟最好還是提供官方支援。 此外微軟也必須提振 app 的支援,一
            些熱門 app 如臉書及推特,都未針對 Win 8 提供程式,這點必須極力改善。 硬體 2012 年
            是微軟的硬體年,它推出了 Surface RT 平板,未來也將推出 Surface Pro,但其銷售卻不
            甚亮眼,這是由於售價達 499 美元─價格與蘋果入門 iPad 售價一樣。 微軟必須體認到一
            個新品牌必須犧牲一些事情,包括獲利。 企業服務 儘管越來越多企業投向非微軟軟體的
            懷抱,它仍必須要建構一個新的企業服務團隊,因為這是商機所在,僅靠持有Avanade 的股份
            是不夠的。 雲端 Windows 的 Azure 雲端平台,在相容性及支援性的力度必須更加
            增強。 巨量資料(Big Data) 微軟在企業客戶方面的敗退,如果能從巨量資料這塊(這當中
            涵蓋了擷取、管理、處理、整理的過程)收復失土,對於提振獲利相當有益。 Xbox 它向來是
            微軟的金雞母,如果微軟能夠將其整合進其他的產品列中,或許能夠贏得從未有過的消費者歡心
            。或許它可以嘗試以 Xbox 作為品牌推出手機,或是以遊戲鉅作 Halo 為本推出手持裝置。
            '''
        ),
    )
    assert parsed_news.category == '科技新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1357315200
    assert parsed_news.reporter is None
    assert parsed_news.title == '〈分析〉微軟2013年該做的6件事'
    assert parsed_news.url_pattern == '13-1-5-3769045'
