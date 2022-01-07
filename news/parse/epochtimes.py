import re
from datetime import datetime
from typing import List, Tuple

from bs4 import BeautifulSoup

import news.parse.util.normalize
from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

# Some times paragraph contains figures and captions.  Figure captions are
# repeated and useless, so we remove figures along with captions.
# This observation is made with `url_pattern = 14-1-1-4048433,
# 13-8-12-3938760`.
ARTICLE_DECOMPOSE_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    figure, figcaption
    ''',
)

# News articles are located in `div#artbody`, and all of them are either `p` or
# `h2` tags.  `h2` tags represent section header and `p` tags represent normal
# paragprah.
# This observation is made with `url_pattern = 21-10-27-13332627,
# 14-1-1-4048433`.
#
# For category `視頻集錦`, news articles are located in
# `div#artbody > div#article_wrap`.  In this case `p` and `h2` still act the
# same as normal news.
# This observation is made with `url_pattern = 13-2-23-3807193`.
#
# For category `文化網`, news articles are located in
# `div.whitebg > :is(p, h2)`.  In this case `p` and `h2` still act the same as
# normal news.
# This observation is made with `url_pattern = 13-8-20-3945076`.
ARTICLE_SELECTOR_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    div#artbody > :is(p, h2),
    div#article_wrap > :is(p, h2),
    div.whitebg > :is(p, h2)
    ''',
)

# News title is located in `h1.title`.
# This observation is made with `url_pattern = 21-10-27-13332627,
# 2011-04-12-517548`.
TITLE_SELECTOR_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    h1.title
    ''',
)

###############################################################################
#                                 WARNING:
# Patterns (including `REPORTER_PATTERNS`, `ARTICLE_SUB_PATTERNS`,
# `TITLE_SUB_PATTERNS`) MUST remain their relative ordered, in other words,
# the order of execution may effect the parsing results. `REPORTER_PATTERNS`
# MUST have exactly ONE group.  You can use `(?...)` pattern as non-capture
# group, see python's re module for details.
###############################################################################
REPORTER_PATTERNS: List[re.Pattern] = [
    # This observation is made with `url_pattern = 13-12-23-4041274,
    # 14-1-1-4048455, 14-1-1-4048450, 13-12-31-4046950, 13-12-30-4046025,
    # 13-12-13-4033178, 13-12-11-4031411, 13-12-9-4030334, 13-7-21-3921942,
    # 13-3-12-3820892, 13-3-1-3811503, 13-2-20-3804661, 20-11-9-12536603
    # 20-11-5-12528186`.
    re.compile(
        r'[\[\(]?\s*(?:[這这]是|英文)?[新大][紀纪]元(?:.{1,2}洲)?(?:[週周]刊\d*?期?,?)?(?:資'
        + r'深)?[記记]?者?站?' + r'(?:亞太)?(?:[電电][視视][台臺]?)?'
        + r'([\w、/\s]*?)[的综綜合整理採采訪访編编譯译報报導导道告訊讯]+?[,。]?(?:/\S+?)?\s*[\]\)]'
    ),
    # This observation is made with `url_pattern = 13-2-10-3798072,
    # 19-12-13-11720728`.
    re.compile(
        r'[\(【]大[紀纪]元?[\w]*[記记]者([\w、,/\s]*?)(?:美國.*?)?(?:採訪|編譯)?(?:報導)?[\)】]'
    ),
    # This observation is made with `url_pattern = 12-8-12-3657466,
    # 12-7-3-3626870`.
    re.compile(r'\((?:北美)?(?:晚間)?責任編輯\W?([\w、/\s]*?)\)'),
    # This observation is made with `url_pattern = 19-12-15-11724303`.
    re.compile(r'[\d]*月[\d]*日[,]([\w]*)報導[,]'),
    # This observation is made with `url_pattern = 19-2-1-11017679`.
    re.compile(r'[\(【][記记]者([\w、,/\s]*?)(?:美國.*?)?(?:採訪|編譯)?(?:報導)?[\)】]'),
    # This observation is made with `url_pattern = 19-12-29-11753517`.
    re.compile(r'作者:[\w]*\s*/\s*整理:(\w*)・大紀元'),
    # This observation is made with `url_pattern = 19-12-5-11702167`.
    re.compile(r'文:[\w]*\s?\|\s?翻譯:(\w*)'),
    # This observation is made with `url_pattern = 19-12-4-11700004`.
    re.compile(r'(?:文|編譯):(\w*)・大紀元'),
    # This observation is made with `url_pattern = 19-11-18-11662852`.
    re.compile(r'\(大紀元記者(\w*)\(.*\)報導/[\w]*編譯 \)'),
    # This observation is made with 'urs_pattern = 19-12-5-11701493,
    re.
    compile(r'\(英文大紀元資深記者(\w*)\(.*\)採訪報導/[\w]*編譯\)英文《大紀元.*》資深記者\w*\([\s\w]*\)'),
    # This observation is made with 'urs_pattern = 19-12-20-11735692,
    re.compile(r'\(英文大紀元專欄作家([\w\s]*)撰寫,\w*編譯\)'),
    # This observation is made with 'urs_pattern = 19-4-22-11205994,
    re.compile(r'\(英文大紀元記者([\w\s]*)採訪,\w*編譯\)'),
    # This observation is made with `url_pattern = 19-11-2-11628263`.
    re.compile(r'^文:(\w*)\s?\|\s?圖:[\w\s]*'),
    # This observation is made with `url_pattern = 19-10-23-11606025`.
    re.compile(r'【大[紀纪]元[^】]*?[訊讯]】?文:(\S*?)\s'),
]
ARTICLE_SUB_PATTERNS: List[Tuple[re.Pattern, str]] = [
    # Remove list symbols.
    # This observation is made with `url_pattern = 13-12-14-4034056,
    # 13-12-13-4033481, 13-12-9-4030017, 13-12-7-4028473, 13-7-29-3928497,
    # 13-3-3-3813641, 13-2-1-3790819, 13-1-5-3769045`.
    (
        re.compile(r'([。\s])(※|•|●|★|◎|\*|■)\s*'),
        r'\1',
    ),
    # Remove useless symbols.
    # This observation is made with `url_pattern = 13-9-21-3969060,
    # 13-8-7-3935864, 13-3-3-3813641, 13-2-27-3810705, 13-2-27-3810566,
    # 13-8-20-3945076, 13-2-18-3803627`.
    (
        re.compile(
            r'(◇|□|\[\[\d+\]\]|\?{2,}|\?\*|\(未?完?待?[續续]?(前文)?[圖图]?\)|'
            + r'\(?[註注][\d一二三四五六七八九十]+:?\)?)'
        ),
        '',
    ),
    # This observation is made with `url_pattern = 13-8-20-3945076`.
    (
        re.compile(r'@?\s*[註注][釋释]:'),
        '',
    ),
    # This observation is made with `url_pattern = 13-8-20-3945076`.
    (
        re.compile(r'@\*?#'),
        '',
    ),
    # This observation is made with `url_pattern = 20-1-1-11760821`.
    (
        re.compile(r'@\*'),
        '',
    ),
    # This observation is made with `url_pattern = 13-1-2-3767198`.
    (
        re.compile(r'([。!])@'),
        r'\1',
    ),
    # News copy source.  Parentheses must show up in the begining and the end
    # of the pattern.
    # This observation is made with `url_pattern = 14-1-1-4047920,
    # 13-12-31-4047555, 13-12-31-4047176, 13-12-31-4047058, 13-12-30-4046768,
    # 13-12-28-4044667, 13-12-12-4032207, 13-12-12-4032203, 13-12-19-4037847,
    # 13-12-7-4028971, 13-3-4-3813779, 13-3-1-3812338, 14-1-1-4048450,
    # 14-1-1-4047920, 13-12-26-4043823, 13-2-27-3810172`.
    (
        re.compile(
            r'\([據据轉转]?《?'
            + r'(新[唐塘]人|中央社?|BBC|法[國国廣广]|自由|[美德][國国]之[音聲声]|[台民][視视]|明慧)'
            + r'[^)]*?([電电報报導导道稿社網网])?\)\s*\??',
        ),
        '',
    ),
    # This observation is made with `url_pattern = 14-1-1-4048450,
    # 13-7-30-3928877, 13-2-27-3810172`.
    (
        re.compile(
            r'以上是(自由[亞亚]洲[電电][台臺]|[法美德][國国]之[音聲声]).*?[報报][導导道]。?',
        ),
        '',
    ),
    # This observation is made with `url_pattern = 13-12-15-4034574`.
    (
        re.compile(
            r'\([詳详][細细][報报][導导道][內内]容[請请][見见].*$',
        ),
        '',
    ),
    # This observation is made with `url_pattern = 13-2-7-3795671`.
    (
        re.compile(
            r'\(見文藝復興盛期.*$',
        ),
        '',
    ),
    # Remove news article references.  References might have nested parenthese.
    # This observation is made with `url_pattern = 12-6-25-3620245,
    # 13-6-22-3899772, 13-3-16-3823858`.
    (
        re.compile(
            r'\((事?[據据]|[見见]|出自)([^(]*?\([^)]*?\))*?[^)]*?\)',
        ),
        '',
    ),
    # This observation is made with `url_pattern = 13-3-3-3813542`.
    (
        re.compile(r'\(本文[附有帶带影音照相片及和與与]+\)'),
        '',
    ),
    # This observation is made with `url_pattern = 13-8-12-3938760`.
    (
        re.compile(r'\([^)]*?[攝摄]影[報报][導导道]\)'),
        '',
    ),
    # This observation is made with `url_pattern = 14-1-1-4048382,
    # 13-12-26-4043823, 13-8-7-3935510, 13-2-27-3810619`.
    (
        re.compile(r'[\(〈]([實实][習习])?[編编]?[譯译議议]者?[:;][^)]*?\)'),
        '',
    ),
    # Note that `ord('–') == 8211`, `ord('—') == 8212` and `ord('─') == 9472`.
    # This observation is made with `url_pattern = 13-12-23-4041274,
    # 13-2-15-3801677, 13-8-20-3945076, 13-6-6-3887756, 13-2-9-3797609,
    # 13-3-10-3818921, 13-12-1-4023601`.
    (
        re.compile(r'[\-—–─]*\(?(本文)?(摘[編编]|取材|[轉转]|原)[載载自]+[^,]*?$'),
        '',
    ),
    # This observation is made with `url_pattern = 13-9-21-3969060`.
    (
        re.compile(r'\([^)]*?來稿\)'),
        '',
    ),
    # This observation is made with `url_pattern = 13-12-22-4040557,
    # 13-8-13-3939870, 20-10-10-12466941`.
    (
        re.compile(
            r'([瞭了]解|更多)德[國国].*?'
            + r'大[紀纪]元[歐欧]洲生活[網网]:\s*(https?://)?www\.dajiyuan\.eu',
        ),
        '',
    ),
    # URL pattern was found in
    # https://stackoverflow.com/questions/7109143/what-characters-are-valid-in-a-url
    # This observation is made with `url_pattern = 13-12-12-4032764,
    # 13-2-22-3806891, 13-2-8-3796686, 13-1-15-3777183`.
    (
        re.compile(
            r'([圖图]|申[請请][網网]址|[專专][业業家]版):\s*(\(同[測测][試试]版\))?\s*'
            + r'''(https?://[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;%=]+\s*)+''',
        ),
        ' ',
    ),
    (
        re.compile(r'─+[點点][閱阅]\s*【.*?】\s*─+'),
        '',
    ),
    # This observation is made with `url_pattern = 13-6-6-3887756`.
    (
        re.compile(r'\(?[點点][閱阅]\s*【.*?】\s*(系列文章)?。\)?'),
        '',
    ),
    # This observation is made with `url_pattern = 20-10-10-12466941.'
    (
        re.compile(r'接上文:(.*?)\(\d\)'),
        r'',
    ),
    # This observation is made with `url_pattern = 13-2-23-3807193`.
    (
        re.compile(r'看更多文章»'),
        '',
    ),
    # This observation is made with `url_pattern = 13-1-6-3769836`.
    (
        re.compile(
            r'李進具三十餘年汽車維修保養經驗,對汽車買賣也很熟悉。如果您有汽車維修與保養方面'
            + r'的問題,歡迎發信至car_qna@epochtimes\.com,本報將轉發李進解答。來信請註明'
            + r'汽車型號、牌子及年份。'
        ),
        '',
    ),
    (
        re.compile(r'(本文|影片)網址為?:?\s*.*$'),
        '',
    ),
    # This observation is made with `url_pattern = 20-8-31-12371094
    # 20-9-21-12420158, 19-12-27-1174817, 19-12-27-11749380`.
    (
        re.compile(r'(【[^】^語^(直播)]*?】)+'),
        '',
    ),
    # This observation is made with `url_pattern = 20-9-21-12420158`.
    (
        re.compile(r'\(-?待續-?\)'),
        '',
    ),
    # This observation is made with `url_pattern = 13-7-21-3922412`.
    (
        re.compile(r'【大[紀纪]元[^】]*?[訊讯]】?'),
        '',
    ),
    # This observation is made with `url_pattern = 13-3-3-3813123`.
    (
        re.compile(r'\([大新][紀纪]元[週周]刊\d+期\)'),
        '',
    ),
    # This observation is made with `url_pattern = 13-3-4-3814165
    # 19-12-5-11702167`.
    (
        re.compile(r'\(?(https?)?:?(//)?www[\-\.\\a-z]*\)?'),
        '',
    ),
    # Email pattern was found in
    # https://stackoverflow.com/questions/2049502/what-characters-are-allowed-in-an-email-address
    # This observation is made with `url_pattern = 13-1-25-3785356`.
    (
        re.compile(
            r'[聯联][絡络]本文作者[請请][發发][郵邮]件到:\s*'
            + r'''[a-z0-9!#$%&'*+\-/=?^_`{|}~."(),:;<>@[\\\]]+@[a-z0-9\-.]+''',
            re.IGNORECASE,
        ),
        '',
    ),
    # This observation is made with `url_pattern = 21-10-27-13332627,
    # 14-1-1-4048468, 14-1-1-4048456, 14-1-1-4047776, 13-12-15-4034530,
    # 13-8-5-3933454, 19-12-25-11743970`.
    (
        re.compile(r'[\(@]?\*?\s*[責责]任?[編编][輯辑]?.*?[:;].*$'),
        '',
    ),
    # This observation is made with `url_pattern = 13-7-24-3924107,
    # 13-2-20-3804582`.
    (
        re.compile(r'\(?([視视][频頻]|[攝摄]影)[:;][\S]+\)?'),
        '',
    ),
    # This observation is made with `url_pattern = 13-7-21-3921942`.
    (
        re.compile(r'(ph|f)oto\s*[:;][:a-z\s]+', re.IGNORECASE),
        '',
    ),
    # This observation is made with `url_pattern = 20-1-1-11759086
    # 19-5-14-11256874, 19-4-24-11211180, 19-5-3-11232743, 19-4-25-11212947,
    # 19-4-23-11206720, 19-4-21-11201750, 19-1-4-10954370,
    # 19-12-26-11746439, 19-11-25-11678991, 19-12-24-11743464,
    # 19-12-27-11750145, 19-12-30-11754661, 20-1-1-1176083, 19-12-29-11753517,
    # 19-12-28-11751599, 19-12-18-11729919, 19-9-4-11497783,
    # 19-12-11-11715330, 19-12-7-11707556, 19-12-2-11694728,
    # 19-11-28-11688048, 19-11-24-11677348, 19-11-2-11629034,
    # 19-11-2-11628263, 19-10-11-11581844`.
    (
        re.compile(
            r'(⊙Ending|網絡收看方式|【直播日期】|《大紀元》讀者還享有|\s*謝謝大家!'
            + r'\s*追查迫害法輪功國際組織\s*|下面是視頻直播。|如果您有相關問題|\s*[_'
            + r'=]{10,}|\(原文轉自美房置業網|[◊\s@]*選自《明慧針道|\(本系列完'
            + r'結\) 點閱|註:全文鏈接|事據《.*》(後集)?卷?\w?、?|[\w]*小檔案|\s*\(?[此'
            + r'本]文(?:(此文)?發表|刊載)於[\w\d]*(?:理財|新聞|教育|B4|論壇)版\)?'
            + r'|(\(節錄完\))?\s*[—─]\s*[—─](?:節(?:錄|選)|摘)自|陳彥玲博士(【爸'
            + r'媽必修課】)?|參考資料|【作者簡介】|要瞭解更多有關《.*》|▼|本文作者).*'
        ),
        '',
    ),
    # This observation is made with `url_pattern = 13-8-3-3932270,
    # 13-7-29-3928497, 13-3-6-3816184, 13-3-9-3818323, 12-7-30-364941`.
    (
        re.compile(r'(\W)\(?([參参]考)?[資资]料([來来]源)?[:《][^)]*?(\)|$)'),
        r'\1',
    ),
    # This observation is made with `url_pattern = 13-2-24-3807746`.
    (
        re.compile(r'文:\S*?$'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-22-11738876,
    # 19-5-19-11266537`.
    (
        re.compile(r'\s?文字整理:\w*[,。]?(視頻製作:\w*[,]?)?$'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-17-11728852,
    # 19-12-27-11750457, 19-12-31-11758753 19-12-31-11756845,
    # 19-12-28-11751781, 19-12-13-11719537, 19-5-20-11268809
    # 19-5-10-11248624`.
    (
        re.compile(
            r'(?:現場來賓:(\w|\W)*|\s*好的,感謝您關注新聞看點(,別忘了轉發點[讚贊])?,再'
            + r'會。\s*|\s我們在本期節目結尾.*)?[#]?((?:大紀元《新聞看點》|新唐人(?:'
            + r'《熱點互動》|《新聞拍案驚奇》|《新聞大破解》|《世事關心》))製作組)*[#]?'
        ),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-27-11750457,
    # 19-12-30-11753878, 19-12-28-11751781, 19-12-25-11744047,
    # 19-12-23-11739348`.
    (
        re.compile(
            r'(觀眾朋友(大家)?|大家)好[,!](歡迎(?:(大家)?(訂閱)?關注新聞看點,?|'
            + r'收看(?:舊金山焦點|《新聞拍案驚奇》|這一期的(【熱點互動】)?)),|我們現在進'
            + r'入「新拍互動」環節。)?(我是\w*[。,](?:今天都好嗎\?\s)?|《新聞拍案驚奇》' + r'獲授權獨家首發:)?'
        ),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-27-11750457,
    # 19-12-28-11751523, 19-12-18-11730757, 19-10-16-11592527`
    (
        re.compile(
            r'(?:歡迎訂閱(【三國英雄】)?|請看視頻(?:~|《以史為鑒》。))?\s*新唐人、' + r'大紀元《三國英雄》聯合製作組'
        ),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-13-11719537,
    # 19-4-24-11210656`
    (
        re.compile(r'(?:您正在收看世事關心|最終結果如何,我們繼續拭目以待)。'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-30-11753878,
    # 19-12-19-11731456, 19-12-17-11728882`.
    (
        re.compile(r'\s?(好了?,)?今天就先?聊?到這裡了?,.*'),
        '',
    ),
    # This observation is made with `url_pattern = 20-1-1-11759086,
    # 19-4-23-11206720, 19-4-21-11201750`.
    (
        re.compile(r'[\W*\w*]*(⊙Opening|女士們[,、]先生們:\s*)'),
        '',
    ),
    # This observation is made with `url_pattern = 20-1-1-11759265
    # 19-12-20-11734996, 19-4-21-11201856, 19-4-5-11166312`.
    (
        re.compile(
            r'(?:[\S]*翻牆必看的文章|編(?:輯|者)按|[\S]*' + r'錄音如下|各位同修,各位同胞|以下是播出時間表):'
        ),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-30-11754591
    # 19-12-17-11727172`
    (
        re.compile(r'聲明人:(\s*\S+){,6}[\d\-:\s]+\S+\s*http\S+'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-23-11741126,
    # 19-12-5-11702000`.
    (
        re.compile(r'\s註[:\s\[\d\]]*(?:李洪志師父著作:《轉法輪》|這高度表示安全、' + r'牢不可破。)'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-21-11736511
    # 19-12-14-11722295`.
    (
        re.compile(r'(?:那?好|最後),歡迎您訂閱和分享我們的頻道.*'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-20-11735692
    # 19-12-13-11721610`.
    (
        re.compile(r'本文僅代表作者(個人)?觀點。$'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-19-11733577`.
    (
        re.compile(r'嘉賓:[\s\w]*,[\s\w]*主持人:.*$'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-19-11733207,
    # 19-12-20-11734006, 19-12-18-11730384, 19-12-18-11731126,
    # 19-10-16-11592972, 19-5-13-11255964, 19-5-11-11250223,
    # 20-1-1-11761463, 19-12-30-11756323, 19-12-27-11749380
    # 19-12-27-11748178`.
    (
        re.compile(
            r'(?:文章來源|大紀元新聞網|主辦單位|作者簡介|醫師小檔案|明慧學校夏'
            + r'令營時間|直播日期|有問題請聯繫|參考書目|【漣漪小語】|新唐人電視台官網' + r'|徵簽網址):.*'
        ),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-17-11727211`.
    (
        re.compile(r'\(\*\*\*插入片段\).*'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-15-11724589,
    # 19-12-14-11722684, 19-5-7-11240051, 19-5-11-11250223, 19-12-17-11727172
    # 19-12-20-11734996, 19-12-27-11748709, 19-8-14-11453112,
    # 19-12-1-11692633, 19-11-29-11688080, 19-11-13-11653910,
    # 19-11-13-11653876, 19-10-30-11623041, 19-10-28-11617434,
    # 19-10-17-11595022, 19-4-23-11206723`.
    (
        re.compile(
            r'\((?:澳洲墨爾本記者站採訪報導|本文歡迎轉載引用,註明出處即可|簽[名字]|'
            + r'化名|轉改自美國之音|(?:未|本[章卷])完,(全文)?待續|網站專文|(圖畫|圖片|視'
            + r'頻|、|圖片\S*)*|特別銘謝:.*|《.*敬請關注.*|敬請繼續關注.*|全文完|接[下' + r'上]文|前言)\)'
        ),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-20-11735692,
    # 19-12-15-11723411.`
    (
        re.compile(r'(接上文:)?【(十字路口|美國思想領袖)\s?】[\w\d]*\([上中]\),?'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-15-11723396`
    (
        re.compile(r'接上文:.*\([上中]\),?'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-15-11723411'`.
    (
        re.compile(r'以下視頻是採訪的第[二三]部分\(中文字幕\):(?:中共就是個黑幫組織|面對殘暴年輕人毫不退縮)。'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-14-11722898`.
    (
        re.compile(r',您去大紀元、新唐人網站,就可以看到活動的具體訊息。好的非常感謝各位的收看,我們下次節目再見。(\s?)'),
        r'\1',
    ),
    # This observation is made with `url_pattern = 19-11-4-11631494,
    # 19-5-3-11232059, 19-12-30-11754661`.
    (
        re.compile(r'(?:法輪大法世界各地免費煉功點|觀看|吳熾昌《客窗閒話》)$'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-20-11734499,
    # 19-10-23-11606025, 19-10-21-11602441`.
    (
        re.compile(r'(?:\s|時間:\S+\s?)(?:(研討會)地址|地點|電話):.*(?:電話|地址|郵箱):.*'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-19-11732179`.
    (
        re.compile(r'\(駐舊金山台北經濟文化辦事處\s?供稿.*'),
        '',
    ),
    # This observation is made with `url_pattern = 19-5-19-11266537`.
    (
        re.compile(r'相關視頻»\s*點擊下載[\s\dp,]*'),
        '',
    ),
    # This observation is made with `url_pattern = 19-4-23-11206723`.
    (
        re.compile(r'我叫[\w]*,是來自[\w]*的一名法輪功學員[,。]'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-24-11743216,
    # 19-12-30-11754199, 19-12-13-11721380, 19-12-8-11708626,
    # 19-12-16-11725356, 19-12-11-11714906, 19-11-15-11657230,
    # 19-6-1-11293517`.
    (
        re.compile(
            r'[-─—\*@\s\(]*點閱[《「【]?[^】」》]*[】」》]?(相關)?(?:(的亮點)?系'
            + r'列(文章)?|連載文章。|徵文)?[-─—\)]*'
        ),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-2-11694728,
    # 19-12-28-11751523, 19-12-31-11758244`.
    (
        re.compile(r'\[[\d]*\]'),
        '',
    ),
    # This observation is made with `url_pattern = 19-11-14-11655799`.
    (
        re.compile(r'\*.*作者.*\*'),
        '',
    ),
    # This observation is made with `url_pattern = 19-11-5-11636046`.
    (
        re.compile(r'\s[\w]{1,3}\s新唐人電視台.*$'),
        '',
    ),
    # This observation is made with `url_pattern = 19-11-5-11636046`.
    (
        re.compile(r'\(-【成語數來寶】待續-\)'),
        '',
    ),
    # This observation is made with `url_pattern = 19-10-16-11591305`.
    (
        re.compile(r'<本文摘自[^>]*>'),
        '',
    ),
    # This observation is made with `url_pattern = 19-10-7-11574545`.
    (
        re.compile(r'關注我們[\w]*主頁,[\w]*獲得更多資訊.*'),
        '',
    ),
    # This observation is made with `url_pattern = 13-8-3-3932270,
    # 13-7-29-3928497, 20-10-10-12466941`.
    (
        re.compile(r'\(?文字整理:[^)]*?(\)|$)'),
        '',
    ),
    # This observation is made with `url_pattern = 20-10-15-12478440`.
    (
        re.compile(r'#$'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-11-11715330`.
    (
        re.compile(r'\(\d\)$'),
        '',
    ),
    # This observation is made with `url_pattern = 19-10-16-11591235`.
    (
        re.compile(r'\**'),
        '',
    ),
    # This observation is made with `url_pattern = 19-10-25-11611601
    # 19-11-29-11688080`.
    (
        re.compile(r'[^的](?:來源|後記):\S+'),
        '',
    ),
    # This observation is made with `url_pattern = 19-10-25-11611601
    # 19-12-16-11725356`.
    (
        re.compile(r'參註:\s*\S*'),
        '',
    ),
    # This observation is made with `url_pattern = 19-12-18-11730384
    # 19-12-27-11748178, 19-12-27-11750092`.
    (
        re.compile(r'[^,^。\S]*請鎖定新聞直播間\S*'),
        '',
    ),
    # This observation is made with `url_pattern = 19-1-4-10954370`.
    (
        re.compile(r'\s‧\s'),
        '',
    ),
]
TITLE_SUB_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (
        re.compile(r'(【[^】]*?】|\([^)]*?\))'),
        '',
    ),
    (
        re.compile(r'(快[訊讯]|組[圖图]|焦[點点]人物):'),
        '',
    ),
    (
        re.compile(r'(—)+'),
        ' ',
    ),
]


def parser(raw_news: RawNews) -> ParsedNews:
    """Parse EPOCHTIMES news from raw HTML.

    Input news must contain `raw_xml` and `url` since these information cannot
    be retrieved from `raw_xml`.
    """
    # Information which cannot be parsed from `raw_xml`.
    parsed_news = ParsedNews(
        url_pattern=raw_news.url_pattern,
        company_id=raw_news.company_id,
    )

    try:
        soup = BeautifulSoup(raw_news.raw_xml, 'html.parser')
    except Exception:
        raise ValueError('Invalid html format.')

    ###########################################################################
    # Parsing news article.
    ###########################################################################
    article = ''
    try:
        # First remove tags we don't need.  This statement must always put
        # before tags retrieving statement.
        list(
            map(
                lambda tag: tag.decompose(),
                soup.select(ARTICLE_DECOMPOSE_LIST),
            )
        )
        # Next we retrieve tags contains article text.  This statement must
        # always put after tags removing statement.
        article = ' '.join(
            map(
                lambda tag: tag.text,
                soup.select(ARTICLE_SELECTOR_LIST),
            )
        )
        article = news.parse.util.normalize.NFKC(article)
    except Exception:
        raise ValueError('Fail to parse EPOCHTIMES news article.')

    ###########################################################################
    # Parsing news category.
    ###########################################################################
    category = ''
    try:
        # Sometimes news does not have categories, but if they do, categories
        # are always located in breadcrumbs `a.breadcrumbs`.  The first text
        # in breadcrumbs is media type, we also exclude it (`a.breadcrumbs`
        # does not select `首頁`).  There might be more than one category.  Thus
        # we include them all and save as comma separated format.  Some
        # categories are duplicated, thus we remove it using
        # `list(dict.fromkeys(...))`.
        category = ','.join(
            list(
                dict.fromkeys(
                    map(
                        lambda tag: tag.text,
                        soup.select('a.breadcrumbs')[1:],
                    )
                )
            )
        )
        category = news.parse.util.normalize.NFKC(category)
    except Exception:
        # There may not have category.
        category = ''

    ###########################################################################
    # Parsing news datetime.
    ###########################################################################
    timestamp = 0
    try:
        # Some news publishing date time are different to URL pattern.  For
        # simplicity we only use URL pattern to represent the same news.  News
        # datetime will convert to POSIX time (which is under UTC time zone).
        year, month, day, _ = parsed_news.url_pattern.split('-')
        year = f'20{year}'
        if len(month) == 1:
            month = f'0{month}'
        if len(day) == 1:
            day = f'0{day}'
        timestamp = int(
            datetime.strptime(f'{year}{month}{day}', '%Y%m%d').timestamp()
        )
    except Exception:
        raise ValueError('Fail to parse EPOCHTIMES news datetime.')

    ###########################################################################
    # Parsing news reporter.
    ###########################################################################
    reporter_list = []
    reporter = ''
    try:
        for reporter_pttn in REPORTER_PATTERNS:
            # There might have more than one pattern matched.
            reporter_list.extend(reporter_pttn.findall(article))
            # Remove reporter text from article.
            article = news.parse.util.normalize.NFKC(
                reporter_pttn.sub('', article)
            )
        # Reporters are comma seperated.
        reporter = ','.join(map(news.parse.util.normalize.NFKC, reporter_list))
        # Some reporters are separated by whitespaces, '/' or '、'.
        reporter = news.parse.util.normalize.NFKC(
            re.sub(
                r'[\s、/]+',
                ',',
                reporter,
            )
        )
    except Exception:
        # There may not have reporter.
        reporter = ''

    ###########################################################################
    # Parsing news title.
    ###########################################################################
    title = ''
    try:
        title = soup.select_one(TITLE_SELECTOR_LIST).text
        title = news.parse.util.normalize.NFKC(title)
    except Exception:
        raise ValueError('Fail to parse EPOCHTIMES news title.')

    ###########################################################################
    # Substitude some article pattern.
    ###########################################################################
    try:
        for article_pttn, article_sub_str in ARTICLE_SUB_PATTERNS:
            article = news.parse.util.normalize.NFKC(
                article_pttn.sub(
                    article_sub_str,
                    article,
                )
            )
    except Exception:
        raise ValueError('Fail to substitude EPOCHTIMES article pattern.')

    ###########################################################################
    # Substitude some title pattern.
    ###########################################################################
    try:
        for title_pttn, title_sub_str in TITLE_SUB_PATTERNS:
            title = news.parse.util.normalize.NFKC(
                title_pttn.sub(
                    title_sub_str,
                    title,
                )
            )
    except Exception:
        raise ValueError('Fail to substitude EPOCHTIMES title pattern.')

    parsed_news.article = article
    if category:
        parsed_news.category = category
    else:
        parsed_news.category = ParsedNews.category
    if reporter:
        parsed_news.reporter = reporter
    else:
        parsed_news.reporter = ParsedNews.reporter
    parsed_news.timestamp = timestamp
    parsed_news.title = title
    return parsed_news
