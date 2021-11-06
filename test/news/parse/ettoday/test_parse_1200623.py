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
    url = r'https://star.ettoday.net/news/1200623'
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
            畢業的季節又到了,我們今天從星盤當中的太陽星座與火星星座,來看十二星座的職業選項
            。 現代的工作型態,非常多采多姿多元化,所以今天在這裡只是舉例,只要性質上有符合,都
            可以勇於嘗試喔! 牡羊座: 個性上直接不隱藏,喜歡接受挑戰。業務性質的工作,需要去
            開疆闢土的行業,都很適合牡羊座。 例如:業務人員、銷售人員、軍警消防人員、運動員、
            電競選手。 金牛座: 能夠不疾不徐慢慢來、穩定且能夠運用感官知覺的工作,適合金牛
            座好好發揮。例如:諮商輔導員、美容與化妝品產業、市內設計與裝修、花卉工作者。 雙子
            座: 活潑、擅長訊息搜集與傳遞,能夠因人而異的表達是雙子座的特質。適合的行業性
            質為:講師、新聞媒體工作者、統計分析家、導遊或旅遊規劃諮詢人員。 巨蟹座: 總是
            有媽媽的感覺,非常懂得如何關懷照顧他人的巨蟹座,適合的工作特質如:餐飲或飯店行業、
            與食物有關的工作、幼保教育工作者、居家照顧工作者。 獅子座: 充滿熱情又能夠帶動
            週遭氣氛的獅子座,適合如:表演工作者、廣告行銷業、休閒娛樂產業、兒童用品業之類的
            工作。 處女座: 細心、懂得舉一反三又有耐心是處女座的特質,所以例如:會計工作、稽
            核、倉儲管理、金融投資業等,都是適合處女座的行業。 天秤座: 懂得好好打扮自已的
            外表,也懂得拿捏社交分寸的天秤座,適合的工作有:設計業、手作手工藝業、接待專員、人
            事管理、芳療業。 天蠍座: 能夠長期忍受獨處而專心工作,是天蠍座的一大特質,因此例
            如:醫師、分析師、心理研究、調查員、保險業等,都能夠讓天蠍座有很好的發揮。 射手
            座: 看似豪放不羈,事實上對生命有著一套自己想法的射手座,適合的工作有:旅遊業、新聞
            工作者、老師教授、出版業、國際貿易業等工作領域。 摩羯座: 只要立定目標,便能夠
            很有耐心慢慢抵達的摩羯座,適合從事例如:建築設計業、土地開發業、工程師、科研人員
            等性質的工作。 水瓶座: 重視思維邏輯,但又能夠跳脫舊有思維,是水瓶座的特質,因此
            例如:程式設計人員、資訊領域、網路工作者、社會工作者、新創領域。都是水瓶座能夠好
            好發揮的領域。 雙魚座: 充滿愛心與善良的心,能夠為他人的處境感同身受,是雙魚座的
            天賦,可以考慮:醫護工作、治療師、精神醫學、藝術領域、影音工作、舞蹈等行業。
            '''
        ),
    )
    assert parsed_news.category == '運勢'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530313200
    assert parsed_news.reporter == 'Amanda'
    assert parsed_news.title == '12星座看職業!牡羊適合打電競、雙魚天生心理師'
    assert parsed_news.url_pattern == '1200623'
