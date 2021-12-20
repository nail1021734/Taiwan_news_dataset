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
    url = r'https://www.epochtimes.com/b5/13/2/22/n3806891.htm'
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
            谷歌正在舉辦一場比賽,贏者有機會購買一副可上網的谷歌眼鏡(Google Glass)。 想取得
            參賽資格嗎?你必須住在美國,還必須提交50個字的申請告訴谷歌你打算用這眼鏡做甚麼。
            另外眼鏡不白送,你要為眼鏡支付1500美元。申請截止日期是2月27日。 要想參加動作要快
            。不然2014年以後谷歌才會在大眾市場上銷售谷歌眼鏡噢。 谷歌眼鏡位於所謂「可穿戴
            計算技術」新浪潮的最前沿。谷歌眼鏡能處理大部份與智能手機相同的任務,不同點是響應
            語音命令,而不是響應手指觸摸屏幕。 2月20日谷歌發佈了一段視頻,向人們展示戴著谷歌
            眼鏡跳傘、坐過山車、滑雪、騎馬,甚至乘坐熱氣球升空。 谷歌雖然不急於將「眼鏡」上市,
            不過正在努力造勢宣傳它最近幾年在個人計算領域的最新成果之一。 這種眼鏡的右眼上方的
            邊緣有一個微小的顯示屏幕,運行谷歌移動設備Android操作系統。 谷歌曾表示,「大眾
            市場版」的谷歌眼鏡價格將低於1,500美元,不過高於智能手機。 獲獎者將獲得「探險者」
            版本的谷歌眼鏡,這款眼鏡預計將於明年走進大眾市場,去年6月份,已經有一些電腦程序員
            快手先得,他們也付了1500美元。 獲獎者3月中下旬會收到通知,需要前往紐約、洛杉磯或
            舊金山灣來迎接這款眼鏡。 操作谷歌眼鏡不需要用手,拍照或錄製視頻時更加方便,想拍就拍,
            說話就行。網上搜索也一樣容易,只要動嘴告訴谷歌眼鏡找哪條信息。智能手機和平板電腦用
            的谷歌Andr​​oid系統已經具備語音搜索功能。 谷歌眼鏡有五種顏色可供選擇:炭黑、橘色、
            巖灰、棉白和天藍色。 為了衡量人們將如何使用谷歌眼鏡,谷歌鼓勵參賽者用谷歌的應用程序
            提供多達五張照片和15秒的視頻,但不要有任何裸露或暴力鏡頭。谷歌說,「不要提交你媽媽不願意
            見到的東西。」 去年6月在公司會議上,谷歌聯合創始人謝爾蓋.布林(Sergey Brin)承認,
            該公司仍然在修正錯誤,並努力延長眼鏡的電池壽命。谷歌眼鏡於2010年開始研發,那时還
            作為秘密保守。現在,谷歌眼鏡已經不再是一個秘密,布林經常在公共場合戴著它。最近他
            佩戴谷歌眼鏡出席了醫學和生物學傑出成就獎金創立會。
            '''
        ),
    )
    assert parsed_news.category == '科技新聞,IT 動向'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1361462400
    assert parsed_news.reporter == '沙莉,畢儒宗'
    assert parsed_news.title == '谷歌眼鏡將上市 谷歌設大賽分享新奇用法'
    assert parsed_news.url_pattern == '13-2-22-3806891'
