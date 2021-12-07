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


def ner_dataset(dataset: List[news.parse.db.schema.ParsedNews],) -> List[Dict]:
    r"""對資料集做 NER 分析取出 entity 並回傳分析結果.
    """
    # Initial NER model.
    ner_driver = CkipNerChunker(level=3, device=0)
    # Get id, article and title.
    data = [[i.idx, i.title, i.article] for i in dataset]
    # NER titles.
    titles_ner = ner_driver(
        list(zip(*data))[1],
        batch_size=8,
        show_progress=False,
    )
    # NER article.
    articles_ner = ner_driver(
        list(zip(*data))[2],
        batch_size=8,
        show_progress=False,
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
