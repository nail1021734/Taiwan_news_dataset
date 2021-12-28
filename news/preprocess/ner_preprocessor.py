import argparse
import gc
import re
from typing import Dict, List, Tuple

import torch
from ckip_transformers.nlp import CkipNerChunker
from ckip_transformers.nlp.util import NerToken
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


def ner_arg_post_process(args: argparse.Namespace,) -> Dict:
    args = args.__dict__

    need_id_validation = {}
    ner_tag_lookup_table = {}
    for ner_class in NER_CLASSES:
        ner_tag = args[f'use_{ner_class}'] or args[f'use_{ner_class}_with_id']
        need_id = bool(args[f'use_{ner_class}_with_id'])

        # 若 `args[f'use_{ner_class}']` 以及 `args[f'use_{ner_class}_with_id']`
        # 皆為 None 則直接跳過後續處理.
        if not ner_tag:
            continue

        # 檢查 `need_id` 是否有衝突(例如: 相同 tag 其中一類需要 id 另外一類不用).
        if (ner_tag in need_id_validation
                and need_id_validation[ner_tag] != need_id):
            raise ValueError(f'<{ner_tag}> tag id conflict.')

        need_id_validation[ner_tag] = need_id

        ner_tag_lookup_table[ner_class] = {
            'ner_tag': ner_tag,
            'need_id': need_id,
        }

    return ner_tag_lookup_table


def ner_dataset(
    dataset: List[news.parse.db.schema.ParsedNews],
    device: int = 0,
    batch_size: int = 8,
) -> Tuple[List[NerToken], List[NerToken]]:
    r"""對資料集 title 與 article 做 NER 分析取出 entity 並回傳分析結果.
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
    title_ner_tokens_list = ner_model(
        title_list,
        batch_size=batch_size,
        show_progress=False,
    )
    # NER article.
    article_ner_tokens_list = ner_model(
        article_list,
        batch_size=batch_size,
        show_progress=False,
    )

    del ner_model
    torch.cuda.empty_cache()
    gc.collect()
    return title_ner_tokens_list, article_ner_tokens_list


def ner_tags_sub(
    dataset: List[news.parse.db.schema.ParsedNews],
    ner_tag_lookup_table: Dict,
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
    `ner_tag_lookup_table`: Dict
        用來指定需要用 tag 替換的 NER entity 以及 tag 的名稱，範例如下
        ```
        ner_tag_lookup_table = {
            'ORG': {
                'ner_tag': 'org',
                'need_id': False,
            },
            'LOC': {
                'ner_tag': 'loc',
                'need_id': True,
            },
            'GPE': {
                'ner_tag': 'loc',
                'need_id': True,
            },
        },
        ```
        表示所有 ORG 的 entity 要被換為 `<org>` 這個 tag ，
        以及 LOC 和 GPE 都被換為 `<loc1>` 這種格式的 tag.( ID 會根據名稱不同改變.)
    `use_date_replacer`: bool
        用來指定要不要將日期中的數字替換成 `<num>`.
    """

    def text_ner_sub(
        ori_text: str,
        text_ner_tokens: str,
        token_tag2str: Dict,
        ner_tag_counter: Dict,
    ):
        # Record all NER tags in text.
        text_ner_infos = []
        for ner_token in text_ner_tokens:
            if ner_token.ner not in ner_tag_lookup_table:
                continue

            _d = ner_tag_lookup_table[ner_token.ner]
            ner_tag = _d['ner_tag']
            need_id = _d['need_id']
            token = ner_token.word
            start_pos = ner_token.idx[0]
            end_pos = ner_token.idx[1]

            if (token, ner_tag) not in token_tag2str:
                if need_id:
                    tag_id = ner_tag_counter[ner_tag]
                    token_tag2str[token, ner_tag] = f'<{ner_tag}{tag_id}>'
                    ner_tag_counter[ner_tag] += 1
                else:
                    token_tag2str[token, ner_tag] = f'<{ner_tag}>'

            text_ner_infos.append(
                {
                    'replace_tag': token_tag2str[token, ner_tag],
                    'start_pos': start_pos,
                    'end_pos': end_pos,
                }
            )

        # Replace all NER tags in text.
        replace_idx = 0
        new_text = ''
        for text_ner_info in sorted(
                text_ner_infos,
                key=lambda info: info['start_pos'],
        ):
            new_text += ori_text[replace_idx:text_ner_info['start_pos']]
            new_text += text_ner_info['replace_tag']
            replace_idx = text_ner_info['end_pos']
        new_text += ori_text[replace_idx:]

        return new_text

    # 取得 NER 分析結果
    title_ner_tokens_list, article_ner_tokens_list = ner_dataset(
        dataset=dataset,
        device=device,
        batch_size=batch_size,
    )
    # Replace NER result with custom NER tags.
    for title_ner_tokens, article_ner_tokens, record in tqdm(
            zip(
                title_ner_tokens_list,
                article_ner_tokens_list,
                dataset,
            ),
            disable=not debug,
    ):
        # Title and article share same NER tag table.
        token_tag2str = {}
        ner_tag_counter = {
            _d['ner_tag']: 0
            for _d in ner_tag_lookup_table.values()
        }

        record.title = text_ner_sub(
            ori_text=record.title,
            text_ner_tokens=title_ner_tokens,
            token_tag2str=token_tag2str,
            ner_tag_counter=ner_tag_counter,
        )
        record.article = text_ner_sub(
            ori_text=record.article,
            text_ner_tokens=article_ner_tokens,
            token_tag2str=token_tag2str,
            ner_tag_counter=ner_tag_counter,
        )
    # If `use_date_replacer` is true then replace number in date with `<num>`.
    if use_date_replacer:
        dataset = date_replacer(
            dataset=dataset,
            title_ner_tokens_list=title_ner_tokens_list,
            article_ner_tokens_list=article_ner_tokens_list,
            debug=debug,
        )

    return dataset


def date_replacer(
    dataset: List[news.parse.db.schema.ParsedNews],
    article_ner_tokens_list: List[NerToken],
    title_ner_tokens_list: List[NerToken],
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

    for title_ner_tokens, article_ner_tokens, record in tqdm(
            zip(
                title_ner_tokens_list,
                article_ner_tokens_list,
                dataset,
            ),
            disable=not debug,
    ):
        data_ner_result = title_ner_tokens + article_ner_tokens

        new_title = record.title
        new_article = record.article
        for ner_token in data_ner_result:
            if ner_token.ner == 'DATE':
                sub = date_preprocess(ner_token.word)
                if sub:
                    new_title = new_title.replace(ner_token.word, sub)
                    new_article = new_article.replace(ner_token.word, sub)
        record.title = new_title
        record.article = new_article

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
    ner_tag_lookup_table = args.ner_tag_lookup_table
    debug = args.debug
    device = args.device
    use_date_replacer = args.use_date_replacer

    return ner_tags_sub(
        batch_size=batch_size,
        ner_tag_lookup_table=ner_tag_lookup_table,
        dataset=dataset,
        debug=debug,
        device=device,
        use_date_replacer=use_date_replacer,
    )
