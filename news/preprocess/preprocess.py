import unicodedata
from tqdm import tqdm
import news.parse.db.schema
import news.parse.db.read
from typing import List, Dict
import re
from ckip_transformers.nlp import CkipNerChunker

TAG_TABLE = {
    'GPE': 'gpe',
    'PERSON': 'per',
    'ORG': 'org',
    'NORP': 'nrp',
    'LOC': 'loc',
    'FAC': 'fac',
    'PRODUCT': 'prdt',
    'WORK_OF_ART': 'woa',
    'EVENT': 'evt',
    'LAW': 'law',
}


def NFKC(
    dataset: List[news.parse.db.schema.ParsedNews],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Use NFKC normalize `title`, `article`, `category` and `reporter`.
    """
    for i in tqdm(dataset, desc='NFKC', disable=not debug):
        i.title = unicodedata.normalize('NFKC', i.title)
        i.article = unicodedata.normalize('NFKC', i.article)

        # Check whether `i.category` is None.
        if i.category:
            # If `i.category` is not None than do NFKC normalize.
            i.category = unicodedata.normalize('NFKC', i.category)

        # Check whether `i.reporter` is None.
        if i.reporter:
            # If `i.reporter` is not None then do NFKC normalize.
            i.reporter = unicodedata.normalize('NFKC', i.reporter)

    return dataset


def length_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    min_length: int,
    max_length: int,
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove articles that are too long or too short.
    """
    result = []
    for i in tqdm(dataset, desc='Length_filter', disable=not debug):
        if max_length:
            if max_length < len(i.article):
                continue
        if min_length:
            if min_length > len(i.article):
                continue
        result.append(i)

    return result


def url_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    url_pattern = re.compile(r'https?://[a-zA-Z0-9/\?\=\-\.]+')
    for i in tqdm(dataset, desc='Url_filter', disable=not debug):
        i.title = url_pattern.sub('', i.title)
        i.article = url_pattern.sub('', i.article)
    return dataset


def whitespace_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Use single space to replace continuously space.
    """
    for i in tqdm(dataset, desc='Whitespace_filter', disable=not debug):
        i.title = re.sub('\s+', ' ', i.title)
        i.article = re.sub('\s+', ' ', i.article)
    return dataset


def parentheses_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove parentheses and words in parentheses.
    """
    parentheses_pattern = re.compile(r'.([^(]*\))')
    for i in tqdm(dataset, desc='Parentheses_filter', disable=not debug):
        i.title = parentheses_pattern.sub('', i.title)
        i.article = parentheses_pattern.sub('', i.article)
    return dataset


def brackets_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove brackets and words in brackets.
    """
    parentheses_pattern = re.compile(r'.([^[]*\])')
    for i in tqdm(dataset, desc='Brackets_filter', disable=not debug):
        i.title = parentheses_pattern.sub('', i.title)
        i.article = parentheses_pattern.sub('', i.article)
    return dataset


def lenticular_brackets_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove lenticular brackets and words in lenticular brackets.
    """
    lenticular_brackets_pattern = re.compile(r'.([^【]*】)')
    for i in tqdm(dataset, desc='Lenticular_brackets_filter',
                  disable=not debug):
        i.title = lenticular_brackets_pattern.sub('', i.title)
        i.article = lenticular_brackets_pattern.sub('', i.article)
    return dataset


def curly_brackets_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove curly brackets and words in curly brackets.
    """
    curly_bracket_pattern = re.compile(r'.([^{]*\})')
    for i in tqdm(dataset, desc='Curly_brackets_filter', disable=not debug):
        i.title = curly_bracket_pattern.sub('', i.title)
        i.article = curly_bracket_pattern.sub('', i.article)
    return dataset


def number_replacer(
    dataset: List[news.parse.db.schema.ParsedNews],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Replace Arabic numerals with `<num>`.
    """
    number_pattern = re.compile(r'\d+(?![^<]*>)')
    for i in tqdm(dataset, desc='Number_filter', disable=not debug):
        i.title = number_pattern.sub('<num>', i.title)
        i.article = number_pattern.sub('<num>', i.article)
    return dataset


def guillemet_replacer(
    dataset: List[news.parse.db.schema.ParsedNews],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Replace guillemet text with `<unk>`.
    Example: 《香港國安法》->《<unk>》
    """
    guillemet_pattern = re.compile('(?<=《)(.*?)(?=》)')
    for i in tqdm(dataset, desc='Guillemet_filter', disable=not debug):
        i.title = guillemet_pattern.sub('<unk>', i.title)
        i.article = guillemet_pattern.sub('<unk>', i.article)
    return dataset


def emoji_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove emoji in dataset.
    """
    emoji_pattern = re.compile(
        pattern="["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE
    )
    for data in tqdm(dataset, desc='Emoji_filter', disable=not debug):
        data.title = emoji_pattern.sub('', data.title)
        data.article = emoji_pattern.sub('', data.article)
    return dataset


def not_cjk_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove text other than Chinese and English.

    Remove too special punctuation and keep only punctuation below.
    `[.~<、,。《?>*-!》:」「+%/]`
    """
    remove_char_pattern = re.compile(
        r'[^\u4e00-\u9fff.~<、,。《?>*\-!》:」「+%/a-zA-Z\d()\[\]【】]'
    )
    for i in tqdm(dataset, desc='Not_cjk_filter', disable=not debug):
        i.title = remove_char_pattern.sub('', i.title)
        i.article = remove_char_pattern.sub('', i.article)

    return dataset


def english_replacer(
    dataset: List[news.parse.db.schema.ParsedNews],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Convert English to `<en>` tag.
    """
    english_pattern = re.compile(r'[a-zA-z][a-zA-z\s\d]+(?![^<]*>)')
    for i in tqdm(dataset, desc='English_to_tag', disable=not debug):
        i.title = english_pattern.sub('<en>', i.title)
        i.article = english_pattern.sub('<en>', i.article)
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
                'id':
                    d[0],
                'title':
                    d[1],
                'article':
                    d[2],
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
    r"""Replace the names of people, places, and organizations based on NER results.

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
    for data in tqdm(dataset, desc='Ner_tag_subs', disable=not debug):
        index = data.idx

        # Find data that have same id.
        ner_data = next(i for i in ner_result if i['id'] == index)

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
        ori_title = ner_data['title']
        ori_article = ner_data['article']
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

        data.title = rp_title
        data.article = rp_article

    # If `use_date_replacer` is True then replace number in date with `<num>`.
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

    for data in tqdm(dataset, desc='Date_filter', disable=not debug):
        index = data.idx
        # Find data that have same id.
        ner_data = next(i for i in ner_result if i['id'] == index)

        data_ner_result = ner_data['article_NER'] + ner_data['title_NER']

        rp_title = data.title
        rp_article = data.article
        for word in data_ner_result:
            if word['ner'] == 'DATE':
                sub = date_preprocess(word['word'])
                if sub:
                    rp_article = rp_article.replace(word['word'], sub)
                    rp_title = rp_title.replace(word['word'], sub)
        data.title = rp_title
        data.article = rp_article

    return dataset


def ner_entity_replacer(
    dataset: List[news.parse.db.schema.ParsedNews],
    ner_class: List[str],
    ner_need_id_class: List[str],
    use_date_replacer: bool,
    debug: bool,
):
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
