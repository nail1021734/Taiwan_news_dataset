from dataclasses import dataclass


@dataclass
class ParsedNews:
    index: int = None
    article: str = ''
    category: str = ''
    company_id: str = ''
    datetime: str = ''
    reporter: str = ''
    title: str = ''
    url_pattern: str = ''

    def __iter__(self):
        if self.index:
            yield self.index
        yield self.article
        yield self.category
        yield self.company_id
        yield self.datetime
        yield self.reporter
        yield self.title
        yield self.url_pattern
