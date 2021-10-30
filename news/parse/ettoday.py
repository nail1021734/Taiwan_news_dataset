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
#   Located in `img`, `div.story > p:not([class]) strong` and `b` tags.
#   Note that `div.story > p:not([class]) strong > span` and
#   `div.story > p:not([class]) span > strong` tags usually appear in the
#   middle of text and thus are highly likely to be part of paragraph instead
#   of captions, the only exception is the last paragraph, i.e.,
#   `div.story > p:not([class]):last-child strong`, which contains extra
#   information.
#   This observation is made with `url_pattern = 2112150, 1200023, 1200034,
#   1200071, 1200075`.
# - Videos:
#   Located in `div.fb-video`
#   This observation is made with `url_pattern = 1200000`.
# - Ads:
#   Located in `div` tags and contains 'ad' in their classname.
#   This observation is made with `url_pattern = 2112150`.
# - App download recommendation:
#   Located in `p` tags immediately precede by a `hr` tag.
#   This observation is made with `url_pattern = 1200011`.
# - Social media links:
#   Located in `div` tags and contains 'social' in their classname.
#   Also exclude instagram post (contains in `blockquote.instagram-media`).
#   This observation is made with `url_pattern = 2112150, 1200040`.
# - Related news:
#   Located in `p.note`, `p a`, `p a strong` and `iframe` tags.
#   This observation is made with `url_pattern = 2112150, 1200077, 1200097`.
ARTICLE_DECOMPOSE_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    img,
    div.story > p:not([class]):not(:has(span[style*="color"] > strong))
    strong:not(:has(span[style*="color"])),
    div.story > p:not([class]):last-child strong,
    b,

    div.fb-video,

    div.ad_readmore,
    div.ad_in_news,
    div[class*='et_ad_group'],
    div[class*='ad_txt'],
    div[class^='ad'],

    hr ~ p,

    div[class*='et_social'],
    blockquote.instagram-media,

    p.note,
    p:has(strong) ~ p a strong,
    p a:has(strong) ~ a strong,
    iframe,
    iframe ~ p a
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
    # 1200002, 1200002, 1200012, 1200021, 1200025, 1200057, 1200071, 1200085`.
    re.compile(
        r'(?:記者|(?:網搜|寵物)小組|(?:體育|國際|社會|大陸|娛樂|地方|生活|財經)中心)'
        + r'([\w、\s]*?)/.*?報導',
    ),
    # This observation is made with `url_pattern = 1200028, 1200034`.
    re.compile(r'文/([\w、]*)(?:\([^)]*\))?\s+'),
]
ARTICLE_SUB_PATTERNS: List[Tuple[re.Pattern, str]] = [
    # Remove captions.
    # This observation is made with `url_pattern = 2112150, 1200012, 1200028`.
    (
        re.compile(r'[▲●▼★►※]\S*。?'),
        '',
    ),
    # Remove captions.
    # This observation is made with `url_pattern = 2112150`.
    (
        re.compile(r'\((示意)?圖[^)]*?\)'),
        '',
    ),
    # Remove recommendations.
    # This observation is made with `url_pattern = 1200009`.
    (
        re.compile(r'\*《ETtoday新聞雲》.*$'),
        '',
    ),
    # Remove recommendations.
    # This observation is made with `url_pattern = 1200077`.
    (
        re.compile(r'\(ETtoday寵物雲[^)]*?\)'),
        '',
    ),
    # Remove recommendations.
    # This observation is made with `url_pattern = 1200077`.
    (
        re.compile(r'(你可能也想看|更多精采影音):?\S*(\s|$)'),
        '',
    ),
    # Remove information source.
    # This observation is made with `url_pattern = 1200022`.
    (
        re.compile(r'\*[圖片、資料]+來源:\S+'),
        '',
    ),
    # Remove editor notes.
    # This observation is made with `url_pattern = 1200039`.
    (
        re.compile(r'(出稿|更新):[\d.:\s]+'),
        '',
    ),
    # Remove update notes.
    # This observation is made with `url_pattern = 1200039`.
    (
        re.compile(r'\(補充官方回應\)'),
        '',
    ),
    # Remove datetime notes.
    # This observation is made with `url_pattern = 1200058`.
    (
        re.compile(r'(報名|舉辦)日期:[\d/()~一二三四五六日]+'),
        '',
    ),
    # Remove copy right notes.
    # This observation is made with `url_pattern = 1200071, 1200090`.
    (
        re.compile(r'\s+(版權聲明:|圖片為版權照片|\*?本文由).*?不得.*?轉載\S*'),
        '',
    ),
    # Remove recommendations.
    # This observation is made with `url_pattern = 1200090`.
    (
        re.compile(r'【延伸閱讀】.*$'),
        '',
    ),
    # Remove news source in fashion category.
    # This observation is made with `url_pattern = 1200090`.
    (
        re.compile(r'更多時尚藝術資訊.*$'),
        '',
    ),
    # Remove picture source.
    # This observation is made with `url_pattern = 1200090`.
    (
        re.compile(r'圖/.*$'),
        '',
    ),
    # Remove article source.  Note that this does not conflict with reporter
    # pattern `文/([\w、]*)(?:\([^)]*\))?\s+` since it is executed after
    # searching reporter pattern.
    # This observation is made with `url_pattern = 1200090`.
    (
        re.compile(r'文/.*$'),
        '',
    ),
    # Remove china news copy source.
    # This observation is made with `url_pattern = 1200098`.
    (
        re.compile(r'\((科技|[新南]華|人民)([早日]報|網)\)'),
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
    #     re.compile(r'延伸閱讀：'),
    #     '',
    # ),
    # (
    #     re.compile(r'【】'),
    #     '',
    # ),
    # (
    #     re.compile(r'授權轉載'),
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
