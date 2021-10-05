from datetime import datetime

import news.crawlers.db
import news.parse.db
from news.crawlers.util.normalize import COMPANY_ID_TABLE, COMPANY_URL
from news.formatter.schema import FormatedNews


def raw_data_formatter(
    dataset: news.crawlers.db.schema.RawNews
) -> FormatedNews:
    r"""將 raw data 中的 `url_pattern` 改為完整 URL, 以及 `company_id` 改回公司名"""
    result = []

    # 將company對應id的table改為id對應company的table
    id_to_company = {v: k for k, v in COMPANY_ID_TABLE.items()}

    # 對每一筆資料進行轉換
    for i in dataset:
        company = id_to_company[i.idx]
        url = COMPANY_URL[company] + i.url_pattern
        result.append(FormatedNews(
            idx=i.idx,
            company=company,
            url=url,
            raw_xml=i.raw_xml,
        ))
    return result


def parsed_data_formatter(
    dataset: news.parse.db.schema.ParsedNews
) -> FormatedNews:
    r"""將 parsed data 中的 `url_pattern` 改為完整 URL, 以及 `company_id` 改回公司名"""
    result = []

    # 將company對應id的table改為id對應company的table
    id_to_company = {v: k for k, v in COMPANY_ID_TABLE.items()}

    # 對每一筆資料進行轉換
    for i in dataset:
        company = id_to_company[i.idx]
        url = COMPANY_URL[company] + i.url_pattern
        time = datetime.fromtimestamp(i.datetime)
        date = time.strftime('%Y%m%d')
        result.append(FormatedNews(
            idx=i.idx,
            article=i.article,
            category=i.category,
            company=company,
            url=url,
            datetime=date,
            reporter=i.reporter,
            title=i.title,
        ))
    return result
