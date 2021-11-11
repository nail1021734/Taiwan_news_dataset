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
    url = r'https://www.epochtimes.com/b5/20/11/9/n12536603.htm'
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
            陸媒報導,中國恆大集團與深深房集團11月8日晚宣布,兩者之間的重大資產重組計劃終止
            。此案創下中國股市重組暫停交易的最長時間紀錄,整整超過4年。 第一財經報導,兩家
            集團8日晚發布的公告,也代表中國恆大旗下的恆大地產,4年來想要回歸A股上市之路,正式
            宣告終結。 深圳經濟特區房地產股份有限公司(深深房)公告稱,基於目前市場環境等原因
            ,現階段繼續推進重大資產重組的條件尚不成熟,為切實維護公司及全體股東利益,經公司
            審慎研究並與交易各方友好協商,公司決定終止本次交易事項,深深房股票自9日起恢復交易
            。 恆大地產與深深房的重組事宜,最早發軔於2016年9月14日,當時深深房股票開始暫停
            交易。同年10月3日,恆大地產與深深房簽署「關於重組上市的合作協議」,深深房以發行
            A股股份及或支付現金的方式購買恆大地產100%股權。交易完成後,恆大地產將實現A股
            上市。 到了2017年,恆大地產完成三輪增資,戰略投資者合計向恆大地產投入人民幣1300億
            元資本金,共獲得恆大地產擴大股權後約36.54%權益,凱隆置業(恆大中國全資子公司)則
            持股63.46%權益。 當時因為對回歸A股有信心,恆大在戰略投資設置對賭條款,預設的重組
            時間周期為3年,後來又順延一年至2021年初。 根據合約,如果能在約定時間內完成重組
            ,戰投投資人有權要求凱隆置業及恆大集團董事局主席許家印回購相應股權,或者由
            凱隆置業無償向戰略投資者轉讓部分恆大地產股份。 今年9月,中國恆大傳出資金有困難
            ,希望廣東政府支持其與深深房的重大資產重組案。不過,恆大對此否認並報警。 到了
            9月29日,恆大地產與1300億元戰略投資中的863億元戰投簽訂補充協議,戰投同意轉為
            普通股權長期持有,且股權比例保持不變。 中國恆大在11月8日晚的最新公告提及剩餘
            戰投資金的安排情況:其中,357億元戰略投資者也已商談完畢,即將簽訂補充協議;50億元
            戰略投資者由於涉及其自身大股東的資產重組,正在商談;剩餘30億元戰略投資者的本金
            ,集團已支付,即將回購。 報導稱,此舉意味著,恆大原本需要在2021年1月31日前履行的
            1300億戰略投資的回購義務,絕大部分已經「一筆勾銷」。同時,恆大地產布局逾4年的A股
            上市之路,也正式宣告終結。
            '''
        ),
    )
    assert parsed_news.category == "大陸新聞,中國經濟"
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1604851200
    assert parsed_news.reporter is None
    assert parsed_news.title == '恆大資產重組計劃告終 A股上市之路宣告終結'
    assert parsed_news.url_pattern == '20-11-9-12536603'
