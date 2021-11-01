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
#   Sometimes captions are inside the same `p:has(img, iframe)`, thus we use
#   `p:has(:is(img, iframe) ~ strong, strong ~ :is(img, iframe))` to select
#   these captions.  Most of the time captions follow **immediately** after
#   `img` or `iframe`, and captions does not have color highlights.  With this
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
#   5. Even with this level of specifity, we still find bugs, but those bugs
#      are beyond repaired since the formatting of ETtoday suck ass.
#      This observation is made with `url_pattern = 1200297`.
#
#   This observation is made with `url_pattern = 2112150, 1200023, 1200034,
#   1200071, 1200075, 1200173, 1200265`.
#
# - Copy right notes:
#   Paragraphs using center style are probably copy rights.
#   This observation is made with `url_pattern = 1200311`.
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
#   Located in `p.note`, `iframe` and `p a[href*="ettoday"]` tags.
#   This observation is made with `url_pattern = 2112150, 1200022, 1200077,
#   1200097, 1200118, 1200132, 1200158`.
ARTICLE_DECOMPOSE_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    b,
    img,
    iframe,
    p:has(:is(img, iframe) ~ strong, strong ~ :is(img, iframe)),
    p:has(img, iframe):not(:has(strong))
    + p:not(:has(span[style*="color"]:has(strong))):not(:has(
        strong:has(span[style*="color"])
    )):has(strong),

    p[style*="text-align: center"],

    p:not([class]):has(strong):has(a ~ a ~ a),

    div.fb-video,

    div.ad_readmore,
    div.ad_in_news,
    div[class*='et_ad_group'],
    div[class*='ad_txt'],
    div[class^='ad'],

    hr ~ p,

    div[class*='et_social'],
    blockquote,

    p.note,
    p:has(a[href*="ettoday"]) a
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
# This observation is made with `url_pattern = `.
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
    # This observation is made with `url_pattern = 1200000, 1200001, 1200002,
    # 1200012, 1200021, 1200025, 1200057, 1200071, 1200085, 1200115, 1200125,
    # 1200134, 1200161, 1200181, 1200286, 2112150`.
    re.compile(
        r'(?:(?:實習)?記者|(?:網搜|寵物)小組|(?:體育|國際|社會|大陸|娛樂|地方|生活|財經|政治|旅遊|新聞節目)中心)'
        + r'([\w、\s]*?)/.*?(?:綜合)?(?:報導|編譯)',
    ),
    # This observation is made with `url_pattern = 1200028, 1200034, 1200168,
    # 1200197, 1200260, 1200280, 1200297`.
    re.compile(
        r'(?:(?:圖、|撰)?文|彙整整理|編輯)/(?:(?:藥|護理)師)?(?:特約撰述\s*)?([\w、]*?)'
        + r'(?:(?:提供|摘自|圖片)\S*)?(?:\([^)]*\))?\s+'
    ),
]
ARTICLE_SUB_PATTERNS: List[Tuple[re.Pattern, str]] = [
    # Remove captions.  This is still needed even if we have
    # `ARTICLE_DECOMPOSE_LIST` since some captions were located before images.
    # Usually captions will have source reference surrounded by parenthese at
    # the end, for example, `(圖/...)`.  But since ETtoday's format is so fucked
    # up, there will always have exceptions.  Thus for those case we simply
    # match as much text as possible.
    # This observation is made with `url_pattern = 1200012, 1200028, 1200278,
    # 2112150`.
    (
        re.compile(r'[▲▼►]+(.*?(\([圖影片相照資料來源翻攝][^)]*\))|\s*\S+)\s*'),
        ' ',
    ),
    # Remove list symbols.
    # This observation is made with `url_pattern = 1200034, 1200318, 1200403`.
    (
        re.compile(r'\s[●★▇]+(\S*)'),
        r' \1',
    ),
    # Remove additional information in the middle of paragraphs which are
    # surrounded by parenthese.
    # This observation is made with `url_pattern = 1200039, 1200077, 1200090,
    # 1200098, 1200146, 1200243, 1200190, 1200260, 2112150`.
    (
        re.compile(
            r'\((參考|(示意)?圖|畫面顯示|左|右|ETtoday寵物雲|補充官方回應|(註|編按):|本文轉載?自'
            + r'|(科技|[新南]華|人民)([早日]報|網))[^)]*?\)'
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
    # This observation is made with `url_pattern = 1200022, 1200132, 1200161,
    # 1200168, 1200193, 1200234, 1200237, 1200267, 1200392, 1200403, 1200426`.
    (
        re.compile(
            r'(^|\s)(《(ETtoday新聞雲|ET FASHION)》提醒您|\*[圖片、資料]+來源|到這裡找'
            + r'|這裡悶、那裏痛,親友說吃這個藥卡有效|(作者|摘自|Photo|BLOG|粉絲頁|FB)\s*:\s*|◎鎖定'
            + r'|《?ETtoday寵物雲》?期許每個人都能更重視生命|(自殺防治諮詢安心|生命線協談)專線|歡迎加入\S+:)\S+',
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
    # Remove editor notes at the end of news article.
    # This observation is made with `url_pattern = 1200090`.
    (
        re.compile(
            r'\s[圖文]/.*$',
        ),
        ' ',
    ),
    # Remove recommendations and additional informations at the end of news
    # article.  Note that `本文作者:` should be the reporter, but since the
    # format is so fucked up, we say "Fuck it. just remove it".
    # This observation is made with `url_pattern = 1200009,  1200077, 1200081,
    # 1200090, 1200105, 1200165, 1200181, 1200190, 1200193, 1200243, 1200260,
    # 1200265, 1200278, 1200311, 1200318, 1200321, 1200362, 1200413`.
    (
        re.compile(
            r'(\*《ETtoday新聞雲》|好文推薦|【?延伸閱讀】?|更多(時尚藝術資訊|精[彩采]影音|健康訊息)'
            + r'|你可能也想看|關於《(雲端最前線|慧眼看天下)》|\(?本文(由|原刊|(轉載|摘)自|經授權|作者:)'
            + r'|以上言論不代表本網立場|\S+>{3,}|\S+—基本資料|\(?完整文章請看|商品介紹:'
            + r'|本集.ETtoday看電影.|系列報導可詳見).*$',
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
    # 1200335, 1200387, 1200411`.
    (
        re.compile(
            r'\s\S{1,50}(\s*(地址|電話|信箱|票價|基地(規模|位置)|(建築|結構)設計|(報名|舉辦|營業)(日期|時間)'
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
    # Remove content hints.
    # This observation is made with `url_pattern = 1200285, 1200321`.
    (
        re.compile(r'(^|\s)【[^】]*】(→\S+)?(\s|$)'),
        ' ',
    ),
    # (
    #     re.compile(r'【更多新聞】'),
    #     '',
    # ),
    # (
    #     re.compile(r'圖[一二三四五六七八九十]+、'),
    #     '',
    # ),
    # (
    #     re.compile(r'熱門點閱》'),
    #     '',
    # ),
    # (
    #     re.compile(r'原文出處'),
    #     '',
    # ),
]

TITLE_SUB_PATTERNS: List[Tuple[re.Pattern, str]] = [
    # This observation is made with `url_pattern = 1200001, 1200029`.
    (
        re.compile(r'精彩回顧看這邊?!?'),
        '',
    ),
    # Remove content hints.
    # This observation is made with `url_pattern = 1200017, 1200019`.
    (
        re.compile(r'^[^/]*?/'),
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
    # (
    #     re.compile(r'(快[訊讯]|組[圖图]|焦[點点]人物):'),
    #     '',
    # ),
    # (
    #     re.compile(r'(—)+'),
    #     ' ',
    # ),
]


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
        soup = BeautifulSoup(raw_news.raw_xml, 'html.parser')
    except Exception:
        raise ValueError('Invalid html format.')

    ###########################################################################
    # Parsing news article.
    ###########################################################################
    article = ''
    try:
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
        # Some reporters are separated by whitespaces or '、'.
        # This observation is made with `url_pattern = 1200037`.
        reporter = news.parse.util.normalize.NFKC(
            re.sub(
                r'[\s、]+',
                ',',
                reporter,
            )
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
