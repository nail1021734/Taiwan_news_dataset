from dataclasses import dataclass


@dataclass
class ParsedNews:
    article: str = ''
    category: str = ''
    company_id: str = ''
    datetime: str = ''
    reporter: str = ''
    title: str = ''
    url_pattern: str = ''

    def __iter__(self):
        yield self.article
        yield self.category
        yield self.company_id
        yield self.datetime
        yield self.reporter
        yield self.title
        yield self.url_pattern
