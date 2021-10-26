import re
from datetime import datetime
from typing import Final, List, Tuple

from bs4 import BeautifulSoup

import news.parse.util.normalize
from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

###############################################################################
#                                 WARNING:
# Patterns (including `REPORTER_PATTERNS`, `ARTICLE_SUB_PATTERNS`,
# `TITLE_SUB_PATTERNS`) MUST remain unordered, in other words, the order of
# execution WILL NOT and MUST NOT effect the parsing results.
# `REPORTER_PATTERNS` MUST have exactly ONE group.  You can use `(?...)`
# pattern as non-capture group, see python's re module for details.
###############################################################################
REPORTER_PATTERNS: Final[List[re.Pattern]] = [
    # re.compile(r'^採訪/(.*?)\s*編輯/(.*?)\s*後製/(.*?)$'),
    # re.compile(r'\(責任編輯:(\S*?)\)'),
    # This observation is made with `url_pattern = 2012-01-01-640292,
    # 2012-01-01-640245, 2012-01-01-640054, 2011-12-31-639654,
    # 2011-12-30-639201, 2011-12-30-639175, 2011-12-28-638568,
    # 2011-12-25-636878, 2011-12-22-635455, 2011-12-21-635019,
    # 2011-12-20-634655, 2011-12-18-633615, 2011-12-15-632140,
    # 2011-12-13-631155, 2011-04-17-519983, 2011-04-15-519037`.
    re.compile(
        r'\(?(?:這是)?新(?:唐|塘)人(?:記|记)?者?(?:亞太)?(?:電視臺?)?([\w、\s]*?)'
        + r'的?(?:(?:综|綜)合|整理|(?:採|采)訪)?(?:報|报)(?:導|导|道)。?\)?'
    ),
    # This observation is made with `url_pattern = 2012-01-01-640083`.
    re.compile(r'文字:([^/]+?)/.+$'),
]
ARTICLE_SUB_PATTERNS: Final[List[Tuple[re.Pattern, str]]] = [
    # This observation is made with `url_pattern = 2011-04-17-519983,
    # 2011-04-16-519478`.
    (
        re.compile(r'\((攝影|圖片):[^)]+?\)'),
        '',
    ),
    (
        re.compile(r'@\*#'),
        '',
    ),
    # This observation is made with `url_pattern = 2021-10-24-103250967,
    # 2011-12-23-635993`.
    (
        re.compile(r'—*\(?轉自[^)\s]*?\)?$'),
        '',
    ),
    (
        re.compile(r'─+點閱\s*【.*?】\s*─+'),
        '',
    ),
    (
        re.compile(r'點閱\s*【.*?】\s*系列文章'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-04-15-519169`.
    (
        re.compile(r'美東時間:\s*.*?【萬年曆】'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-04-15-519169`.
    (
        re.compile(r'本文網址:\s*.*$'),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640292,
    # 2011-12-14-631632`.
    (
        re.compile(r'^(【[^】]*?】)+'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-04-17-519966`.
    (
        re.compile(r'【新唐人[^】]*?訊】'),
        '',
    ),
    # Remove useless last paragraph with at most one space in between. This
    # observation is made with `url_pattern = 2011-12-20-634477`.
    (
        re.compile(r'【禁聞】\S+?\s?\S+?$'),
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
        re.compile(r'相關(鏈接|視頻|新聞)+?:.*$'),
        '',
    ),
    # This observation is made with `url_pattern = 2021-10-24-103250967`.
    (
        re.compile(r'(撰文|製作):.*$'),
        ' ',
    ),
    # This observation is made with `url_pattern = 2021-10-24-103250967`.
    (
        re.compile(r'訂閱\S+?:https://\S+?$'),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640316,
    # 2012-01-01-640301, 2012-01-01-640240, 2012-01-01-640096,
    # 2011-12-31-639994, 2011-04-17-519993, 2011-04-17-519859`.
    (
        re.compile(r'\(?(大紀元|中央社?)(記者)?[^()0-9]*?\d*?[^()]*?(電|報導|特稿|社)\)'),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640301,
    # 2011-12-23-636434`.
    (
        re.compile(r'\(譯者:[^)]+\)?'),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640045,
    # 2012-01-01-640280, 2011-12-30-639608, 2011-12-26-637451,
    # 2011-12-25-636915`.
    (
        re.compile(r'\(本文附(有|帶)?照片及?帶?(影音)?\)'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-12-31-639655,
    # 2011-12-29-638743, 2011-12-28-638138, 2011-12-26-637224,
    # 2011-12-17-633228`.
    (
        re.compile(r'\((自由亞洲電(臺|台)|美國之音)[^)]*?(报|報)導\)'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-12-26-636848,
    # 2011-12-19-633545, 2011-12-19-633525`.
    (
        re.compile(r'社(區|区)(廣|广)角(鏡|镜)\(\d+?\)(提要:)?'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-12-18-633615,
    # 2011-04-17-519866`.
    (
        re.compile(r'新(聞|闻)(週|周)刊\(?\d+\)?期?'),
        '',
    ),
    # Remove traslation and datetime string at the end. This observation is
    # made with `url_pattern = 2011-12-30-639201, 2011-12-30-639463,
    # 2011-12-24-636612, 2011-12-24-636565, 2011-12-21-634964,
    # 2011-12-22-635525, 2011-12-20-634431, 2011-12-20-634429,
    # 2011-12-17-633168, 2011-12-15-632169`.
    (
        re.compile(r'''[0-9a-zA-sÀ-ÿ,.:;?!/“”’'"$%『』\[\]()*=—\-\s]+$'''),
        '',
    ),
    # Remove list item symbols. This observation is made with
    # `url_pattern = 2011-12-28-638636, 2011-12-28-638635, 2011-12-28-638631,
    # 2011-12-28-638568`.
    (
        re.compile(r'\s+(★|●|•)'),
        ' ',
    ),
    # Remove figure references. This observation is made with
    # `url_pattern = 2011-12-28-638568`.
    (
        re.compile(r'\[圖卡\d+\]\s*'),
        '',
    ),
    # Remove wierd typos. This observation is made with `url_pattern =
    # 2011-12-28-638568.`
    (
        re.compile(r'([^:])//'),
        r'\1',
    ),
    # Remove download links. This observation is made with `url_pattern =
    # 2011-12-21-635020, 2011-04-17-519966`.
    (
        re.compile(r'(下載錄像)?\s*新唐人電視台\s*((https?://)?www\.ntdtv\.com)?'),
        '',
    ),
    # Remove left along symbols at the begin. This observation is made with
    # `url_pattern = 2011-12-17-633460`.
    (
        re.compile(r'^\)'),
        '',
    ),
    # Remove related news tags. This observation is made with `url_pattern =
    # 2011-04-17-519966`.
    (
        re.compile(r'\s+相關新聞\s+'),
        ' ',
    ),
]
TITLE_SUB_PATTERNS: Final[List[Tuple[re.Pattern, str]]] = [
    # Remove content hints. This observation is made with `url_pattern =
    # 2012-01-01-640083`.
    (
        re.compile(r'【[^】]*?】'),
        '',
    ),
    # Remove picture hints. This observation is made with `url_pattern =
    # 2011-12-23-636402, 2011-04-16-519478`.
    (
        re.compile(r'\(?組圖:?\)?'),
        '',
    ),
    # Remove useless symbols. This observation is made with `url_pattern =
    # 2011-12-20-634431`.
    (
        re.compile(r'(—)+'),
        ' ',
    ),
]


def parser(raw_news: Final[RawNews]) -> ParsedNews:
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
        # There are at least two article patterns, and these patterns are
        # mutually exclusive (in other words, only one pattern applies to each
        # news). We use selector lists (selectors separated by comma) to denote
        # all article patterns. This observation is made with `url_pattern =
        # 2012-01-01-640251, 2011-04-12-517548`.
        article = ' '.join(
            map(
                lambda tag: tag.text,
                soup.select(
                    'div[itemprop=articleBody].post_content > p,'
                    + 'div.article_content > p'
                )
            )
        )
        article = news.parse.util.normalize.NFKC(article)
    except Exception:
        raise ValueError('Fail to parse NTDTV news article.')

    ###########################################################################
    # Parsing news category.
    ###########################################################################
    category = ''
    try:
        # Sometimes news does not have categories, but if they have, then
        # categories are always located in breadcrumbs `div#breadcrumb > a`.
        # The first text in breadcrumb is always '首頁', so we exclude it.
        # The second text in breadcrumb is media type, we also exclude it.
        # There might be more than one category, thus we include them all and
        # save as comma separated format.  Some categories are duplicated, thus
        # we remove it using `list(dict.fromkeys(...))`.  See
        # https://stackoverflow.com/questions/1653970/does-python-have-an-ordered-set
        # for details.  This observation is made with `url_pattern =
        # 2012-01-01-640251, 2011-04-12-517548`.
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
    news_datetime = ''
    try:
        # Some news publishing date time are different to URL pattern.  For
        # simplicity we only use URL pattern to represent the same news.  News
        # datetime will convert to POSIX time (which is under UTC time zone).
        news_datetime = int(
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
        for reporter_pattern in REPORTER_PATTERNS:
            # There might have more than one pattern matched.
            reporter_list.extend(reporter_pattern.findall(article))
            # Remove reporter text from article.
            article = news.parse.util.normalize.NFKC(
                reporter_pattern.sub('', article)
            )

        # Reporters are comma seperated.
        reporter = ','.join(map(news.parse.util.normalize.NFKC, reporter_list))
        # Some reporters are separated by whitespaces or '、'.  This
        # observation is made with `url_pattern = 2012-01-01-640292,
        # 2011-12-15-632140`.
        reporter = news.parse.util.normalize.NFKC(
            re.sub(
                r'(\s|、)',
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
        # There are at least two title patterns, and these patterns are
        # mutually exclusive (in other words, only one pattern applies to each
        # news). We use selector lists (selectors separated by comma) to denote
        # all title patterns. This observation is made with `url_pattern =
        # 2012-01-01-640251, 2011-04-12-517548`.
        title = soup.select_one('div.article_title > h1, div.main_title').text
        title = news.parse.util.normalize.NFKC(title)
        # Discard trash news.
        if '【熱門話題】' in title:
            article = ''
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
    parsed_news.datetime = news_datetime
    if reporter:
        parsed_news.reporter = reporter
    else:
        parsed_news.reporter = ParsedNews.reporter
    parsed_news.title = title
    return parsed_news
    return parsed_news
