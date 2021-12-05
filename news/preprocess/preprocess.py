import argparse
import re
from typing import Dict, List

from ckip_transformers.nlp import CkipNerChunker
from tqdm import tqdm

import news.parse.db.read
import news.parse.db.schema
import news.parse.util.normalize

TAG_TABLE = {
    'GPE': 'gpe',
    'PERSON': 'per',
    'ORG': 'org',
    'NORP': 'nrp',
    'LOC': 'loc',
    'FAC': 'fac',
    'PRODUCT': 'prod',
    'WORK_OF_ART': 'woa',
    'EVENT': 'evt',
    'LAW': 'law',
}

URL_PATTERN = re.compile(r'https?://[a-zA-Z0-9/\?\=\-\.]+')
NUMBER_PATTERN = re.compile(r'\d+(?![^<]*>)')
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
ENGLISH_PATTERN = re.compile(r'[a-zA-z][a-zA-z\s\d]+(?![^<]*>)')


def find_pair(
    article: str,
    left_char: str,
    right_char: str,
    replace_str: str = '',
    include: bool = True,
) -> str:
    r"""將 `article` 內 `left_char` 和 `right_char` 之間的字串替換為 `replace_str`.

    Parameters
    ==========
    `article`: str
        要處理的文章.
    `left_char`: str
        `left_char` 與 `right_char` 內的字串會被替換為 `replace_str`.
    `right_char`: str
        `left_char` 與 `right_char` 內的字串會被替換為 `replace_str`.
    `replace_str`: str
        選擇要替換的字串.
    `include`: bool
        若為 True 則會將 `left_char` 與 `right_char` 一起替換掉, 為 False 則會將
        `left_char` 與 `right_char` 保留下來.
    """
    # A stack to count `left_char` hit amount.
    count_stack = []

    # `rp_article` 為最後回傳的文章.
    rp_article = ''
    last_index = 0
    for i, char in enumerate(article):
        if char == left_char:
            if len(count_stack) == 0:
                # 若 `len(count_stack) == 0` 表示遇到開頭的 `left_char`.
                # 若不等於 0 表示先前已經遇過還沒匹配到 `right_char` 的 `left_char`.
                if include:
                    # 將 `left_char` 之前的文章片段加到 `rp_article` 之中.
                    rp_article += article[last_index:i]
                else:
                    # 將 `left_char` 之前的文章片段加到 `rp_article` 之中.
                    # 保留 `left_char`.
                    rp_article += article[last_index:i + 1]
            count_stack.append(i)

        if char == right_char:
            if len(count_stack) > 0:
                # 若 `len(count_stack) > 0` 則 pop 一個元素.
                count_stack.pop()
            else:
                # 若 `len(count_stack) == 0` 則直接跳過後續處理(表示沒有匹配的
                # `left_char` 丟棄此 `right_char`).
                continue
            if len(count_stack) == 0:
                # 若 pop 一個元素後 `len(count_stack) == 0` 表示此 `right_char`
                # 有匹配的 `left_char` 並且是最外層的 `left_char`.
                if include:
                    # 使用 `replace_str` 代替先前的文章片段.
                    rp_article += replace_str
                else:
                    # 使用 `replace_str` 代替先前的文章片段.
                    # 保留 `right_char`.
                    rp_article += replace_str + char
                # 更新 `last_index` 到 `right_char` 的下一個索引.
                last_index = i + 1
    # 將 `last_index` 之後的文章, 加到 `rp_article` 之後.
    rp_article += article[last_index:]
    return rp_article


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


def url_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    # Get function arguments.
    debug = args.debug

    for i in tqdm(dataset, desc='Url_filter', disable=not debug):
        i.title = URL_PATTERN.sub('', i.title)
        i.article = URL_PATTERN.sub('', i.article)
    return dataset


def parentheses_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove parentheses and words in parentheses.
    """
    # Get function arguments.
    debug = args.debug
    for record in tqdm(dataset, desc='Parentheses_filter', disable=not debug):
        record.title = find_pair(
            article=record.title, left_char='(', right_char=')'
        )
        record.article = find_pair(
            article=record.article, left_char='(', right_char=')'
        )
    return dataset


def brackets_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove brackets and words in brackets.
    """
    # Get function arguments.
    debug = args.debug

    for record in tqdm(dataset, desc='Brackets_filter', disable=not debug):
        record.title = find_pair(
            article=record.title, left_char='[', right_char=']'
        )
        record.article = find_pair(
            article=record.article, left_char='[', right_char=']'
        )
    return dataset


def lenticular_brackets_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove lenticular brackets and words in lenticular brackets.
    """
    # Get function arguments.
    debug = args.debug
    for record in tqdm(dataset, desc='Lenticular_brackets_filter',
                       disable=not debug):
        record.title = find_pair(
            article=record.title, left_char='【', right_char='】'
        )
        record.article = find_pair(
            article=record.article, left_char='【', right_char='】'
        )
    return dataset


def curly_brackets_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove curly brackets and words in curly brackets.
    """
    # Get function arguments.
    debug = args.debug
    for record in tqdm(dataset, desc='Curly_brackets_filter',
                       disable=not debug):
        record.title = find_pair(
            article=record.title, left_char='{', right_char='}'
        )
        record.article = find_pair(
            article=record.article, left_char='{', right_char='}'
        )
    return dataset


def number_replacer(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Replace Arabic numerals with `<num>`.
    """
    # Get function arguments.
    debug = args.debug

    for record in tqdm(dataset, desc='Number_filter', disable=not debug):
        record.title = NUMBER_PATTERN.sub('<num>', record.title)
        record.article = NUMBER_PATTERN.sub('<num>', record.article)
    return dataset


def guillemet_replacer(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Replace guillemet text with `<unk>`.
    Example: 《香港國安法》->《<unk>》
    """
    # Get function arguments.
    debug = args.debug

    for record in tqdm(dataset, desc='Guillemet_filter', disable=not debug):
        record.title = find_pair(
            article=record.title,
            left_char='《',
            right_char='》',
            replace_str='<unk>',
            include=False
        )
        record.article = find_pair(
            article=record.article,
            left_char='《',
            right_char='》',
            replace_str='<unk>',
            include=False
        )
    return dataset


def emoji_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove emoji in dataset.
    """
    # Get function arguments.
    debug = args.debug

    for record in tqdm(dataset, desc='Emoji_filter', disable=not debug):
        record.title = EMOJI_PATTERN.sub('', record.title)
        record.article = EMOJI_PATTERN.sub('', record.article)
    return dataset


def not_cjk_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove text other than Chinese and English.

    Remove too special punctuation and keep only punctuation below.
    `[.~<、,。《?>*-!》:」「+%/]`
    """
    # Get function arguments.
    debug = args.debug

    for record in tqdm(dataset, desc='Not_cjk_filter', disable=not debug):
        record.title = REMOVE_CHAR_PATTERN.sub('', record.title)
        record.article = REMOVE_CHAR_PATTERN.sub('', record.article)

    return dataset


def english_replacer(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Convert English to `<en>` tag.
    """
    # Get function arguments.
    debug = args.debug

    for record in tqdm(dataset, desc='English_to_tag', disable=not debug):
        record.title = ENGLISH_PATTERN.sub('<en>', record.title)
        record.article = ENGLISH_PATTERN.sub('<en>', record.article)
    return dataset


def ner_dataset(dataset: List[news.parse.db.schema.ParsedNews],) -> List[Dict]:
    r"""對資料集做 NER 分析取出 entity 並回傳分析結果.
    """
    # Initial NER model.
    ner_driver = CkipNerChunker(level=3, device=0)
    # Get id, article and title.
    data = [[i.idx, i.title, i.article] for i in dataset]
    # NER titles.
    titles_ner = ner_driver(
        list(zip(*data))[1], batch_size=8, show_progress=False
    )
    # NER article.
    articles_ner = ner_driver(
        list(zip(*data))[2], batch_size=8, show_progress=False
    )

    ner_result = []
    for d, title_ner, article_ner in zip(data, titles_ner, articles_ner):
        ner_result.append(
            {
                'idx':
                    d[0],
                'title_NER':
                    [
                        {
                            'word': e.word,
                            'ner': e.ner,
                            'idx': e.idx
                        } for e in title_ner
                    ],
                'article_NER':
                    [
                        {
                            'word': e.word,
                            'ner': e.ner,
                            'idx': e.idx
                        } for e in article_ner
                    ]
            }
        )
    return ner_result


def _ner_tag_subs(
    dataset: List[news.parse.db.schema.ParsedNews],
    tag_dict: List[Dict],
    use_date_replacer: bool,
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Replace the names of people, places, and organizations based on NER
    results.

    Parameters
    ==========
    `dataset`: List[news.parse.db.schema.ParsedNews]
        要處理的資料集.
    `tag_dict`: List[Dict]
        用來指定需要用 tag 替換的 NER entity 以及 tag 的名稱，範例如下
        `tag_dict` = [
            {'type': ['ORG'], 'tag': 'org', 'NeedID': False},
            {'type': ['LOC', 'GPE'], 'tag': 'loc', 'NeedID': True}
        ]
        表示所有 ORG 的 entity 要被換為 `<org>` 這個 tag ，
        以及 LOC 和 GPE 都被換為 `<loc1>` 這種格式的 tag.( ID 會根據名稱不同改變.)
    `use_date_replacer`: bool
        用來指定要不要將日期中的數字替換成 `<num>`.
    """

    # 取得 NER 分析結果
    ner_result = ner_dataset(dataset)
    for record in tqdm(dataset, desc='Ner_tag_subs', disable=not debug):
        # Find data that have same id.
        ner_data = ner_result[dataset.index(record)]

        # Make sure `ner_data` and `data` have same id.
        assert ner_data['idx'] == record.idx

        # 得到 article 的 ner 結果.
        a_ner = ner_data['article_NER']
        # 得到 title 的 ner 結果.
        t_ner = ner_data['title_NER']
        # 將兩個 NER 結果合併成同一個表.
        tot_ner = ner_data['article_NER'] + ner_data['title_NER']

        # Build type table.
        # 建立一個 key 為 NER 類別名稱(例如:org, per) value 為一個紀錄此 NER 類別
        # 的資訊的字典(`id` 紀錄此 NER 類別對應到 `tag_dict` 的哪個元素, `NeedID`: 紀錄
        # 需不需要給每個不同的 token 一個獨立的id, `tag`: 紀錄此 NER 類別需被替換成的 tag
        # ), 建立這個表方便我們後續可以直接用 NER 類別名稱得到 value 中的資訊.
        type_table = dict(
            (
                k, {
                    'id': idx,
                    'NeedID': tag_dict[idx]['NeedID'],
                    'tag': tag_dict[idx]['tag']
                }
            ) for idx in range(len(tag_dict)) for k in tag_dict[idx]['type']
        )

        # Build word to tag table.
        # 建立一個表紀錄每個被 NER 標記出來的 token 對應到的 tag.
        # 建立這個表方便我們直接使用 token 查詢對應的 tag.
        word2tag_dict = [{} for i in range(len(tag_dict))]
        for word in tot_ner:
            if word['ner'] in type_table.keys():
                if word['word'] not in word2tag_dict[type_table[word['ner']]
                                                     ['id']].keys():
                    if type_table[word['ner']]['NeedID']:
                        tag_id = len(
                            word2tag_dict[type_table[word['ner']]['id']]
                        )
                        tag_str = type_table[word['ner']]['tag']
                        word2tag_dict[type_table[word['ner']]['id']][
                            word['word']] = f'<{tag_str}{tag_id}>'
                    else:
                        tag_str = type_table[word['ner']]['tag']
                        word2tag_dict[type_table[word['ner']]['id']][
                            word['word']] = f'<{tag_str}>'

        # Get origin title and article.
        ori_title = record.title
        ori_article = record.article
        rp_title = ""
        rp_article = ""

        # Substitute title.
        last_len = 0
        for word in t_ner:
            if word['ner'] in type_table.keys():
                rp_title = rp_title + \
                    ori_title[last_len: word['idx'][0]] + \
                    word2tag_dict[type_table[word['ner']]['id']][word['word']]
                last_len = word['idx'][1]
        rp_title = rp_title + ori_title[last_len:]

        # Substitute article.
        last_len = 0
        for word in a_ner:
            if word['ner'] in type_table.keys():
                rp_article = rp_article + \
                    ori_article[last_len: word['idx'][0]] + \
                    word2tag_dict[type_table[word['ner']]['id']][word['word']]
                last_len = word['idx'][1]
        rp_article = rp_article + ori_article[last_len:]

        # Replace some words that NER didn’t catch index but in dictionary.
        for k, v in type_table.items():
            tag_dic = word2tag_dict[v['id']]
            tag_dic = sorted(
                tag_dic.items(), key=lambda x: len(x[0]), reverse=True
            )
            for k, v in tag_dic:
                rp_title = rp_title.replace(k, v)
                rp_article = rp_article.replace(k, v)

        record.title = rp_title
        record.article = rp_article

    # If `use_date_replacer` is true then replace number in date with `<num>`.
    if use_date_replacer:
        dataset = date_replacer(dataset=dataset, ner_result=ner_result)

    return dataset


def date_replacer(
    dataset: List[news.parse.db.schema.ParsedNews],
    ner_result: List[Dict],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Replace number in date tag with `<num>`.
    """

    def date_preprocess(date):
        if re.match('.*年.*月.*日', date):
            return r'<num>年<num>月<num>日'
        elif re.match('.*月.*日', date):
            return r'<num>月<num>日'
        else:
            return False

    for record in tqdm(dataset, desc='Date_filter', disable=not debug):
        # Find data that have same id.
        ner_data = ner_result[dataset.index(record)]

        # Make sure `ner_data` and `data` have same id.
        assert ner_data['idx'] == record.idx

        data_ner_result = ner_data['article_NER'] + ner_data['title_NER']

        rp_title = record.title
        rp_article = record.article
        for word in data_ner_result:
            if word['ner'] == 'DATE':
                sub = date_preprocess(word['word'])
                if sub:
                    rp_article = rp_article.replace(word['word'], sub)
                    rp_title = rp_title.replace(word['word'], sub)
        record.title = rp_title
        record.article = rp_article

    return dataset


def ner_entity_replacer(
    dataset: List[news.parse.db.schema.ParsedNews],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""使用 flag 指定要將 NER 結果的哪些類別替換成 tag.

    Parameters
    ==========
    `dataset`: List[news.parse.db.schema.ParsedNews]
        要處理的資料集.
    `ner_class`: str
        依照 `tag_list` 的表格指定是否將此 NER 類別替換成 tag.
    `ner_need_id_class`: str
        指定每個要替換成 tag 的 NER 類別是否使用特定 ID 表示一樣的token.
    `use_date_replacer`: bool
        是否將日期中的數字替換成 `<num>`.
    """
    # Get function arguments.
    ner_class = args.ner_class if 'ner_class' in args else None
    ner_need_id_class = args.ner_need_id_class
    use_date_replacer = args.use_date_replacer
    debug = args.debug

    # 建立 `tag_dict`.
    tag_dict = []
    if ner_class:
        # 如果有指定要替換成 tag 的 NER 類別則建立 `tag_dict`.
        for tag in ner_class:
            tag_dict.append(
                {
                    'type': [tag],
                    'tag': TAG_TABLE[tag],
                    'NeedID': tag in ner_need_id_class,
                }
            )

    dataset = _ner_tag_subs(
        dataset=dataset,
        tag_dict=tag_dict,
        use_date_replacer=use_date_replacer,
        debug=debug,
    )
    return dataset
