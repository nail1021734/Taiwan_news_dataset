import re
import unicodedata

from bs4 import BeautifulSoup

from news.db.schema import News

categories = {
    'entertainment': unicodedata.normalize('NFKC', '娛樂'),
    'local': unicodedata.normalize('NFKC', '社會'),
    'life': unicodedata.normalize('NFKC', '生活'),
    'property': unicodedata.normalize('NFKC', '財經地產'),
    'international': unicodedata.normalize('NFKC', '國際'),
    'politics': unicodedata.normalize('NFKC', '政治'),
    'gadget': unicodedata.normalize('NFKC', '3C車市'),
    'supplement': unicodedata.normalize('NFKC', '吃喝玩樂'),
    'sports': unicodedata.normalize('NFKC', '體育'),
    'forum': unicodedata.normalize('NFKC', '蘋評理'),
}

reporter_pattern = re.compile(r'\((.*?)/.*?報導\)')


def parse(ori_news: News) -> News:
    """Parse apple news from raw HTML.

    Input news must contain `datetime`, `raw_xml` and `url` since these
    information cannot be retrieved from `raw_xml`.
    """
    # Information which cannot be parsed.
    parsed_news = News(
        datetime=ori_news.datetime,
        # Minimize `raw_xml`.
        raw_xml=re.sub(r'\s+', ' ', ori_news.raw_xml),
        url=ori_news.url,
    )

    soup = None
    try:
        soup = BeautifulSoup(parsed_news.raw_xml, 'html.parser')
    except Exception:
        raise ValueError('Invalid html format.')

    # News article.
    article = None
    try:
        article_class_ = [
            'text--desktop',
            'text--mobile',
            'article-text-size_md',
            'tw-max_width',
        ]
        article_tags = (
            soup.find('div', id='articleBody')
            .find_all('p', class_=article_class_)
        )
        article = ' '.join([article_tag.text for article_tag in article_tags])
        article = unicodedata.normalize('NFKC', article)
    except Exception:
        raise ValueError('Fail to parse apple news article.')

    # News category.
    category = next(
        iter(i for i in parsed_news.url.split('/') if i in categories.keys()),
        None
    )
    if category is not None:
        category = categories[unicodedata.normalize('NFKC', category)]

    # News reporter.
    reporter = None
    try:
        paragraphs = article.split(' ')
        for paragraph in paragraphs[-2:]:
            possible_reporter = reporter_pattern.findall(paragraph)
            if possible_reporter:
                reporter = possible_reporter[-1]
                break
    except Exception:
        # There may not have reporter.
        pass

    # News title.
    title = None
    try:
        title = (
            soup.find('div', id='article-header').find('header')
            .find('h1', class_='text_medium').find('span').text
        )
        title = unicodedata.normalize('NFKC', title)
    except Exception:
        raise ValueError('Fail to parse apple news title.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.company = '壹傳媒'
    parsed_news.reporter = reporter
    parsed_news.title = title
    return parsed_news
