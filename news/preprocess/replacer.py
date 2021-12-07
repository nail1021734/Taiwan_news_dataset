import argparse
import re
from typing import List

from tqdm import tqdm

import news.parse.db.read
import news.parse.db.schema
import news.parse.util.normalize
from news.preprocess.filters import delimiter_filter_factory
from news.preprocess.ner_preprocessor import TAG_TABLE

ENGLISH_PATTERN = re.compile(r'[a-zA-z][a-zA-z\s\d]+')
NUMBER_PATTERN = re.compile(r'\d+')


def number_replacer(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Replace Arabic numerals with `<num>`.
    """
    # Get function arguments.
    debug = args.debug

    # Create tag table.
    tag_table = tuple(TAG_TABLE.values())

    for record in tqdm(dataset, disable=not debug):
        # Replace numbers in titles.
        rp_title = ''
        last_index = 0
        for match in NUMBER_PATTERN.finditer(record.title):
            if record.title[:match.span()[0]].endswith(tag_table):
                continue
            rp_title += record.title[last_index:match.span()[0]] + '<num>'
            last_index = match.span()[1]
        rp_title += record.title[last_index:]

        # Replace numbers in articles.
        rp_article = ''
        last_index = 0
        for match in NUMBER_PATTERN.finditer(record.article):
            if record.article[:match.span()[0]].endswith(tag_table):
                continue
            rp_article += record.article[last_index:match.span()[0]] + '<num>'
            last_index = match.span()[1]
        rp_article += record.article[last_index:]

        # 替換掉原本資料集中的 title 和 article.
        record.title = rp_title
        record.article = rp_article

    return dataset


def english_replacer(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Convert English to `<en>` tag.
    """
    # Get function arguments.
    debug = args.debug

    # Create tag table.
    tag_table = tuple(TAG_TABLE.values()) + ('en', 'num', 'unk')
    # Compile regular expression pattern.
    tag_pattern = re.compile(f"{'|'.join(tag_table)}(\d+)?")

    for record in tqdm(dataset, disable=not debug):
        # Replace numbers in titles.
        rp_title = ''
        last_index = 0
        for match in ENGLISH_PATTERN.finditer(record.title):
            if tag_pattern.match(match.group()):
                continue
            rp_title += record.title[last_index:match.span()[0]] + '<en>'
            last_index = match.span()[1]
        rp_title += record.title[last_index:]

        # Replace numbers in articles.
        rp_article = ''
        last_index = 0
        for match in ENGLISH_PATTERN.finditer(record.article):
            if tag_pattern.match(match.group()):
                continue
            rp_article += record.article[last_index:match.span()[0]] + '<en>'
            last_index = match.span()[1]
        rp_article += record.article[last_index:]

        # 替換掉原本資料集中的 title 和 article.
        record.title = rp_title
        record.article = rp_article

    return dataset


guillemet_replacer = delimiter_filter_factory(
    left_delimiter='《',
    right_delimiter='》',
    replace_str='<unk>',
    drop_delimiter=False,
)
