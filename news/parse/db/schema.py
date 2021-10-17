from dataclasses import dataclass


@dataclass
class ParsedNews:
    idx: int = 0
    article: str = ''
    category: str = None  # Some `RawNews` does not have category.
    company_id: int = 0
    datetime: int = 0
    reporter: str = None  # Some `RawNews` does not have reporter.
    title: str = ''
    url_pattern: str = ''

    def __iter__(self):
        yield self.idx
        yield self.article
        yield self.category
        yield self.company_id
        yield self.datetime
        yield self.reporter
        yield self.title
        yield self.url_pattern
