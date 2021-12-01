import unicodedata
from tqdm import tqdm
import news.parse.db.schema
import news.parse.db.read
from typing import List, Dict
import re
from ckip_transformers.nlp import CkipNerChunker
import copy
import inspect


def NFKC(
    dataset: List[news.parse.db.schema.ParsedNews],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Use NFKC normalize `title`, `article`, `category` and `reporter`.
    """
    for i in tqdm(dataset, desc='NFKC', disable=not debug):
        i.title = unicodedata.normalize('NFKC', i.title)
        i.article = unicodedata.normalize('NFKC', i.article)

        # Check if `i.category` is None.
        if i.category:
            # If `i.category` is not None than do NFKC normalize.
            i.category = unicodedata.normalize('NFKC', i.category)

        # Check if `i.reporter` is None.
        if i.reporter:
            # If `i.reporter` is not None then do NFKC normalize.
            i.reporter = unicodedata.normalize('NFKC', i.reporter)

    return dataset


def length_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    min_length: int = 200,
    max_length: int = 1000,
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove articles that are too long or too short.
    """
    result = []
    for i in tqdm(dataset, desc='length_filter', disable=not debug):
        if max_length > len(i.article) > min_length:
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
    r"""Remove various brackets and words in brackets.
    """
    parentheses_pattern = re.compile(r'.([^(]*\)|[^[]*\]|[^【]*】)')
    for i in tqdm(dataset, desc='Parentheses_filter', disable=not debug):
        i.title = parentheses_pattern.sub('', i.title)
        i.article = parentheses_pattern.sub('', i.article)
    return dataset


def number_filter(
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


def guillemet_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Replace guillemet with `<unk>`.
    Example: 《香港國安法》->《<unk>》
    """
    guillemet_pattern = re.compile('(?<=《)(.*?)(?=》)')
    for i in tqdm(dataset, desc='Guillemet_filter', disable=not debug):
        i.title = guillemet_pattern.sub('<unk>', i.title)
        i.article = guillemet_pattern.sub('<unk>', i.article)
    return dataset


def deEmojify(text: str):
    r"""Remove emoji in one text.
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
    return emoji_pattern.sub('', text)


def emoji_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    debug: bool = False,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Remove emoji of all text in dataset.
    """
    for data in tqdm(dataset, desc='Emoji_filter', disable=not debug):
        data.title = deEmojify(data.title)
        data.article = deEmojify(data.article)
    return dataset


def not_CJK_filter(
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
    for i in tqdm(dataset, desc='Not_CJK_filter', disable=not debug):
        i.title = remove_char_pattern.sub('', i.title)
        i.article = remove_char_pattern.sub('', i.article)

    return dataset


def english_to_tag(
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


def NER_dataset(dataset: List[news.parse.db.schema.ParsedNews],) -> List[Dict]:
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


def ner_tag_subs(
    dataset: List[news.parse.db.schema.ParsedNews],
    tag_dict: List[Dict],
    filter_date: bool = True,
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
    `filter_date`: bool
        用來指定要不要將日期中的數字替換成 `<num>`.
    """

    # 取得 NER 分析結果
    NER_result = NER_dataset(dataset)
    for data in tqdm(dataset, desc='Ner_tag_subs', disable=not debug):
        index = data.idx

        # Find data that have same id.
        ner_data = next(i for i in NER_result if i['id'] == index)

        # 得到 article 的 NER 結果.
        a_ner = ner_data['article_NER']
        # 得到 title 的 NER 結果.
        t_ner = ner_data['title_NER']
        # 將兩個 NER 結果合併成同一個表.
        tot_ner = copy.deepcopy(a_ner) + copy.deepcopy(t_ner)

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

    # If `filter_date` is True then replace number in date with `<num>`.
    if filter_date:
        dataset = date_filter(dataset=dataset, NER_result=NER_result)

    return dataset


def date_filter(
    dataset: List[news.parse.db.schema.ParsedNews],
    NER_result: List[Dict],
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
        ner_data = next(i for i in NER_result if i['id'] == index)

        ner_result = ner_data['article_NER']
        ner_result.extend(ner_data['title_NER'])

        rp_title = data.title
        rp_article = data.article
        for word in ner_result:
            if word['ner'] == 'DATE':
                sub = date_preprocess(word['word'])
                if sub:
                    rp_article = rp_article.replace(word['word'], sub)
                    rp_title = rp_title.replace(word['word'], sub)
        data.title = rp_title
        data.article = rp_article

    return dataset


def ner_tag_subs_flag_version(
    dataset: List[news.parse.db.schema.ParsedNews],
    NER_flag: str,
    NER_NeedID_flag: str,
    filter_date: bool,
):
    r"""使用 flag 指定要將 NER 結果的哪些類別替換成 tag.

    Parameters
    ==========
    `dataset`: List[news.parse.db.schema.ParsedNews]
        要處理的資料集.
    `NER_flag`: str
        10個 bit 的 flag 依照 `tag_list` 的順序指定是否將此 NER 類別替換成 tag.
    `NER_NeedID_flag`: str
        指定每個要替換成 tag 的 NER 類別是否使用特定 ID 表示一樣的token.
    `filter_date`: bool
        是否將日期中的數字替換成 `<num>`.

    Example
    =======
    當 `NER_flag == 1010000000` 且 `NER_NeedID_flag == 1000000000`
    表示 GPE 類別以及 ORG 類別分別要換成 `<gpe1>` 和 `<org>` 兩種 token.
    (注意，gpe 的每個不同 token 會有各自的 ID.)
    """
    # 建立 `tag_list` 照順序分別代表 flag 中的每個 bit.
    tag_list = [
        {
            'tag_name': 'GPE',
            'sub_tag': 'gpe'
        },
        {
            'tag_name': 'PERSON',
            'sub_tag': 'per'
        },
        {
            'tag_name': 'ORG',
            'sub_tag': 'org'
        },
        {
            'tag_name': 'NORP',
            'sub_tag': 'nrp'
        },
        {
            'tag_name': 'LOC',
            'sub_tag': 'loc'
        },
        {
            'tag_name': 'FAC',
            'sub_tag': 'fac'
        },
        {
            'tag_name': 'PRODUCT',
            'sub_tag': 'prdt'
        },
        {
            'tag_name': 'WORK_OF_ART',
            'sub_tag': 'woa'
        },
        {
            'tag_name': 'EVENT',
            'sub_tag': 'evt'
        },
        {
            'tag_name': 'LAW',
            'sub_tag': 'law'
        },
    ]

    # 建立 `tag_dict`.
    tag_dict = []
    for tag_flag, ID_flag, tag_info in zip(NER_flag, NER_NeedID_flag, tag_list):
        if int(tag_flag):
            tag_dict.append(
                {
                    'type': [tag_info['tag_name']],
                    'tag': tag_info['sub_tag'],
                    'NeedID': bool(int(ID_flag)),
                }
            )

    # Run `ner_tag_subs`.
    dataset = ner_tag_subs(
        dataset=dataset,
        tag_dict=tag_dict,
        filter_date=filter_date,
    )
    return dataset


def preprocess_by_flag(
    function_flag: str,
    **kwargs,
):
    r"""根據 flag 決定哪些 preprocess function 要執行.

    Parameters
    ==========
    `flag`: str
        11個 bit 組成的字串,每個 bit 照順序各自代表 `preprocess_order` 內的每個
        function 若對應 bit 為1代表要執行,對應 bit 為0則不執行.
    """
    # Set preprocess order to ensure run preprocess in the correct sequence.
    preprocess_order = [
        NFKC,
        url_filter,
        whitespace_filter,
        parentheses_filter,
        emoji_filter,
        not_CJK_filter,
        length_filter,
        ner_tag_subs_flag_version,
        english_to_tag,
        guillemet_filter,
        number_filter,
    ]

    # Run preprocess in specified order.
    for flag_value, func in zip(function_flag, preprocess_order):
        # If `flag == 1` then run the preprocess function.
        if int(flag_value):
            # Get function parameters.
            func_parameter = dict(
                (p_name, kwargs[p_name])
                for p_name in inspect.signature(func).parameters
            )

        # Run preprocess function.
        dataset = func(**func_parameter)
    return dataset
