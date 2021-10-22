import unicodedata
from typing import Final

import news.crawlers.util.normalize


def NFKC(text: Final[str]) -> str:
    r"""Normalized by NFKC then collapse multiple whitespaces."""
    return news.crawlers.util.normalize.compress_raw_xml(
        raw_xml=unicodedata.normalize('NFKC', text),
    )
