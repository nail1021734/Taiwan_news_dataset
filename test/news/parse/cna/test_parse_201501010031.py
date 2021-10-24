import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201501010031.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            死傷數字,更新為36死47傷。 大陸上海外灘昨夜發生的跨年活動踩踏事故,造成35人
            死亡,至少48人受傷。在已查明身分的39名傷者中,有3名台灣人。 根據人民日報官方
            微博,35名死者中,男性10名、女性25名。截至發稿為止,查明身分的死者已有10人,年齡
            最大的36歲、最小16歲。傷者中,已查明身分的有39人,其中台灣3人,馬來西亞1人。 上海
            市政府新聞辦公室透過微博發布,踩踏事件受傷人數增至48人。 新華網報導,上海市第一
            人民醫院、瑞金醫院等救治傷者的醫生表示,傷者大多數都是20歲左右的年輕人,基本沒有
            中老年傷者。 傷亡者中以年輕女性居多,有包括復旦大學在內的大學學生,也有兒童。目前
            救治的最小年齡傷者是1998年出生。 上海跨年人潮洶湧,上海地鐵統計,到2014年12月
            31日晚間10時40分為止,單日地鐵客流就超過1003萬人次,刷新紀錄。 上海市政府新聞
            辦公室表示,中共上海市委書記韓正、上海市長楊雄連夜部署全力做好傷員搶救和善後
            處置等工作。韓正、楊雄第一時間趕往長征醫院、第一人民醫院、瑞金醫院、黃浦區中心
            醫院,看望傷員,要求全力以赴救治。事故原因正在調查中。 新民網報導,新民晚報新民
            網記者在醫院看到,有關方面開始為在現場焦急等候消息的家屬登記訊息。警方現場負責人
            表示,由於事件中的傷者被分別送往多家醫院,情況相對復雜,因此要求等待的家屬現場登記
            尋人信息。凌晨4時30分許,一名傷者被保安推出。這位年輕的傷者坐在輪椅上,身上背著
            雙肩包,沒有穿外套,右腳沒有穿鞋子,褲子膝蓋處有污跡。傷者說,他與朋友一起去外灘
            跨年,沒想到發生了不幸,而他的朋友還在急診室內搶救。 網友@小鐵煉鋼ing當時在外灘
            踩踏事件的現場,拍下了現場影片說,當時人很多,現場警方在維持秩序不讓靠近,周圍有人
            自發手拉手擋住人潮為傷者留出安置的地方,和救護車救治的通道。 網友@iiiiisay 回憶
            說,當時人真的是太多,只能隨著一波又一波人流隨波逐流,完全不知自己被擠去哪,交警都
            手拉手築成人牆還是被沖破好多次,後來發生踩踏,都沒辦法好好把人送下來,一個又一個從
            樓梯上遞下來的。 根據上海市政府新聞辦公室發布消息,上海跨年夜發生踩踏慘劇,至今天
            凌晨5時,已造成35人死亡,43人受傷。 2014年12月31日晚間11時35分,上海市黃浦區
            外灘陳毅廣場發生擁擠踩踏事故。 上海踩踏意外 目擊者:有人樓上拋美金 據一位上海
            外灘踩踏意外事件的目擊者表示,12月31日晚間11時50分左右,外灘18號樓的樓上有人向
            樓下拋撒美金紙鈔,造成人群哄搶,行人駐足圍觀及起鬨。 鳳凰網報導,這位安徽籍年輕人
            吳濤說,他是這件意外事件的親身經歷者,當時有人從樓上拋撒美金。 跨年夜,上海外灘
            發生踩踏意外事故,目前已造成35人死亡、42傷。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1420041600
    assert parsed_news.reporter == '台北,台北,高照芬上海'
    assert parsed_news.title == '上海跨年夜踩死人 釀35死48傷'
    assert parsed_news.url_pattern == '201501010031'
