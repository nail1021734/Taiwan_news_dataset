from dataclasses import dataclass


@dataclass
class RawNews:
    index: int = 0
    company_id: str = ''
    raw_xml: str = ''
    url_pattern: str = ''

    def __iter__(self):
        yield self.index
        yield self.company_id
        yield self.raw_xml
        yield self.url_pattern
