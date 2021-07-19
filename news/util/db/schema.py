from dataclasses import dataclass


@dataclass
class News:
    article: str = ''
    category: str = ''
    company: str = ''
    datetime: str = ''
    raw_xml: str = ''
    reporter: str = ''
    title: str = ''
    url: str = ''

    def __iter__(self):
        yield self.article
        yield self.category
        yield self.company
        yield self.datetime
        yield self.raw_xml
        yield self.reporter
        yield self.title
        yield self.url
