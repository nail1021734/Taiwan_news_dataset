from dataclasses import dataclass


@dataclass
class FormatedNews:
    idx: int = 0
    article: str = ''
    category: str = ''
    company: str = ''
    datetime: str = ''
    reporter: str = ''
    title: str = ''
    url: str = ''

    def __iter__(self):
        yield self.idx
        yield self.article
        yield self.category
        yield self.company
        yield self.datetime
        yield self.reporter
        yield self.title
        yield self.url
