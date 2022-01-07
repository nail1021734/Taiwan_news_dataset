import re
from datetime import datetime
from typing import List, Tuple

from bs4 import BeautifulSoup

import news.parse.util.normalize
from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

# We remove the following content:
#
# - Figures and captions:
#   Located in `b`, `img`, `iframe` and `strong` tags.
#   Sometimes captions are inside the same `p` tag which satisfying
#   `p:has(img, iframe)`, thus we use
#   `p:has(:is(img, iframe) ~ strong, strong ~ :is(img, iframe)) strong` to
#   select these captions.  Most of the time captions are inside
#   `p:has(strong)` which follow **immediately** after `p:has(img)` or
#   `p:has(iframe)`, and captions does not have color highlights.  With this
#   observation, we apply the following rule to select `strong` tags:
#
#   1. Use `:not(:has(span[style*="color"]))` to avoid select color highlighted
#      tags.  News company must use editor to write down drafts, and those
#      editor use `span` to perform color highlighting.
#
#   2. Avoid any nested combination of `span` and `strong` tags, including
#      `span strong` or `strong span`.  In this way strong tag would not be
#      color highlighted.
#
#   3. News article always consist of `p` tags, thus we drop `p` tags which
#      containing `strong` tags, namely `p:has(strong)`.
#
#   4. Use `p:has(img, iframe):not(:has(strong)) +` at the begining.  `+`
#      ensure immediately precedence of `p:has(img, iframe)`.
#      `:not(:has(strong))` is used to avoid already paired images and
#      captions, which were already addressed by
#      `p:has(:is(img, iframe) ~ strong, strong ~ :is(img, iframe))`).
#
#   5. Use `p:not(:has(img, iframe))` to make sure dropping candidates does not
#      have `img` or `iframe` tags.  This is need to avoid confliction with
#      `p:has(:is(img, iframe) ~ strong, strong ~ :is(img, iframe)) strong`.
#
#   6. Even with this level of specifity, we still find bugs, but those bugs
#      are beyond repaired since the formatting of ETtoday suck ass.
#      This observation is made with `url_pattern = 1200297`.
#
#   This observation is made with `url_pattern = 2112150, 1200023, 1200034,
#   1200071, 1200075, 1200173, 1200265`.
#
# - Copy rights or fortune telling:
#   Paragraphs using center style are probably copy rights or fortune telling.
#   This observation is made with `url_pattern = 1200311, 1200480`.
#
# - Extra informations:
#   Paragraphs contains one `strong` tags and at least 3 `a` tags are
#   probably extra information, thus we use
#   `p:not([class]):has(strong):has(a ~ a ~ a)` to capture these paragraphs.
#   This observation is made with `url_pattern = 1200034`.
#
# - Videos:
#   Located in `div.fb-video`
#   This observation is made with `url_pattern = 1200000`.
#
# - Ads:
#   Located in `div` tags and contains 'ad' in their classname.
#   This observation is made with `url_pattern = 2112150`.
#
# - App download recommendation:
#   Located in `p` tags precede by a `hr` tag.
#   This observation is made with `url_pattern = 1200011`.
#
# - Social media links:
#   Located in `div` tags and contains 'social' in their classname.
#   Also exclude social media post (including instagram, twitter, facebook)
#   in `blockquote` tags.
#   This observation is made with `url_pattern = 2112150, 1200040, 1200102,
#   1200138`.
#
# - Related news:
#   Located in `p.note` and `p a` tags.  The following rules applied:
#
#   1. Related news are mainly in the format
#      `p:has(a[href*="ettoday" i]) a`, the `i` in the selector stands for
#      case-insensitive.  They usually appear at the end of news articles, but
#      sometimes in the middle of paragraph.  Thus we only remove the
#      occurrence of `a` tags.
#
#   2. For news under movie category, related news may come from different
#      sites.  These include `p:has(a[href*="dramaqueen"]) a`.
#
#   3. For news on facebook, we use `p:has(a[href*="facebook.com/ettoday" i])`
#      to capture.  Since they ALWAYS appear at the end of news article, we
#      drop these `p` tags along with all the `p` tags follow by using
#      `p:has(a[href*="facebook.com/ettoday" i]) ~ p`.
#
#   4. For news under finance category, we use
#      `p:has(a[href*="businessweekly"])` to capture.  Since they ALWAYS appear
#      at the end of news article, we drop these `p` tags along with all the
#      `p` tags follow by using `p:has(a[href*="businessweekly"]) ~ p`.
#
#   5. For news under traveling category, related news may include address
#      wrapped inside google map, thus we use
#      `p:has(a[href*="google.com/maps"])`.
#
#   6. 有些新聞包含廣告,使用 `p:has(a[href*="bit.ly"]) a` 過濾掉廣告的網址.
#
#   7. 過濾掉宇宙人外信的廣告 `p:has(a[href*="vip"]) a,`.
#
#   8. 過濾掉房產廣告 `p:has(a[href*="lihi.cc"]) a`,不只比對 "cc" 是因為 "cc"
#   有包含 PTT 的內容過濾掉 PTT 網址會影響新聞內容.
#
#   9. 夏日宅家自制氣泡飲廣告 `p:has(a[href*="u-mall"]) a`.
#
#   10. 其他新聞的網址 `p:has(a[href*="kkbox"]) a`.
#
#   11. 濾掉部落格網址 `p:has(a[href*="blog"]) a`.
#
#   This observation is made with `url_pattern = 2112150, 1200022, 1200077,
#   1200097, 1200118, 1200132, 1200158, 1200478, 1200491, 1200547, 1200562,
#   10715, 2000176, 2000195, 2004431, 2015327, 8902, 2096795`.
ARTICLE_DECOMPOSE_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    b,
    img,
    iframe,
    p:has(:is(img, iframe) + strong, strong + :is(img, iframe)) strong,
    p:has(img, iframe):not(:has(strong)) + p:not(
        :has(img, iframe)
    ):not(
        :has(span[style*="color"]:has(strong))
    ):not(
        :has(strong:has(span[style*="color"]))
    ):has(strong),

    p[style*="text-align: center"],

    p:not([class]):has(strong):has(a ~ a ~ a),

    div.fb-video,

    div.ad_readmore,
    div.ad_in_news,
    div[class*='et_ad_group'],
    div[class*='ad_txt'],
    div[class^='ad'],

    div.story > table,
    div.story div.comment,

    hr ~ p,

    div[class*='et_social'],
    blockquote,

    p.note,
    p:has(a[href*="ettoday" i]) a,
    p:has(a[href*="dramaqueen"]) a,
    p:has(a[href*="facebook.com/ettoday" i]),
    p:has(a[href*="facebook.com/ettoday" i]) ~ p,
    p:has(a[href*="businessweekly"]),
    p:has(a[href*="businessweekly"]) ~ p,
    p:has(a[href*="google.com/maps"]),
    p:has(a[href*="bit.ly"]) a,
    p:has(a[href*="vip"]) a,
    p:has(a[href*="lihi.cc"]) a,
    p:has(a[href*="mall"]) a,
    p:has(a[href*="kkbox"]) a,
    p:has(a[href*="blog"]) a
    ''',
)

# News articles are located in `div.story > p(:not([class]))`.
# ETtoday has inconsistent format.  For example, news article might located in
# `div.story > link > p:not([class])` which is caused by forgetting closeing
# `link` tags with `</link>`.  These cases should be consider as bug, and
# we should simply include it.  For example, we include
# `div.story > link > p(:not([class]))`.  Note that always use `>` operator
# since `p` tags might include another `p` tags.
# This observation is made with `url_pattern = 2112150`.
ARTICLE_SELECTOR_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    div.story > p:not([class]),
    div.story > link > p:not([class])
    ''',
)

# News title is located in `h1.title`.
# This observation is made with `url_pattern = 2112150`.
TITLE_SELECTOR_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    h1.title,
    h1.title_article,
    div.subject_article > header > h1
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
    # This observation is made with `url_pattern = 2100177, 2100299, 2104515,
    # 2104622`.
    re.compile(
        r'^●\s(.*?)/.*?\s',
    ),
    # This observation is made with `url_pattern = 2026235, 2031830`.
    re.compile(r'^文(?:/?.*?教育學苑)?\.(.*?)\s'),
    # This observation is made with `url_pattern = 1200000, 1200001, 1200002,
    # 1200012, 1200021, 1200025, 1200057, 1200071, 1200085, 1200115, 1200125,
    # 1200134, 1200161, 1200181, 1200286, 1200474, 1200501, 2112150, 1200554,
    # 1200581, 1200621, 261, 7626, 520, 379, 1021, 9616, 2104727, 2104772`.
    re.compile(
        r'(?:(?:東森新聞)?(?:新竹)?(?:實習|振道)?(?:記者|編輯(?!部))|(?:網搜|寵物)小組|'
        + r'(?:影視|影劇|體育|運動|國際|社[群會]|大陸(?:新聞)?|娛樂|地方|生活|要聞|財經|政治|旅遊|新聞節目|消費)中心)'
        + r'([\w、\s]*?)/.*?(?:綜合)?(?:報導|編譯)(?:、攝影)?',
    ),
    # Reporter name with leading English characters.  Only English characters
    # can have whitespace in between, other characters cannot.
    # This observation is made with `url_pattern = 1200594, 2100192`.
    re.compile(
        r'(?:(?:圖、?|撰)?文(?:、?圖)?|彙整整理|編輯)/(?!中央社)'
        + r'([a-zA-Z\d]+(?:(?:\s[a-zA-Z\d]+)+[^(\s]*)?)'
        + r'(?:(?:提供|摘自|圖片|\s*\S*觀點)\S*)?(?:\([^)]*\))?\s+'
    ),
    # Reporter name with no whitespace.
    # This observation is made with `url_pattern = 1200028, 1200034, 1200168,
    # 1200197, 1200260, 1200280, 1200297, 1200436, 1200592, 2100006`.
    re.compile(
        r'(?:(?:圖、?|撰)?文(?:、?圖)?|彙整整理|編輯)/(?:(?:藥|護理)師)?(?!中央社)'
        + r'(?:記者|特約撰述\s*)?([\w、]*?)(?:(?:提供|摘自|圖片|\s*\S*觀點)\S*)?'
        + r'(?:\([^)]*\))?\s+'
    ),
]
ARTICLE_SUB_PATTERNS: List[Tuple[re.Pattern, str]] = [
    # Remove captions.  This is still needed even if we have
    # `ARTICLE_DECOMPOSE_LIST` since some captions were located before images.
    # Usually captions will have source reference surrounded by parenthese at
    # the end, for example, `(圖/...)`.  But since ETtoday's format is so fucked
    # up, there will always have exceptions.  Thus for those case we simply
    # match as much text as possible.  Note that parentheses inside parenthese
    # are allowed.
    # This observation is made with `url_pattern = 1200012, 1200028, 1200192,
    # 1200193, 1200278, 2112150, 520`.
    (
        re.compile(
            r'[▲▼►]+(.*?\([組合圖影片相照資料來源翻攝採訪撰稿剪輯轉][^)]*\)([^()]+\))?|\s*\S+)'
            + r'((?<=[a-zA-Z])[a-zA-Z\d\s]+)?\s*',
        ),
        ' ',
    ),
    # Remove reference hint at the end.
    # This observation is made with `url_pattern = 8565, 9616, 5043, 5452,
    # 10034`.
    (
        re.compile(r'([◎※]+|(張老師|(自殺防治諮詢)?安心)專線|請快來「ETtoday)\S*$'),
        ' ',
    ),
    # Remove list symbols.
    # This observation is made with `url_pattern = 1200034, 1200318, 1200403,
    # 1200591, 1200623, 2104523, 2000123, 2026310, 2085868`.
    (
        re.compile(
            r'\s(?:[◉◆►■●★▇※◎]|TOP\s?\d+/?)+(\S*)',
            re.IGNORECASE,
        ),
        r' \1',
    ),
    # Remove additional information in the middle of paragraphs which are
    # surrounded by parenthese.
    # This observation is made with `url_pattern = 1200039, 1200077, 1200090,
    # 1200098, 1200146, 1200243, 1200190, 1200260, 1200493, 1200601, 2112150,
    # 8902`.
    (
        re.compile(
            r'\((參考|(示意)?圖|畫面顯示|左|右|ETtoday寵物雲|補充官方回應|(註|編按|新聞來源):|本文轉載?自'
            + r'|(科技|[新南]華|人民|經濟參考|中新)([早日]?報|網)|日本足球觀察家)[^)]*?\)'
        ),
        '',
    ),
    # Remove recommendations with whitspace at both begin and end.  Use
    # `(?=...)` to avoid consume whitespace at the end since multiple occurence
    # may be side by side.
    # This observation is made with `url_pattern = 1200181, 1200426`.
    (
        re.compile(r'\s(精選書摘|《(ETtoday(筋斗|新聞)雲|播吧)》)(?=\s)'),
        ' ',
    ),
    # Remove paragraphs contains additional informations.
    # This observation is made with `url_pattern = 1200022, 1200132, 1200152,
    # 1200161, 1200168, 1200193, 1200234, 1200237, 1200267, 1200392, 1200403,
    # 1200426, 1200436, 1200526, 1200577, 1200579, 7427`.
    (
        re.compile(
            r'(^|[\s.])(《?(ETtoday新聞雲|ET FASHION)》?提醒您?|\*[圖片、資料]+來源|到這裡找'
            + r'|這裡悶、那裏痛,親友說吃這個藥卡有效|(作者|摘自|Photo|BLOG|粉絲頁|FB|附註)\s*:\s*|鎖定每日刊文'
            + r'|《?ETtoday寵物雲》?期許每個人都能更重視生命|(自殺防治諮詢安心|生命線協談)專線|歡迎加入\S+:'
            + r'|\(?(圖|攝?影|撰文)/|\*+以下有|影片恐會引起部分讀者不適,請自行斟酌觀看|影音連結)\S+',
            re.IGNORECASE,
        ),
        ' ',
    ),
    # Remove suggestion.
    # This observation is made with `url_pattern = 1200058`.
    (
        re.compile(r'《[^》]*》\S+(報名|快訊)\s.*$'),
        ' ',
    ),
    # Remove legal notes.
    # This observation is made with `url_pattern = 1200010, 1200161`.
    (
        re.compile(r'\s((飲酒過量|有礙健康|喝酒不開車|開車不喝酒).?)+'),
        ' ',
    ),
    # Remove editor notes.
    # This observation is made with `url_pattern = 1200039`.
    (
        re.compile(r'(出稿|更新):[\d.:\s]+'),
        '',
    ),
    # Remove copy right notes.
    # This observation is made with `url_pattern = 1200071, 1200090`.
    (
        re.compile(r'\s+(版權聲明:|圖片為版權照片|\*?本文由).*?不得.*?轉載\S*'),
        '',
    ),
    # Remove editor notes with slash `/` at the start of news article.
    # This observation is made with `url_pattern = 2104609`.
    (
        re.compile(r'^(\s?([圖文]|Text|Photo)/.*?美麗佳人)+', re.IGNORECASE),
        ' ',
    ),
    # Remove editor notes with slash `/` at the end of news article.
    # This observation is made with `url_pattern = 1200090, 1200492`.
    (
        re.compile(r'\s([圖文]|Text|Photo)/.*$', re.IGNORECASE),
        ' ',
    ),
    # Remove recommendations and additional informations at the end of news
    # article.  Note that `本文作者:` should be the reporter, but since the
    # format is so fucked up, we say "Fuck it. just remove it".
    # This observation is made with `url_pattern = 1200009,  1200077, 1200081,
    # 1200090, 1200105, 1200165, 1200181, 1200190, 1200193, 1200243, 1200260,
    # 1200265, 1200278, 1200311, 1200318, 1200321, 1200362, 1200413, 1200436,
    # 1200442, 1200452, 1200470, 1200474, 1200510, 1200511, 1200521, 1200526,
    # 1200534, 1200547, 1200558, 1200563, 1200578, 1200579, 1200591, 1200594,
    # 5210, 3728, 1021, 3186, 2100002, 2100046, 2100081, 2100233, 2104412,
    # 2104432, 2104523, 2104536, 2104598, 2104606, 2104659, 2000174, 2000197,
    # 2000210, 2004394, 2004402, 2015254, 2015284, 2015388, 2015435, 2026226,
    # 2026235, 2026241, 2026279, 2026280, 2026349, 2031723, 2031751, 2031760, 2031765,
    # 2031809, 2031830, 2031832, 2053512, 2053560, 2053582, 2053589, 2053611,
    # 2085854, 2085868, 2085889, 2085895, 2096796, 2096842, 2096887, 2096935`.
    (
        re.compile(
            r'(想?看?[【,]*?更多(圖片|時尚藝術資訊|賽事|(精[彩采]|\S*在台上架相關)(影音|內容|報導)'
            + r'|活動訊息|健康訊息|\S+?新消息,|詳細帶逛)(精[闢彩采])?(分析)?(都在|請([洽見]|鎖定))?'
            + r'|\s?(Google\sPlay預約頁|備註|出處|詳情請見\S*官網|資料來源|相關(影音|內容|報導)'
            + r'|♡\S*|線上展請至|商品介紹|活動詳情|聯繫窗口|服務諮詢專線|\S*(售票|店家)資訊'
            + r'|活動(時間|辦法)|作者介紹|開放時間|門票):'
            + r'|\(?本文(由|原刊|(轉載|摘)自|經(授權)?|作者:)|\S*以上言論不代表本網立場|\S+—基本資料'
            + r'|【(貼心提醒|延伸閱讀|更多新聞)】|本集.ETtoday看電影.|\S+>{3,}|\S+★|\[info\]'
            + r'|這場我有另外個選項,有興趣讀者|\S+詳細活動內容|\*關於\S+\s*詳細介紹|如遇緊急狀況\S+?聯絡資料如下'
            + r'|\(?(完整|系列)(文章|報導)[請可]|相關資訊可至|延伸閱讀|熱門點閱》|原文出處|【?你可能也?想看】?'
            + r'|\*《ETtoday新聞雲》|\s?好文推薦\s?| 關於《(雲端最前線 | 慧眼看天下)》|\S*?投票網址'
            + r'|\s*其他人也看了:?(這些新聞)?|「Webike台灣」編輯部\S*?撰稿報導|本文依據\S*?處理'
            + r'|[\s【]?(閱讀)?(更多|相關)+((熱門)?新聞|鏡週刊)(閱讀|頁面|報導)?|\(編輯:.*?\)\d+'
            + r'|\*部落客.*?現有經營|[^。\s]*?可點此連結|感謝您在.*?社團的投稿.*?|更多\S*?日常'
            + r'|毛爸毛媽的神隊友!|連任8屆憑實力無誤|此文\S*?投稿。?|[^。\s]*?完整內容請見'
            + r'|「PS178 玩運彩一起發」每周一至五|數位時代的潮流下,所有的東西都開始結合數位科技'
            + r'|[^。\s]*?歡迎雲友更多參與|「MAZDA挺你,醫起守護」活動辦法|同時也歡迎到\S*?社團投稿'
            + r'|【車主有話說】|想(學習|知道)更多(股市|外匯)(操作技巧|資訊)|加入\S*?粉絲團'
            + r'|橘子狗愛吃糖部落格|想要收看最新的\S*?節目|[^。\s]*?懶人包連結|搶孅體驗組'
            + r'|本文.*?為.*?所有並授權提供|精彩全文,詳見|#我在案發現場|飛天璇\s我用輕鬆的筆調'
            + r'|以上言論為個人立場|[^。\s]*?就快上ETtoday新聞雲).*?$',
        ),
        ' ',
    ),
    # Remove instagram account.
    # This observation is made with `url_pattern = 1200146`.
    (
        re.compile(r'instagram:\s*@[a-z0-9_]+', re.IGNORECASE),
        '',
    ),
    # Remove reference to ETtoday old news.
    # This observation is made with `url_pattern = 1200022`.
    (
        re.compile(r'如同\(\),'),
        '',
    ),
    # Remove promote information follow by a colon `:`.  This kind of
    # information usually appear at the end, with structure like the follow:
    #
    # promotion-title
    # 地址:...
    # 電話:...
    #
    # Note that `promotion-title` is not longer than 50 words and will be
    # deleted.  Thus address information in the middle of paragraphs will not
    # be deleted (like `url_pattern = 1200387`).
    # This observation is made with `url_pattern = 1200161, 1200193, 1200254,
    # 1200335, 1200387, 1200411, 1200594`.
    (
        re.compile(
            r'\s\S{1,50}(\s*(地址|電話|信箱|票價|門票|基地(規模|位置)'
            + r'|(建築|結構)設計|(活動|報名|舉辦|營業|開放)(日期|時間|辦法)'
            + r'|(戶數|樓層|產品)規劃|投資建設):\s*([a-zA-Z\d\s,\-:]+)?([^a-zA-Z\s]+)?)+',
        ),
        ' ',
    ),
    # Remove content hints.
    # This observation is made with `url_pattern = 1200190`.
    (
        re.compile(r'【第一次[^】]*上手】'),
        '',
    ),
    # Remove searching url notes.
    # This observation is made with `url_pattern = 1200234`.
    (
        re.compile(
            r'(網站)?查詢:'
            + r'''((https?://)?[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;%=]+\s*)+'''
        ),
        '',
    ),
    # Remove inviting url inside parenthese.
    # This observation is made with `url_pattern = 1200584`.
    (
        re.compile(
            r'\(\s*'
            + r'''(https?://[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;%=]+\s*)+'''
            + r'\s*\)'
        ),
        '',
    ),
    # Remove content hints.
    # This observation is made with `url_pattern = 1200285, 1200321`.
    (
        re.compile(r'(^|\s)【[^】]*】(→\S+)?(\s|$)'),
        ' ',
    ),
    # 移除其他公司的記者.
    # This observation is made with `url_pattern = 2100006, 2100007, 2100192,
    # 2031852, 2053474, 2096928`.
    (
        re.compile(
            r'((圖、?|撰)?文(、?圖)?|彙整整理|編輯|活動小組)/'
            + r'(.*?報導|三國殺名將傳-.*?\s|中央社.*專?電|中央社)'
        ),
        '',
    ),
    # 移除常見但是在文章最後突然出現的詞.
    # This observation is made with `url_pattern = 2100012, 2000210, 2096795`.
    (
        re.compile(r'\s*(農遊券|、|規小孫、FB|主要規格)$'),
        '',
    ),
    # 將重複句點換成一個.
    # This observation is made with `url_pattern = 2100012, 2000210, 2026349`.
    (
        re.compile(r'。[\s*?。]+$'),
        '。',
    ),
    # 移除文章開頭的贅詞.
    # This observation is made with `url_pattern = 2100081, 2026310, 2086009,
    # 2086055`.
    (
        re.compile(
            r'([圖文]+/.*(摩托新聞)\s+|取材(.*?)/Mazda標達汽車(.*?)廠'
            + r'|中央社.*?(\d+日)?(綜合)?[外專]?電?報導|中央社\s)'
        ),
        '',
    ),
    # 移除文章中莫名出現的的 backspace.
    # This observation is made with `url_pattern = 2026279`.
    (re.compile(r'\u0008'), ''),
    # Remove failed parsing paragraph at the begining. This kind of paragraphs
    # are consist of what ever we left after parsing from all patterns above.
    # Thus this pattern must always put at the end of all patterns.
    # This observation is made with `url_pattern = 1200594, 1200601, 2004373`.
    (
        re.compile(r'^(Emmy\s|是小眼睛\s|,)'),
        ' ',
    ),
    # Remove stand along character at the begining.  This kind of paragraphs
    # are consist of what ever we left after parsing from all patterns above.
    # Thus this pattern must always put at the end of all patterns.
    # This observation is made with `url_pattern = 1200594`.
    (
        re.compile(r'^([\da-zA-Z\u4e00-\u9fff](?=\s))+'),
        ' ',
    ),
    # Remove stand along character at the end.  This kind of paragraphs are
    # consist of what ever we left after parsing from all patterns above.  Thus
    # this pattern must always put at the end of all patterns.
    # This observation is made with `url_pattern = 1200601`.
    (
        re.compile(r'((?<=\s)[\da-zA-Z\u4e00-\u9fff])+$'),
        ' ',
    ),
]

TITLE_SUB_PATTERNS: List[Tuple[re.Pattern, str]] = [
    # This observation is made with `url_pattern = 1200001, 1200029`.
    (
        re.compile(r'精彩回顧看這邊?!?'),
        '',
    ),
    # Remove content hints followed by a slash `/`.  Note that if word before
    # slash is too long, then it is probably not a content hint.
    # This observation is made with `url_pattern = 1200017, 1200019, 1200501`.
    (
        re.compile(r'^[^/]{1,11}/'),
        '',
    ),
    # Remove useless symbol.
    # This observation is made with `url_pattern = 1200021`.
    (
        re.compile(r'[❤]'),
        '',
    ),
    # Remove content hints.
    # This observation is made with `url_pattern = 1200285`.
    (
        re.compile(r'(【[^】]*】|\([^)]*\))'),
        '',
    ),
]

BR_PATTERN: re.Pattern = re.compile(r'(\s*<br\s*/>)+\s*')
FIX_PATTERN: re.Pattern = re.compile(
    r'(<strong[^>]*>[^<]*)(<img[^>]*>)([^<]*)',
)


def fix_raw_xml(raw_xml: str) -> str:
    r"""Fix raw XML.

    ETtoday's news sometimes has following structure:

    <strong>
        ...
        <img .../>
        ...
    </strong>

    This make CSS selector hard to select strong tags.  Thus we fix it with
    the following structure:

    <strong>
        ...
    </strong>
        <img .../>
    <strong>
        ...
    </strong>

    Note that paragraphs may contain lots of `<br />` tags, thus we replace
    them with whitespace to make fixing much easier.
    """
    # Remove `<br/>` tags and replace with single whitespace.
    raw_xml = BR_PATTERN.sub(' ', raw_xml)

    # Extract `<strong><img/></strong>`.
    while True:
        match = FIX_PATTERN.search(raw_xml)

        if not match:
            break

        raw_xml = (
            raw_xml[:match.start()] + match.group(1) + '</strong>'
            + match.group(2) + '<strong>' + match.group(3)
            + raw_xml[match.end():]
        )

    return raw_xml


def parser(raw_news: RawNews) -> ParsedNews:
    """Parse ETtoday news from raw HTML.

    Input news must contain `raw_xml` and `url` since these information cannot
    be retrieved from `raw_xml`.
    """
    # Information which cannot be parsed from `raw_xml`.
    parsed_news = ParsedNews(
        url_pattern=raw_news.url_pattern,
        company_id=raw_news.company_id,
    )

    try:
        soup = BeautifulSoup(fix_raw_xml(raw_news.raw_xml), 'html.parser')
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
        raise ValueError('Fail to parse ETtoday news article.')

    ###########################################################################
    # Parsing news category.
    ###########################################################################
    category = ''
    try:
        # Sometimes news does not have categories, but if they do, categories
        # are always located in either `div.menu_bread_crumb` or
        # `div.part_breadcrumb`.  The text of category is then located in the
        # last tag of `div > a > span`.
        category = news.parse.util.normalize.NFKC(
            soup.select(
                'div:is(.menu_bread_crumb, .part_breadcrumb) > div > a > span'
            )[-1].text
        )
        # Some category start with `ETtoday` and end with `雲`.
        # This observation is made with `url_pattern = 1200034, 1200090,
        # 12000105, 1200318`.
        category = re.sub(r'(?:ET)?(?:today)?([^雲]*)雲?$', r'\1', category)
    except Exception:
        # There may not have category.
        category = ''

    ###########################################################################
    # Parsing news datetime.
    ###########################################################################
    timestamp = 0
    try:
        # News publishing date and time is always in the `content` attribute
        # of `meta[name="pubdate"]` tag,  with ISO 8601 format.  We then
        # convert datetime to POSIX time (which is under UTC time zone).
        timestamp = datetime.strptime(
            soup.select_one('meta[name="pubdate"]')['content'],
            '%Y-%m-%dT%H:%M:%S%z',
        ).timestamp()
    except Exception:
        raise ValueError('Fail to parse ETtoday news datetime.')

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
        # Some reporters are separated by whitespaces or '、'.  We replace
        # whitespace precede (or follow) an english character.  This is needed
        # since some reporters have English names.
        # This observation is made with `url_pattern = 1200037`.
        reporter = news.parse.util.normalize.NFKC(
            re.sub(r'[、]+', ',', reporter),
        )
        reporter = news.parse.util.normalize.NFKC(
            re.sub(r'([a-zA-Z\d])\s+(?=\w)', r'\1-', reporter),
        )
        reporter = news.parse.util.normalize.NFKC(
            re.sub(r'(?<=\w)\s+([a-zA-Z\d])', r'-\1', reporter),
        )
        reporter = news.parse.util.normalize.NFKC(
            re.sub(r'\s+', ',', reporter),
        )
        # Remove trailing comma.
        # This observation is made with `url_pattern = 1200260`.
        reporter = re.sub(',$', '', reporter)
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
        raise ValueError('Fail to parse ETtoday news title.')

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
        raise ValueError('Fail to substitude ETtoday article pattern.')

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
        raise ValueError('Fail to substitude ETtoday title pattern.')

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
