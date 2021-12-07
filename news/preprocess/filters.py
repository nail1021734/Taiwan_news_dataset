import argparse
import re
from typing import Callable, List

from tqdm import tqdm

import news.parse.db.read
import news.parse.db.schema
import news.parse.util.normalize

URL_PATTERN = re.compile(r'https?://[A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;%=]+\s*')
EMOJI_PATTERN = re.compile(
    pattern="["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "]+",
    flags=re.UNICODE
)
REMOVE_CHAR_PATTERN = re.compile(
    r'[^\u4e00-\u9fff.~<、,。《?>*\-!》:」「+%/a-zA-Z\d()\[\]【】]'
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
    for i in tqdm(dataset, desc='Length_filter', disable=not debug):
        if max_length != -1:
            if max_length < len(i.article):
                continue
        if min_length > len(i.article):
            continue
        result.append(i)

    return result


def find_delimiter(
    article: str,
    left_delimiter: str,
    right_delimiter: str,
    replace_str: str = '',
    drop_delimiter: bool = True,
) -> str:
    r"""將 `article` 內 `left_delimiter` 和 `right_delimiter` 之間的字串替換為 `replace_str`.

    Parameters
    ==========
    `article`: str
        要處理的文章.
    `left_delimiter`: str
        `left_delimiter` 與 `right_delimiter` 內的字串會被替換為 `replace_str`.
    `right_delimiter`: str
        `left_delimiter` 與 `right_delimiter` 內的字串會被替換為 `replace_str`.
    `replace_str`: str
        選擇要替換的字串.
    `drop_delimiter`: bool
        若為 True 則會將 `left_delimiter` 與 `right_delimiter` 一起替換掉, 為 False 則會將
        `left_delimiter` 與 `right_delimiter` 保留下來.
    """
    # A stack to count `left_delimiter` hit amount.
    count_stack = 0

    # `rp_article` 為最後回傳的文章.
    rp_article = ''
    last_index = 0
    for i, char in enumerate(article):
        if char == left_delimiter:
            if count_stack == 0:
                # 若 `count_stack == 0` 表示遇到開頭的 `left_delimiter`.
                # 若不等於 0 表示先前已經遇過還沒匹配到 `right_delimiter` 的 `left_delimiter`.

                # 將 `left_delimiter` 之前的文章片段加到 `rp_article` 之中.
                rp_article += article[last_index:i]
                if not drop_delimiter:
                    # 將 `left_delimiter` 加到 `rp_article` 之中.
                    rp_article += left_delimiter
            count_stack += 1

        if char == right_delimiter:
            if count_stack > 0:
                # 若 `count_stack > 0` 則 pop 一個元素.
                count_stack -= 1
            else:
                # 若 `count_stack == 0` 則直接跳過後續處理(表示沒有匹配的
                # `left_delimiter` 無視此 `right_delimiter`).
                continue
            if count_stack == 0:
                # 若 pop 一個元素後 `count_stack == 0` 表示此 `right_delimiter`
                # 有匹配的 `left_delimiter` 並且是最外層的 `left_delimiter`.

                # 使用 `replace_str` 代替先前的文章片段.
                rp_article += replace_str
                if not drop_delimiter:
                    # 保留 `right_delimiter`.
                    rp_article += right_delimiter

                # 更新 `last_index` 到 `right_delimiter` 的下一個索引.
                last_index = i + 1

    # 將 `last_index` 之後的文章, 加到 `rp_article` 之後.
    rp_article += article[last_index:]
    return rp_article


def filter_factory(re_pattern: str,) -> Callable:
    r"""生成一般的 filter function.
    """

    def func(
        dataset: List[news.parse.db.schema.ParsedNews],
        args: argparse.Namespace,
    ) -> List[news.parse.db.schema.ParsedNews]:
        # Get function arguments.
        debug = args.debug

        for record in tqdm(dataset, disable=not debug):
            record.title = re_pattern.sub('', record.title)
            record.article = re_pattern.sub('', record.article)
        return dataset

    return func


def delimiter_filter_factory(
    left_delimiter: str,
    right_delimiter: str,
    replace_str: str = '',
    drop_delimiter: bool = True,
) -> Callable:
    r"""生成過濾 delimiter 之間字元的 filter function.
    """

    def func(
        dataset: List[news.parse.db.schema.ParsedNews],
        args: argparse.Namespace,
    ) -> List[news.parse.db.schema.ParsedNews]:
        # Get function arguments.
        debug = args.debug
        for record in tqdm(dataset, disable=not debug):
            record.title = find_delimiter(
                article=record.title,
                left_delimiter=left_delimiter,
                right_delimiter=right_delimiter,
                replace_str=replace_str,
                drop_delimiter=drop_delimiter,
            )
            record.article = find_delimiter(
                article=record.article,
                left_delimiter=left_delimiter,
                right_delimiter=right_delimiter,
                replace_str=replace_str,
                drop_delimiter=drop_delimiter,
            )
        return dataset

    return func


# Remove url in articles.
url_filter = filter_factory(re_pattern=URL_PATTERN)

# Remove emoji in articles.
emoji_filter = filter_factory(re_pattern=EMOJI_PATTERN)

# Remove text other than Chinese and English.
# Remove too special punctuation and keep only punctuation below.
# `[.~<、,。《?>*-!》:」「+%/]`
non_CJK_filter = filter_factory(re_pattern=REMOVE_CHAR_PATTERN)

# Remove parentheses and words in parentheses.
parentheses_filter = delimiter_filter_factory(
    left_delimiter='(',
    right_delimiter=')',
)

# Remove brackets and words in brackets.
brackets_filter = delimiter_filter_factory(
    left_delimiter='[',
    right_delimiter=']',
)

# Remove lenticular brackets and words in lenticular brackets.
lenticular_brackets_filter = delimiter_filter_factory(
    left_delimiter='【',
    right_delimiter='】',
)

# Remove curly brackets and words in curly brackets.
curly_brackets_filter = delimiter_filter_factory(
    left_delimiter='{',
    right_delimiter='}',
)
