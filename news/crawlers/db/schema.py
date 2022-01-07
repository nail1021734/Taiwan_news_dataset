from dataclasses import dataclass


@dataclass
class RawNews:
    idx: int = 0
    company_id: int = 0
    raw_xml: str = ''
    url_pattern: str = ''

    def __iter__(self):
        yield self.idx
        yield self.company_id
        yield self.raw_xml
        yield self.url_pattern
