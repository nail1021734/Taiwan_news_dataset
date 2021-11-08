import re
from datetime import datetime
from typing import List, Tuple

from bs4 import BeautifulSoup

import news.parse.util.normalize
from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

# There are at least two article patterns, and these patterns are mutually
# exclusive (in other words, only one pattern applies to each news).  We use
# selector lists (selectors separated by comma) to denote all article patterns.
# This observation is made with `url_pattern = 2012-01-01-640251,
# 2011-04-12-517548`.
#
# In the pattern `div[itemprop=articleBody].post_content > p`, some of the
# article contains image captions, thus we remove it using
# `:not(:has(a:has(img)))`.
# This observation is made with `url_pattern = 2011-04-11-517450`.
ARTICLE_SELECTOR_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    div[itemprop=articleBody].post_content > p:not(:has(a:has(img))),
    div.article_content > p
    ''',
)

# There are at least two title patterns, and these patterns are mutually
# exclusive (in other words, only one pattern applies to each news). We use
# selector lists (selectors separated by comma) to denote all title patterns.
# This observation is made with `url_pattern = 2012-01-01-640251,
# 2011-04-12-517548`.
TITLE_SELECTOR_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    div.article_title > h1,
    div.main_title
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
    # This observation is made with `url_pattern = 2012-01-01-640292,
    # 2012-01-01-640245, 2012-01-01-640054, 2011-12-31-639654,
    # 2011-12-30-639201, 2011-12-30-639175, 2011-12-28-638568,
    # 2011-12-25-636878, 2011-12-22-635455, 2011-12-21-635019,
    # 2011-12-20-634655, 2011-12-18-633615, 2011-12-15-632140,
    # 2011-12-13-631155, 2011-04-17-519983, 2011-04-15-519037,
    # 2018-11-26-1400746`.
    re.compile(
        r'\(?(?:[這这]是)?新[唐塘]人[記记]?者?(?:亞太)?(?:[電电][視视][台臺]?)?'
        + r'([\w、\s]*?)(?:的|在)?(?:香港|[综綜]合|整理|[採采][訪访])?(?:)'
        + r'[報报][導导道]?。?\)?'
    ),
    # This observation is made with `url_pattern = 2018-12-10-102462948,
    # 2018-12-29-102476332`.
    re.compile(
        r'\(?(?:[這这]是|轉自)?新?[唐塘]?人?[記记]?者?(?:亞太|大紀元)?(?:[電电][視视][台臺]?)?'
        + r'([\w、\s]*?)的?(?:[综綜]合|整理|[採采][訪访])?[報报]?[導导道]?'
        + r'(?:/?責任編輯:[^\)]*)。?\)?'
    ),
    # This observation is made with `url_pattern = 2018-09-17-1391777`.
    re.compile(
        r'\(?(?:[這这]是)?新[唐塘]人[記记]?者?(?:亞太)?(?:[電电][視视][台臺]?)?'
        + r'([\w、\s]*?)。?\)?$'
    ),
    # This observation is made with `url_pattern = 2012-01-01-640083`.
    re.compile(r'文字:([^/]+?)/.+$'),
    # This observation is made with `url_pattern = 2013-08-04-943508,
    # 2013-08-04-943532`.
    re.compile(
        r'(?:[採采][訪访])?(?:[記记]者/\s*([^\s;。]+))'
        + r'(?:;?(?:[編编][輯辑]|[後后][製制]|旁白)/[^;。]+)+。?'
    ),
]
ARTICLE_SUB_PATTERNS: List[Tuple[re.Pattern, str]] = [
    # This observation is made with `url_pattern = 2011-04-17-519983,
    # 2011-04-16-519478`.
    (
        re.compile(r'\(([攝摄]影|[圖图]片):[^)]+?\)'),
        '',
    ),
    (
        re.compile(r'@\*#'),
        '',
    ),
    # Note that `ord('–') == 8211`, `ord('—') == 8212` and `ord('─') == 9472`.
    # This observation is made with `url_pattern = 2021-10-24-103250967,
    # 2011-12-23-635993, 2011-04-11-517450, 2011-03-30-512271`.
    (
        re.compile(r'[—–─]*\(?[轉转]自[^)\s]*?\)?\s*(有[刪删][節节])?$'),
        '',
    ),
    (
        re.compile(r'─+[點点][閱阅]\s*【.*?】\s*─+'),
        '',
    ),
    (
        re.compile(r'[點点][閱阅]\s*【.*?】\s*系列文章'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-04-15-519169`.
    (
        re.compile(r'美[東东][時时][间間]:\s*.*?【[萬万]年[曆历]】'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-04-15-519169,
    # 2011-07-14-559558`.
    (
        re.compile(r'(本文|影片)[網网]址[為为]?:?\s*.*$'),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640292,
    # 2011-12-14-631632`.
    (
        re.compile(r'^(【[^】]*?】)+'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-04-17-519966,
    # 2011-04-03-514098`.
    (
        re.compile(r'【新[唐塘]人[^】]*?[訊讯]】?'),
        '',
    ),
    # Remove useless last paragraph with at most one space in between. This
    # observation is made with `url_pattern = 2011-12-20-634477`.
    (
        re.compile(r'【禁[聞闻]】\S+?\s?\S+?$'),
        '',
    ),
    # Remove draft notes at the end. This observation is made with
    # `url_pattern = 2011-12-18-633616`.
    (
        re.compile(r'待完成$'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-12-31-639654,
    # 2011-12-28-638240, 2011-12-26-637243`.
    (
        re.compile(r'相[關关]([鏈链][接結]|[視视][頻频]|新[聞闻])+?:.*$'),
        '',
    ),
    # This observation is made with `url_pattern = 2021-10-24-103250967`.
    (
        re.compile(r'(撰文|[製制]作):.*$'),
        ' ',
    ),
    # This observation is made with `url_pattern = 2021-10-24-103250967`.
    (
        re.compile(r'[訂订][閱阅]\S+?:https://\S+?$'),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640316,
    # 2012-01-01-640301, 2012-01-01-640240, 2012-01-01-640096,
    # 2011-12-31-639994, 2011-04-17-519993, 2011-04-17-519859,
    # 2011-04-11-517227`.
    (
        re.compile(
            r'\(?(大[紀纪]元|中央社?)([記记]者)?'
            + r'[^()0-9]*?\d*?[^()]*?([電电]|[報报][導导道]|特稿|社)\)',
        ),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640301,
    # 2011-12-23-636434, 2011-04-12-517789, 2011-04-09-516789`.
    (
        re.compile(r'\(([實实][習习])?[編编]?[譯译]者?(:|;)[^)]+\)?'),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640045,
    # 2012-01-01-640280, 2011-12-30-639608, 2011-12-26-637451,
    # 2011-12-25-636915, 2011-04-02-513571, 2011-07-27-565336,
    # 2011-06-11-545215`.
    (
        re.compile(r'\(本文[附有帶带影音照相片及和與与]+\)'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-12-31-639655,
    # 2011-12-29-638743, 2011-12-28-638138, 2011-12-26-637224,
    # 2011-12-17-633228, 2014-01-01-1035035, 2014-01-01-1034743,
    # 2014-01-01-1034722, 2013-12-28-1032509, 2013-12-19-1026801,
    # 2013-03-26-869872`.
    (
        re.compile(
            r'\((自由亞洲電[臺台]|美[國国]之音)[^)]*?[报報導导道電]*?\)',
        ),
        '',
    ),
    # This observation is made with `url_pattern = 2011-12-26-636848,
    # 2011-12-19-633545, 2011-12-19-633525`.
    (
        re.compile(r'社[區区][廣广]角[鏡镜]\(\d+?\)(提要:)?'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-12-18-633615,
    # 2011-04-17-519866`.
    (
        re.compile(r'新[聞闻][週周]刊\(?\d+\)?期?'),
        '',
    ),
    # Remove section header symbols. This observation is made with `url_pattern
    # = 2011-04-10-516866`.
    (
        re.compile(r'\*(\S*?)\*'),
        r'\1',
    ),
    # Remove list item symbols. This observation is made with
    # `url_pattern = 2011-12-28-638636, 2011-12-28-638635, 2011-12-28-638631,
    # 2011-12-28-638568`.
    (
        re.compile(r'\s+(★|●|•)'),
        ' ',
    ),
    # Remove figure references. This observation is made with
    # `url_pattern = 2011-12-28-638568, 2011-04-11-517502, 2011-03-29-511547`.
    (
        re.compile(r'(\[[圖图]卡\d*\]\s*|\([圖图]片來源:.*?\))'),
        '',
    ),
    # Remove wierd typos. This observation is made with `url_pattern =
    # 2011-12-28-638568.`
    (
        re.compile(r'([^:])//'),
        r'\1',
    ),
    # Remove website references. This observation is made with `url_pattern =
    # 2011-12-21-635020, 2011-04-14-518790, 2011-04-07-515910`.
    (
        re.compile(
            r'新[唐塘]人[電电][視视][臺台]\s*((https?://)?www\.ntdtv\.com)?',
        ),
        '',
    ),
    # Remove download links. This observation is made with `url_pattern =
    # 2011-12-21-635020, 2011-04-12-517801, 2011-04-11-517355,
    # 2011-04-08-516206`.
    (
        re.compile(r'(下[載载][錄录]像)'),
        '',
    ),
    # Remove content references. This observation is made with `url_pattern =
    # 2011-04-12-517801, 2011-04-11-517355, 2011-04-08-516206`.
    (
        re.compile(r'\([畫画]面.*?[報报][導导道]\)'),
        '',
    ),
    # Remove left along symbols at the begin. This observation is made with
    # `url_pattern = 2011-12-17-633460, 2011-04-12-517593`.
    (
        re.compile(r'^(主播)?\)'),
        '',
    ),
    # Remove related news tags. This observation is made with `url_pattern =
    # 2011-04-17-519966`.
    (
        re.compile(r'\s+相[關关]新聞\s+'),
        ' ',
    ),
    # Remove unclear links. This observation is made with `url_pattern =
    # 2011-04-14-518847, 2013-12-27-1032242`.
    (
        re.compile(
            r'(\.html#video\s*target=_blank|'
            + r'frameborder="0′′\s*allowfullscreen)>'
        ),
        '',
    ),
    # Remove the editor information. This observation is made with `url_pattern
    # = 2018-03-04-1365990, 2018-08-06-1386361, 2018-11-21-1400130`.
    (
        re.compile(
            r'\s*(?:[採采][訪访]|[編编][輯辑]|[後后][製制]|撰稿)?'
            + r'(?:[採采][訪访]|[編编][輯辑]|[後后][製制]|撰稿)[:/]\w*'
        ),
        '',
    ),
    # Remove the to be continue information. This observation is made with
    # `url_pattern = 2018-12-25-102473518`.
    (
        re.compile(r'\(未完待[續续]'),
        '',
    ),
    # Remove special suffix at the end of article. `url_pattern =
    # 2013-08-20-952909, 2013-04-17-882078, 2013-12-25-1030400,
    # 2013-12-20-1028082, 2013-03-27-870104, 2013-03-25-869138,
    # 2013-08-19-951813, 2013-08-16-950720, 2013-08-15-950231,
    # 2013-08-15-950276, 2013-04-23-885733`
    (
        re.compile(
            r'\s*\(?((相[關关]|youtube)([網网][絡路][圖图]片|視[頻频])|'
            + r'[資资]料[來来]源|[熱热][線线][電电][話话]:' + r'|本文只代表作者的)\S*\)?\s*$',
            re.IGNORECASE
        ),
        '',
    ),
    # Remove traslation and datetime string at the end. Note that
    # `ord('–') == 8211`, `ord('—') == 8212` and `ord('─') == 9472`.  Also note
    # that always leave this pattern at the last of all patterns since this
    # pattern removes everything the above patterns does not match.
    # This observation is made with `url_pattern = 2011-12-30-639201,
    # 2011-12-30-639463, 2011-12-24-636612, 2011-12-24-636565,
    # 2011-12-21-634964, 2011-12-22-635525, 2011-12-20-634431,
    # 2011-12-20-634429, 2011-12-17-633168, 2011-12-15-632169,
    # 2011-04-14-518582, 2011-04-04-514246`.
    (
        re.compile(r'''[0-9a-zA-ZÀ-ÿ,.:;?!&/“”’'"$%『』\[\]()*=—–─\-\s]+$'''),
        '',
    ),
]
TITLE_SUB_PATTERNS: List[Tuple[re.Pattern, str]] = [
    # Remove content hints. This observation is made with `url_pattern =
    # 2012-01-01-640083, 2011-04-12-517801, 2011-12-23-636402`.
    (
        re.compile(r'(【[^】]*?】|\([^)]*?\))'),
        '',
    ),
    # Remove content hints without parentheses. This observation is made with
    # `url_pattern = 2011-04-16-519478, 2011-04-04-514182, 2011-07-06-555876`.
    (
        re.compile(r'(快[訊讯]|組[圖图]|焦[點点]人物):'),
        '',
    ),
    # Remove useless symbols. This observation is made with `url_pattern =
    # 2011-12-20-634431`.
    (
        re.compile(r'(—)+'),
        ' ',
    ),
]


def parser(raw_news: RawNews) -> ParsedNews:
    """Parse NTDTV news from raw HTML.

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
        article = ' '.join(
            map(lambda tag: tag.text, soup.select(ARTICLE_SELECTOR_LIST))
        )
        article = news.parse.util.normalize.NFKC(article)
    except Exception:
        raise ValueError('Fail to parse NTDTV news article.')

    ###########################################################################
    # Parsing news category.
    ###########################################################################
    category = ''
    try:
        # Sometimes news does not have categories, but if they do,  categories
        # are always located in breadcrumbs `div#breadcrumb > a`.
        # The first text in breadcrumb is always '首頁', so we exclude it.
        # The second text in breadcrumb is media type, we also exclude it.
        # There might be more than one category.  Thus we include them all and
        # save as comma separated format.  Some categories are duplicated, thus
        # we remove it using `list(dict.fromkeys(...))`.  See
        # https://stackoverflow.com/questions/1653970/does-python-have-an-ordered-set
        # for details.
        # This observation is made with `url_pattern = 2012-01-01-640251,
        # 2011-04-12-517548`.
        category = ','.join(
            list(
                dict.fromkeys(
                    map(
                        lambda tag: tag.text,
                        soup.select('div#breadcrumb > a')[2:],
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
        timestamp = int(
            datetime.strptime(
                parsed_news.url_pattern[:10],
                '%Y-%m-%d',
            ).timestamp()
        )
    except Exception:
        raise ValueError('Fail to parse NTDTV news datetime.')

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
        # Some reporters are separated by whitespaces or '、'.  This
        # observation is made with `url_pattern = 2012-01-01-640292,
        # 2011-12-15-632140, 2011-04-12-517593`.
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
        raise ValueError('Fail to parse NTDTV news title.')

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
        raise ValueError('Fail to substitude NTDTV article pattern.')

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
        raise ValueError('Fail to substitude NTDTV title pattern.')

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
