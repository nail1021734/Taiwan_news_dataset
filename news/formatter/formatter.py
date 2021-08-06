import news.crawlers.db
import news.parse.db
from news.crawlers.util.normalize import URL_PATTERNS, COMPANY_ID_TABLE
from news.formatter.schema import FormatedNews
from datetime import datetime


def raw_data_formatter(
    dataset: news.crawlers.db.schema.RawNews
) -> FormatedNews:
    result = []
    id_to_company = {v: k for k, v in COMPANY_ID_TABLE.items()}
    for i in dataset:
        company = id_to_company[i.index]
        url = URL_PATTERNS[company] + i.url_pattern
        result.append(FormatedNews(
            company=company,
            url=url,
            raw_xml=i.raw_xml,
        ))
    return result


def parsed_data_formatter(
    dataset: news.parse.db.schema.ParsedNews
) -> FormatedNews:
    result = []
    id_to_company = {v: k for k, v in COMPANY_ID_TABLE.items()}
    for i in dataset:
        company = id_to_company[i.index]
        url = URL_PATTERNS[company] + i.url_pattern
        time = datetime.fromtimestamp(i.datetime)
        date = time.strftime('%Y%m%d')
        result.append(FormatedNews(
            index=i.index,
            article=i.article,
            category=i.category,
            company=company,
            url=url,
            datetime=date,
            reporter=i.reporter,
            title=i.title,
        ))
    return result
