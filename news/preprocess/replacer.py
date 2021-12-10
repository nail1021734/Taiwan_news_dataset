r"""為了保證 ckip 的 NER 效果, 我們認為 NER 的輸入應為不含 tag 的原始文章,因此所有
replacer 的執行順序都應於 NER 前處理之後, 不能於 NER 之前執行.
"""
import argparse
import re
from typing import List

from tqdm import tqdm

import news.parse.db.read
import news.parse.db.schema
import news.parse.util.normalize
from news.preprocess.filters import delimiter_filter_factory
from news.preprocess.ner_preprocessor import TAG_TABLE

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

    def replace_number(text: str):
        rp_text = ''
        last_index = 0
        for match in NUMBER_PATTERN.finditer(text):
            if text[last_index:match.start()].endswith(tag_table):
                continue
            rp_text += text[last_index:match.start()] + '<num>'
            last_index = match.end()
        rp_text += text[last_index:]
        return rp_text

    for record in tqdm(dataset, disable=not debug):
        # Replace numbers in titles.
        record.title = replace_number(text=record.title)
        # Replace numbers in articles.
        record.article = replace_number(text=record.article)

    return dataset


ENGLISH_PATTERN = re.compile(r'[a-zA-z][a-zA-z\s\d]+')


def english_replacer(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Convert English to `<en>` tag.
    """
    # Get function arguments.
    debug = args.debug

    def replace_en(text: str):
        rp_text = ''
        last_index = 0
        for match in ENGLISH_PATTERN.finditer(text):
            # 檢查 match 到的前一個 index 是否小於 0, 以及後一個 index 是否大於
            # `len(text)` 避免超出範圍.
            if match.start() - 1 > -1 and match.end() < len(text):
                # 檢查前一個字元是否為 `<` 以及後一個字元是否為 `>`.
                if (text[match.start() - 1] == '<'
                        and text[match.end()] == '>'):
                    # 如果是就不替換成 `<en>`
                    continue
            rp_text += text[last_index:match.start()] + '<en>'
            last_index = match.end()
        rp_text += text[last_index:]
        return rp_text

    for record in tqdm(dataset, disable=not debug):
        # Replace english in titles.
        record.title = replace_en(text=record.title)
        # Replace english in articles.
        record.article = replace_en(text=record.article)

    return dataset


# Replace word within guillemet with `<unk>`.
guillemet_replacer = delimiter_filter_factory(
    left_delimiter='《',
    right_delimiter='》',
    replace_str='<unk>',
    drop_delimiter=False,
)
