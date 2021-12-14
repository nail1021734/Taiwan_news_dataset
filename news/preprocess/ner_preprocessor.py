import argparse
import gc
import re
from typing import Dict, List

import torch
from ckip_transformers.nlp import CkipNerChunker
from tqdm import tqdm

import news.parse.db.read
import news.parse.db.schema
import news.parse.util.normalize

NER_CLASSES = [
    'GPE',
    'PERSON',
    'ORG',
    'NORP',
    'LOC',
    'FAC',
    'PRODUCT',
    'WORK_OF_ART',
    'EVENT',
    'LAW',
]


def ner_dataset(
    dataset: List[news.parse.db.schema.ParsedNews],
    device: int = 0,
    batch_size: int = 8,
) -> List[Dict]:
    r"""對資料集做 NER 分析取出 entity 並回傳分析結果.
    """
    # Initial NER model.
    ner_model = CkipNerChunker(level=3, device=device)
    # Get id, article and title.
    title_list = []
    article_list = []
    for record in dataset:
        title_list.append(record.title)
        article_list.append(record.article)

    # NER titles.
    title_ner_list = ner_model(
        title_list,
        batch_size=batch_size,
        show_progress=False,
    )
    # NER article.
    article_ner_list = ner_model(
        article_list,
        batch_size=batch_size,
        show_progress=False,
    )

    ner_result = []
    for title_ner, article_ner in zip(
            title_ner_list,
            article_ner_list,
    ):
        ner_result.append(
            {
                'title_NER': title_ner,
                'article_NER': article_ner,
            }
        )

    del ner_model
    torch.cuda.empty_cache()
    gc.collect()
    return ner_result


def _ner_tag_subs(
    dataset: List[news.parse.db.schema.ParsedNews],
    tag_option: List[Dict],
    use_date_replacer: bool,
    debug: bool = False,
    device: int = 0,
    batch_size: int = 8,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""Replace the names of people, places, and organizations based on NER
    results.

    Parameters
    ==========
    `dataset`: List[news.parse.db.schema.ParsedNews]
        要處理的資料集.
    `tag_option`: List[Dict]
        用來指定需要用 tag 替換的 NER entity 以及 tag 的名稱，範例如下
        `tag_option` = [
            {'ner_classes': ['ORG'], 'tag': 'org', 'need_id': False},
            {'ner_classes': ['LOC', 'GPE'], 'tag': 'loc', 'need_id': True}
        ]
        表示所有 ORG 的 entity 要被換為 `<org>` 這個 tag ，
        以及 LOC 和 GPE 都被換為 `<loc1>` 這種格式的 tag.( ID 會根據名稱不同改變.)
    `use_date_replacer`: bool
        用來指定要不要將日期中的數字替換成 `<num>`.
    """

    # 取得 NER 分析結果
    ner_result = ner_dataset(
        dataset=dataset,
        device=device,
        batch_size=batch_size,
    )
    for ner_data, record in tqdm(zip(ner_result, dataset), disable=not debug):
        # 得到 article 的 ner 結果.
        article_ner = ner_data['article_NER']
        # 得到 title 的 ner 結果.
        title_ner = ner_data['title_NER']
        # 將兩個 NER 結果合併成同一個表.
        total_ner = article_ner + title_ner

        # Build type table.
        # 建立一個 key 為 NER 類別名稱(例如:org, per) value 為一個紀錄此 NER 類別
        # 的資訊的字典(`id` 紀錄此 NER 類別對應到 `tag_option` 的哪個元素, `need_id`: 紀錄
        # 需不需要給每個不同的 token 一個獨立的id, `tag`: 紀錄此 NER 類別需被替換成的 tag
        # ), 建立這個表方便我們後續可以直接用 NER 類別名稱得到 value 中的資訊.
        type_table = dict(
            (
                k, {
                    'id': idx,
                    'need_id': tag_option[idx]['need_id'],
                    'tag': tag_option[idx]['tag']
                }
            )
            for idx in range(len(tag_option))
            for k in tag_option[idx]['ner_classes']
        )

        # Build word to tag table.
        # 建立一個表紀錄每個被 NER 標記出來的 token 對應到的 tag.
        # 建立這個表方便我們直接使用 token 查詢對應的 tag.
        word2tag_dict = [{} for i in range(len(tag_option))]
        for ner_token in total_ner:
            if ner_token.ner in type_table:
                if ner_token.word not in word2tag_dict[type_table[ner_token.ner]
                                                       ['id']]:
                    if type_table[ner_token.ner]['need_id']:
                        tag_id = len(
                            word2tag_dict[type_table[ner_token.ner]['id']]
                        )
                        tag_str = type_table[ner_token.ner]['tag']
                        word2tag_dict[type_table[ner_token.ner]['id']][
                            ner_token.word] = f'<{tag_str}{tag_id}>'
                    else:
                        tag_str = type_table[ner_token.ner]['tag']
                        word2tag_dict[type_table[ner_token.ner]['id']][
                            ner_token.word] = f'<{tag_str}>'

        # Get origin title and article.
        ori_title = record.title
        ori_article = record.article
        rp_title = ''
        rp_article = ''

        # Substitute title.
        last_len = 0
        for ner_token in title_ner:
            if ner_token.ner in type_table:
                rp_title = (
                    rp_title + ori_title[last_len:ner_token.idx[0]]
                    + word2tag_dict[type_table[ner_token.ner]['id']][
                        ner_token.word]
                )
                last_len = ner_token.idx[1]
        rp_title = rp_title + ori_title[last_len:]

        # Substitute article.
        last_len = 0
        for ner_token in article_ner:
            if ner_token.ner in type_table:
                rp_article = (
                    rp_article + ori_article[last_len:ner_token.idx[0]]
                    + word2tag_dict[type_table[ner_token.ner]['id']][
                        ner_token.word]
                )
                last_len = ner_token.idx[1]
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
        if re.match('.*?年.*?月.*?日', date):
            return r'<num>年<num>月<num>日'
        elif re.match('.*?月.*?日', date):
            return r'<num>月<num>日'
        else:
            return False

    for ner_data, record in tqdm(zip(ner_result, dataset), disable=not debug):
        data_ner_result = ner_data['article_NER'] + ner_data['title_NER']

        rp_title = record.title
        rp_article = record.article
        for ner_token in data_ner_result:
            if ner_token.ner == 'DATE':
                sub = date_preprocess(ner_token.word)
                if sub:
                    rp_article = rp_article.replace(ner_token.word, sub)
                    rp_title = rp_title.replace(ner_token.word, sub)
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
    batch_size = args.ner_batch_size
    debug = args.debug
    device = args.device
    use_date_replacer = args.use_date_replacer
    tag_option = args.tag_option

    dataset = _ner_tag_subs(
        dataset=dataset,
        tag_option=tag_option,
        use_date_replacer=use_date_replacer,
        device=device,
        batch_size=batch_size,
        debug=debug,
    )
    return dataset