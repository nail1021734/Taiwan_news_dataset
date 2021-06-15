from dataclasses import dataclass


@dataclass
class News:
    article: str = None
    category: str = None
    company: str = None
    datetime: str = None
    raw_xml: str = None
    reporter: str = None
    title: str = None
    url: str = None

    def __iter__(self):
        yield self.article
        yield self.category
        yield self.company
        yield self.datetime
        yield self.raw_xml
        yield self.reporter
        yield self.title
        yield self.url
