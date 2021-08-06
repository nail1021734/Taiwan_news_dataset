from dataclasses import dataclass


@dataclass
class OriginNews:
    index: int = None
    article: str = ''
    category: str = ''
    company: str = ''
    datetime: str = ''
    reporter: str = ''
    title: str = ''
    url: str = ''
    raw_xml: str = ''

    def __iter__(self):
        yield self.index
        yield self.article
        yield self.category
        yield self.company
        yield self.datetime
        yield self.reporter
        yield self.title
        yield self.url
        yield self.raw_xml
