import re
from typing import Final, List, Tuple
from datetime import datetime
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
    # re.compile(r'\(記者(.*?)(?:綜合|整理)?報導/.*?\)'),
    # re.compile(r'\(記者(.*?)/.*?\)'),
    # re.compile(r'新唐人(\S*?)(?:綜合|整理)?報導'),
    # re.compile(r'^採訪/(.*?)\s*編輯/(.*?)\s*後製/(.*?)$'),
    # re.compile(r'\(責任編輯:(\S*?)\)'),
    # This observation is made with `url_pattern = 2012-01-01-640292,
    # 2012-01-01-640245, 2012-01-01-640054, 2011-12-31-639654,
    # 2011-12-30-639201, 2011-12-30-639175, 2011-12-28-638568`.
    re.compile(r'\(?新唐人(?:記者)?(?:亞太電視)?\s*([\w、]*?)\s*(?:綜合|整理|採訪)?報導。?\)?'),
    # This observation is made with `url_pattern = 2012-01-01-640083`.
    re.compile(r'文字:([^/]+?)/.+$'),
    # This observation is made with `url_pattern = 2021-10-24-103250967`.
    re.compile(r'撰文:([^()]+?)(?:\([^()\s]+?\))?'),
]
ARTICLE_SUB_PATTERNS: Final[List[Tuple[re.Pattern, str]]] = [
    (
        re.compile(r'@\*#'),
        '',
    ),
    # This observation is made with `url_pattern = 2021-10-24-103250967`.
    (
        re.compile(r'\(轉自(.*?)/.*?\)'),
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
    (
        re.compile(r'本文網址:\s*.*?$'),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640292`.
    (
        re.compile(r'^【[^】]*?】'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-12-31-639654,
    # 2011-12-28-638240`.
    (
        re.compile(r'相關(?:鏈接|視頻)(?:新聞)?:.+$'),
        '',
    ),
    # This observation is made with `url_pattern = 2021-10-24-103250967`.
    (
        re.compile(r'製作:\S+?'),
        '',
    ),
    # This observation is made with `url_pattern = 2021-10-24-103250967`.
    (
        re.compile(r'訂閱\S+?:https://\S+?$'),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640316,
    # 2012-01-01-640301, 2012-01-01-640240, 2012-01-01-640096,
    # 2011-12-31-639994`.
    (
        re.compile(r'\(?中央社?(?:記者)?[^()0-9]*?\d*?[^()]*?(電|報導|特稿)\)'),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640301`.
    (
        re.compile(r'\(譯者:[^()]+?\)'),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640045,
    # 2012-01-01-640280, 2011-12-30-639608`.
    (
        re.compile(r'\(本文附帶?照片及?帶?影音\)'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-12-31-639655,
    # 2011-12-29-638743`.
    (
        re.compile(r'\((自由亞洲電台|美國之音)報導\)'),
        '',
    ),
    # Remove traslation and datetime string at the end. This observation is
    # made with `url_pattern = 2011-12-30-639201, 2011-12-30-639463`.
    (
        re.compile(r'''[0-9a-zA-s,.:?!/“”’'"\-\s]+$'''),
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
    # 2011-12-28-638568,
    (
        re.compile(r'([^:])//'),
        r'\1',
    ),
]
TITLE_SUB_PATTERNS: Final[List[Tuple[re.Pattern, str]]] = [
    # Remove content hints. This observation is made with
    # `url_pattern = 2012-01-01-640083`.
    (
        re.compile(r'【[^】]*?】'),
        '',
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
        article = ' '.join(
            map(
                lambda tag: tag.text,
                soup.select('div[itemprop=articleBody].post_content > p')
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
        # Categories are always located in breadcrumbs `div#breadcrumb > a`.
        # The first text in breadcrumb is always '首頁', so we exclude it.
        # The second text in breadcrumb is media type, we also exclude it.
        # There might be more than one category, thus we include them all and
        # save as comma separated format.  Some categories are duplicated, thus
        # we remove it using `list(dict.fromkeys(...))`.  See
        # https://stackoverflow.com/questions/1653970/does-python-have-an-ordered-set
        # for details.  This observation is made with `url_pattern =
        # 2012-01-01-640251`.
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
        reporter = ','.join(reporter_list)
        # Some reporters are separated by '、'.  # This observation is made
        # with `url_pattern = 2012-01-01-640292`.
        reporter = news.parse.util.normalize.NFKC(re.sub('、', ',', reporter))
    except Exception:
        # There may not have reporter.
        reporter = ''

    ###########################################################################
    # Parsing news title.
    ###########################################################################
    title = ''
    try:
        title = soup.select_one('div.article_title > h1').text
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
