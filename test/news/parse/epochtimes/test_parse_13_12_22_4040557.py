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
    url = r'https://www.epochtimes.com/b5/13/12/22/n4040557.htm'
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
            俄羅斯最著名的犯人、前石油大亨霍多爾科夫斯基(Michail Chodorkowski)獲釋抵達柏林
            後,於12月22日舉行了記者招待會,他表示,將為俄國的政治犯獲得自由而努力。現階段他暫
            時不會回莫斯科。 不再介入政治 普京不會第二次放過我 霍多爾科夫斯基表示,雖然他的
            特赦並沒有附加什麼條件,但他在另外一封信裏告訴普京,一、不再參與政治;二、不追究自
            己石油公司財產問題。他對一家俄國雜誌表示,如果他回國,當局有可能不會放他第二次出
            國,因為「他們可以找出太多的理由」抓住他。 至於他今後的去向,他還需要時間考慮。他
            暫時沒有重回商界的打算,因為他當石油公司總裁時,事業上已經達到了想達到的目標,也無
            需為今後的生計考慮。他將與太太商量,住在哪裏。他的第二任太太住在瑞士,他們育有三
            個子女。霍多爾科夫斯基的第一任妻子給他生了一個兒子,現年27歲,生活在紐約。在霍多
            爾科夫斯基到達柏林的當晚,他就與大兒子見面了。 霍多爾科夫斯基到達柏林的第二天,他
            的父母也從莫斯科趕到柏林。身患癌症的老母親非常激動,她以為此生再也見不到兒子了,
            十年來第一次抱著兒子,她久久不肯鬆開。 感謝德國前外長根舍的努力 霍多爾科夫斯基獲
            得特赦,這條消息在媒體上像一股旋風從無到有突然冒出來,但是這其實是多方長期不懈努
            力的結果。 德國媒體報道,86歲的根舍早在普京再次當選俄國總統時就開始為霍多爾科夫
            斯基獲得自由而奔走,而且他得到了總理默克爾的支持。根舍多次前往莫斯科,並於2012年6
            月以及今年1月,兩次與普京會面。根舍今年11月份還起草了特赦申請書,並一手安排了到柏
            林的飛機。 根舍表示,整個過程有一定難度,因為霍多爾科夫斯基拒絕流亡,也拒絕遞交特
            赦申請,因為他認為,那就表明他認錯服輸了。現在霍多爾科夫斯基出於「家庭原因」,請求
            獲得特赦,因為他的母親身患癌症,在德國治療。 霍多爾科夫斯基自稱,這完全不代表他認
            錯了。 乘坐德國商人私人飛機飛奔自由 根舍多方走動,周密安排。很早他就請北威州一位
            商人朋友幫忙,出借其私人飛機。兩個月前又請這位商人朋友隨時做好準備。普京簽署了霍
            多爾科夫斯的特赦令後,根舍立即讓德國商人的飛機到莫斯科接前石油大亨來德國,他本人
            也親自到機場迎接。他把前俄國最有錢的大亨送到柏林五星級酒店「阿德龍」,一起喝了一
            杯伏特加,便悄悄退出來了。根舍表示,要留給霍多爾科夫斯基時間,讓他與家人團聚。 據
            稱,霍多爾科夫斯基獲得了德國一年的簽證,可以自由在申根地區活動,去瑞士及美國都沒有
            問題。 現年50歲的霍多爾科夫斯基於12月20日獲得特赦,他說當天淩晨2點得知自己要被釋
            放的消息,下午就飛往柏林。在記者招待會上,他似乎對自己獲釋的內幕並不十分清楚,對外
            界的變化也頗有距離感。霍多爾科夫斯基是前尤科斯石油公司總裁。他在為反對黨提供資
            金後,先後在2005年和2010年兩次被判刑,罪名包括詐騙、盜竊、逃稅、挪用公款和洗錢等,
            刑期13年,還有八個月就可以出獄。他的支持者一直聲稱他是一名政治犯。外界普遍認為,
            普京提前特赦他,是試圖在2014年2月索契冬奧會前,化解國際社會對俄人權記錄的壓力。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1387641600
    assert parsed_news.reporter == '余平德國,賈南'
    assert parsed_news.title == '前俄石油大亨柏林開新聞發布會 暫不回莫斯科'
    assert parsed_news.url_pattern == '13-12-22-4040557'
