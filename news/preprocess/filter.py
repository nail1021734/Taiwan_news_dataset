import argparse
import re
from typing import List

from tqdm import tqdm

import news.parse.db.read
import news.parse.db.schema
import news.parse.util.normalize
from news.preprocess.factory import (
    delimiter_filter_factory, pattern_filter_factory
)


def NFKC(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Use NFKC normalize `title`, `article`, `category` and `reporter`.
    """
    # Get function arguments.
    debug = args.debug

    for record in tqdm(dataset, desc='NFKC', disable=not debug):
        record.title = news.parse.util.normalize.NFKC(text=record.title)
        record.article = news.parse.util.normalize.NFKC(text=record.article)

        # Check whether `record.category` is None.
        if record.category:
            # If `record.category` is not None than do NFKC normalize.
            record.category = news.parse.util.normalize.NFKC(
                text=record.category
            )

        # Check whether `record.reporter` is None.
        if record.reporter:
            # If `record.reporter` is not None then do NFKC normalize.
            record.reporter = news.parse.util.normalize.NFKC(
                text=record.reporter
            )

    return dataset


def length_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove articles that are too long or too short.
    """
    # Get function arguments.
    min_length = args.use_min_length_filter
    max_length = args.use_max_length_filter
    debug = args.debug

    result = []
    for record in tqdm(dataset, desc='Length_filter', disable=not debug):
        if max_length != -1:
            if max_length < len(record.article):
                continue
        if min_length > len(record.article):
            continue
        result.append(record)

    return result


# Remove url in articles.
URL_PATTERN = re.compile(r'https?://[A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;%=]+\s*')
url_filter = pattern_filter_factory(pattern=URL_PATTERN)

# Remove emoji in articles.
EMOJI_PATTERN = re.compile(
    pattern="["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "]+",
    flags=re.UNICODE
)
emoji_filter = pattern_filter_factory(pattern=EMOJI_PATTERN)

# Remove text other than Chinese and English.
# Remove too special punctuation and keep only punctuation below.
# `[.~<、,。《?>*-!》:」「+%/]`
REMOVE_CHAR_PATTERN = re.compile(
    r'[^\u4e00-\u9fff.~<、,。《?>*\-!》:」「+%/a-zA-Z\d()\[\]【】]'
)
non_CJK_filter = pattern_filter_factory(pattern=REMOVE_CHAR_PATTERN)

# Remove parentheses and words within parentheses.
parentheses_filter = delimiter_filter_factory(
    left_delimiter='(',
    right_delimiter=')',
)

# Remove brackets and words within brackets.
brackets_filter = delimiter_filter_factory(
    left_delimiter='[',
    right_delimiter=']',
)

# Remove lenticular brackets and words within lenticular brackets.
lenticular_brackets_filter = delimiter_filter_factory(
    left_delimiter='【',
    right_delimiter='】',
)

# Remove curly brackets and words within curly brackets.
curly_brackets_filter = delimiter_filter_factory(
    left_delimiter='{',
    right_delimiter='}',
)
