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
#   Located in `img`, `p:has(img, iframe) + p:has(strong)` and `b` tags.
#   Note that captions usually follow immediately after `img` or `iframe)`,
#   thus we use `p:has(img, iframe) + p:has(strong)` to capture captions.
#   This observation is made with `url_pattern = 2112150, 1200023, 1200034,
#   1200071, 1200075, 1200173`.
#
# - Extra informations:
#   Paragraphs contains one `strong` tags and at least 3 `a` tags are
#   probabily extra information, thus we use
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
    img,
    p:has(img, iframe) + p:has(strong),
    b,

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
    iframe,
    p:has(a[href*="ettoday"]) a
    ''',
)

# News articles are located in `div.story p(:not([class]))`.
# Sometimes ETtoday has bug, for example, news article might located in
# `div.story > link > p:not([class])` which is caused by forgetting closeing
# `link` tags with `</link>`.  Thus we only use `div.story p(:not([class]))`
# instead of `div.story > p(:not([class]))`.
# This observation is made with `url_pattern = 2112150`.
ARTICLE_SELECTOR_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    div.story p:not([class])
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
    # This observation is made with `url_pattern = 2112150, 1200000, 1200001,
    # 1200002, 1200002, 1200012, 1200021, 1200025, 1200057, 1200071, 1200085,
    # 1200115, 1200125, 1200134, 1200161, 1200181`.
    re.compile(
        r'(?:(?:實習)?記者|(?:網搜|寵物)小組|(?:體育|國際|社會|大陸|娛樂|地方|生活|財經|政治|旅遊|新聞節目)中心)'
        + r'([\w、\s]*?)/.*?(?:綜合)?(?:報導|編譯)',
    ),
    # This observation is made with `url_pattern = 1200028, 1200034, 1200168,
    # 1200197, 1200260`.
    re.compile(
        r'(?:(?:圖、)?文|彙整整理)/(?:(?:藥|護理)師)?([\w、]*?)'
        + r'(?:(?:提供|摘自|圖片)\S*)?(?:\([^)]*\))?\s+'
    ),
]
ARTICLE_SUB_PATTERNS: List[Tuple[re.Pattern, str]] = [
    # Remove captions.  This is still needed even if we have
    # `ARTICLE_DECOMPOSE_LIST` since some captions were located before images.
    # This observation is made with `url_pattern = 2112150, 1200012, 1200028`.
    (
        re.compile(r'[▲▼►]\S*。?'),
        '',
    ),
    # Remove list symbols.
    # This observation is made with `url_pattern = 1200034`.
    (
        re.compile(r'\s[●★](\S*)'),
        r' \1',
    ),
    # Remove additional information in the middle of paragrapgh.
    # This observation is made with `url_pattern = 2112150, 1200090, 1200243,
    # 1200077, 1200039, 1200098, 1200146, 1200190, 1200260`.
    (
        re.compile(
            r'\((參考|(示意)?圖|畫面顯示|左|右|ETtoday寵物雲|補充官方回應|(註|編按):|本文轉載?自'
            + r'|(科技|[新南]華|人民)([早日]報|網))[^)]*?\)'
        ),
        '',
    ),
    # Remove recommendations.
    # This observation is made with `url_pattern = 1200181`.
    (
        re.compile(r'\s(《(ETtoday(筋斗|新聞)雲|播吧)》\s*)*\s'),
        ' ',
    ),
    # Remove paragraphs contains additional informations.
    # This observation is made with `url_pattern = 1200161, 1200022, 1200132,
    # 1200168, 1200234, 1200237, 1200267`.
    (
        re.compile(
            r'\s(《ETtoday新聞雲》提醒您|\*[圖片、資料]+來源|到這裡找|這裡悶、那裏痛,親友說吃這個藥卡有效'
            + r'|(Photo|BLOG|粉絲頁)\s*:\s*|◎鎖定|《?ETtoday寵物雲》?期許每個人都能更重視生命'
            + r'|(自殺防治諮詢安心|生命線協談)專線)\S+',
        ),
        ' ',
    ),
    # Remove suggestion.
    # This observation is made with `url_pattern = 1200058`.
    (
        re.compile(r'《[^》]*》\S+(報名|快訊)\s'),
        ' ',
    ),
    # Remove legal notes.
    # This observation is made with `url_pattern = 1200161`.
    (
        re.compile(r'喝酒不開車,開車不喝酒。?'),
        '',
    ),
    # Remove editor notes.
    # This observation is made with `url_pattern = 1200039`.
    (
        re.compile(r'(出稿|更新):[\d.:\s]+'),
        '',
    ),
    # Remove datetime notes.
    # This observation is made with `url_pattern = 1200058, 1200161`.
    (
        re.compile(r'(報名|舉辦|營業)(日期|時間):[\d:/()~一二三四五六平假日]+'),
        '',
    ),
    # Remove copy right notes.
    # This observation is made with `url_pattern = 1200071, 1200090`.
    (
        re.compile(r'\s+(版權聲明:|圖片為版權照片|\*?本文由).*?不得.*?轉載\S*'),
        '',
    ),
    # Remove recommendations and additional informations at the end of news
    # article.  Note that `本文作者:` should be the reporter, but since the
    # format is so fucked up, we say "Fuck it. just remove it".
    # This observation is made with `url_pattern = 1200009, 1200090, 1200165,
    # 1200190, 1200243, 1200077, 1200181, 1200260, 1200265`.
    (
        re.compile(
            r'\s([圖文]/|\*《ETtoday新聞雲》|好文推薦|【?延伸閱讀】?|更多(時尚藝術資訊|精彩影音|健康訊息)'
            + r'|你可能也想看|關於《雲端最前線》|(本文)?(摘自|經授權|作者:)).*$',
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
    # Remove location, mail, telephone and tick information.
    # This observation is made with `url_pattern = 1200161, 1200254`.
    (
        re.compile(r'\S+(\s*(地址|電話|信箱|票價):\s*\S+)+'),
        '',
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
    # (
    #     re.compile(r'【更多新聞】'),
    #     '',
    # ),
    # (
    #     re.compile(r'以上言論不代表本網立場。'),
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
    # (
    #     re.compile(r'(【[^】]*?】|\([^)]*?\))'),
    #     '',
    # ),
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
        # This observation is made with `url_pattern = 1200034, 1200090`.
        category = re.sub(r'ET(?:today)?([^雲]*)雲?', r'\1', category)
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
