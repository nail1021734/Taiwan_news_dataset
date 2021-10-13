import unicodedata
from datetime import datetime, timedelta

import dateutil.parser
from bs4 import BeautifulSoup

from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

FILTER_WORDS = [
    '▲',
    '●',
    '▼',
    '★',
    '►',
    '※',
    '【更多新聞】',
    '以上言論不代表本網立場。',
    '圖一、',
    '圖二、',
    '圖三、',
    '圖四、',
    '圖五、',
    '圖六、',
    '圖七、',
    '圖八、',
    '圖九、',
    '圖十、',
    '熱門點閱》',
    '【延伸閱讀】',
    '延伸閱讀：',
    '【】',
    '授權轉載',
    '原文出處',
]
REPORTER_WORDS = ['記者', '中央社', '報導']
NON_REPORTER_WORDS = [',', '。', ':']
TYPICAL_REPORTER_LENGTH = 20


def parse(ori_news: RawNews) -> ParsedNews:
    """Parse ETtoday news from raw HTML.

    Input news must contain `raw_xml` and `url` since these
    information cannot be retrieved from `raw_xml`.
    """
    # Information which cannot be parsed.
    parsed_news = ParsedNews(
        url_pattern=ori_news.url_pattern,
        company_id=ori_news.company_id,
    )

    soup = None
    try:
        soup = BeautifulSoup(ori_news.raw_xml, 'html.parser')
    except Exception:
        raise ValueError('Invalid html format.')

    # News article.
    article = ''
    try:
        article_tags = soup.select('div.story > p:not([class])')
        if not article_tags:
            # ETtoday's bug. They accidentally put a </link>.
            article_tags = soup.select('div.story > link > p:not([class])')

        for article_tag in article_tags:
            # Remove redundant tags.
            for redundant_tag in article_tag.select('a, iframe, img'):
                redundant_tag.extract()

        # Remove strong tags if it contains filter words.
        # Also remove strong tag if its previous sibiling contains filter words.
        # ETtoday's formatting sucks.
        for article_tag in article_tags:
            for strong_tag in article_tag.select('strong'):
                for filter_word in FILTER_WORDS:
                    # Check if previous sibiling exists and contains filter
                    # words.
                    if (strong_tag.previous_sibling
                            and filter_word in strong_tag.previous_sibling):
                        strong_tag.previous_sibling.extract()
                        strong_tag.extract()
                        break
                    # Check if strong tag contains filter words or too short.
                    # When text length equals to 1, it means the text is just a
                    # punctuation mark.
                    if (filter_word in strong_tag.text
                            or len(strong_tag.text) <= 1):
                        strong_tag.extract()
                        break

        for article_tag in article_tags:
            text = article_tag.text.strip()

            # Remove 1 character paragraph which contains punctuation mark.
            if not text or len(text) <= 1:
                article_tag.string = ''
            # Remove remaining paragraph which contains filter words.
            for filter_word in FILTER_WORDS:
                if filter_word in article_tag.text:
                    article_tag.string = ''
                    break

        # Joint remaining text.
        article = ' '.join(
            filter(
                bool,
                map(lambda tag: tag.text.strip(), article_tags),
            )
        )
        article = unicodedata.normalize('NFKC', article).strip()
    except Exception:
        raise ValueError('Fail to parse ETtoday news article.')

    # News category.
    category = ''
    try:
        category = (
            soup.select('div.menu_bread_crumb, div.part_breadcrumb')
            [-1].select('div > a > span')[-1].text
        )
        category = unicodedata.normalize('NFKC', category).strip()
    except Exception:
        # There may not have category.
        category = ''

    # News datetime.
    news_datetime = ''
    try:
        time_tag = soup.select('time[datetime]')[0]
        # When datetime is in UTC+8 format.
        if len(time_tag['datetime']) >= 10:
            news_datetime = dateutil.parser.isoparse(time_tag['datetime']
                                                    ) - timedelta(hours=8)
        # When datetime is useless. Again ETtoday's formatting sucks.
        else:
            news_datetime = time_tag.text.strip()
            news_datetime = datetime.strptime(
                news_datetime,
                '%Y-%m-%d %H:%M',
            ) - timedelta(hours=8)
        news_datetime = news_datetime.timestamp()
    except Exception:
        # There may not have category.
        news_datetime = ''

    # News reporter.
    reporter = ''
    try:
        paragraphs = article.split(' ')
        reporter = paragraphs[0].split('/')[0].strip()

        # Inconsistent format. Again ETtoday's formatting sucks.
        if len(reporter) <= 1:
            reporter = paragraphs[0].split('/')[1].strip()

        is_bad = True
        # It is more possible that short text contains actual reporter. This
        # does not means it is not possible for long text to contains actual
        # reporter, so we cannot set `is_bad = True` when text too long.
        if len(reporter) <= TYPICAL_REPORTER_LENGTH:
            is_bad = False

        # Possible reporter words are build upon observation.
        for reporter_word in REPORTER_WORDS:
            if reporter_word in reporter:
                is_bad = False
                break
        # Non reporter words usually means it reporter is actually a paragraph.
        for non_reporter_word in NON_REPORTER_WORDS:
            if non_reporter_word in reporter:
                is_bad = True
                break

        # When no reporter were found.
        if is_bad:
            reporter = ''
        # When reporter is found, remove reporter from article.
        else:
            article = ' '.join(paragraphs[1:]).strip()
    except Exception:
        # There may not have reporter.
        reporter = ''

    # News title.
    title = ''
    try:
        title = soup.select(
            'h1.title, h1.title_article, div.subject_article > header > h1'
        )[0].text
        title = unicodedata.normalize('NFKC', title).strip()
    except Exception:
        raise ValueError('Fail to parse ETtoday news title.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.datetime = news_datetime
    parsed_news.reporter = reporter
    parsed_news.title = title
    return parsed_news
