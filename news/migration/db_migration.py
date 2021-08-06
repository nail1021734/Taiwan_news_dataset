from tqdm import tqdm

import news.crawlers.db
import news.migration.db
from news.crawlers.util.normalize import (company_id, compress_raw_xml,
                                          compress_url)


def v1(
    dataset: news.migration.db.schema.OriginNews,
) -> news.crawlers.db.schema.RawNews:
    result = []
    for i in tqdm(dataset):
        result.append(
            news.crawlers.db.schema.RawNews(
                company_id=company_id(i.company),
                url_pattern=compress_url(i.url),
                raw_xml=compress_raw_xml(i.raw_xml)
            )
        )
    return result
