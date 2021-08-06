import copy
import pickle
import re
import unicodedata
from typing import List

from ckip_transformers.nlp import CkipNerChunker
from tqdm import tqdm

import news.parse.db.schema
import news.preprocess.db


def NFKC(dataset: news.parse.db.schema.ParsedNews):
    r"""
    Use NFKC normalize `title` and `article`.
    """
    for i in tqdm(dataset):
        i.title = unicodedata.normalize('NFKC', i.title)
        i.article = unicodedata.normalize('NFKC', i.article)

    return dataset


def length_filter(
    dataset: news.parse.db.schema.ParsedNews,
    min_length: int,
    max_length: int
):
    r"""
    Remove articles that are too long or too short.
    """
    result = []
    for i in tqdm(dataset):
        if len(i.article) > min_length and len(i.article) < max_length:
            result.append(i)
    return result


def url_filter(dataset: news.parse.db.schema.ParsedNews):
    r"""
    Remove urls in title or article.
    """
    reg = re.compile(r'https?://[a-zA-Z0-9/\?\=\-\.]+')
    for i in tqdm(dataset):
        i.title = reg.sub('', i.title)
        i.article = reg.sub('', i.article)
    return dataset


def whitespace_filter(dataset: news.parse.db.schema.ParsedNews):
    r"""
    Use single space to replace continuously space.
    """
    reg = re.compile(r'\s+')
    for i in tqdm(dataset):
        i.title = reg.sub(' ', i.title)
        i.article = reg.sub(' ', i.article)
    return dataset


def parentheses_filter(dataset: news.parse.db.schema.ParsedNews):
    r"""
    Remove various brackets and words in brackets
    """
    reg = re.compile(r'.([^(]*\)|[^（]*）|[^[]*\]|[^［]*］|[^【]*】)')
    for i in tqdm(dataset):
        i.title = reg.sub('', i.title)
        i.article = reg.sub('', i.article)
    return dataset


def number_filter(dataset: news.parse.db.schema.ParsedNews):
    r"""
    Replace Arabic numerals with `<num>`
    """
    reg = re.compile(r'\d+(?![^<]*>)')
    for i in tqdm(dataset):
        i.title = reg.sub('<num>', i.title)
        i.article = reg.sub('<num>', i.article)
    return dataset


def guillemet_filter(dataset: news.parse.db.schema.ParsedNews):
    r"""
    Replace guillemet with `<unk>`
    """
    reg = re.compile('《(.*?)》')
    for i in tqdm(dataset):
        i.title = reg.sub('<unk>', i.title)
        i.article = reg.sub('<unk>', i.article)
    return dataset


def language_filter(dataset: news.parse.db.schema.ParsedNews):
    r"""
    Replace Japanese or Korean with `<unk>` and english with `<en>`.
    """
    def lang_replace(context: str):
        index = 0
        last_type = None
        while index < len(context):
            if context[index] == '<':
                if all(
                    (
                        context[index+1: index+4] == 'org',
                        context[index+1: index+4] == 'per',
                        context[index+1: index+4] == 'loc',
                        context[index+1: index+4] == 'num',
                        context[index+1: index+4] == 'unk',
                        context[index+1: index+4] == 'fac',
                    )
                ):
                    index = context.find('>', index) + 1
                    continue
            try:
                char_type = unicodedata.name(context[index]).split(' ')[0]
            except Exception as err:
                index += 1
                continue
            if char_type == 'LATIN':
                if last_type == 'LATIN':
                    context = ''.join([context[:index], context[index+1:]])
                    index -= 1
                else:
                    context = ''.join(
                        [context[:index], '<en>', context[index+1:]])
                    index += 3
                last_type = 'LATIN'
            if char_type == 'HANGUL':
                if last_type == 'HANGUL':
                    context = ''.join([context[:index], context[index+1:]])
                    index -= 1
                else:
                    context = ''.join(
                        [context[:index], '<unk>', context[index+1:]])
                    index += 4
                last_type = 'HANGUL'
            if char_type == 'KATAKANA' or char_type == 'HIRAGANA':
                if last_type == 'JAPAN':
                    context = ''.join([context[:index], context[index+1:]])
                    index -= 1
                else:
                    context = ''.join(
                        [context[:index], '<unk>', context[index+1:]])
                    index += 4
                last_type = 'JAPAN'
            if char_type == 'SPACE' and last_type is not None:
                context = ''.join([context[:index], context[index+1:]])
                index -= 1
            if char_type == 'DIGIT' and last_type is not None:
                context = ''.join([context[:index], context[index+1:]])
                index -= 1
            if char_type == 'CJK':
                last_type = None
            index += 1
        return context

    for i in tqdm(dataset):
        i.title = lang_replace(i.title)
        i.article = lang_replace(i.article)
    return dataset


def deEmojify(text: str):
    r"""
    Remove emoji in one text.
    """
    regrex_pattern = re.compile(
        pattern="["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+", flags=re.UNICODE
    )
    return regrex_pattern.sub(r'', text)


def emoji_filter(dataset: news.parse.db.schema.ParsedNews):
    r"""
    Remove emoji of all text in dataset.
    """
    for data in tqdm(dataset):
        data.title = deEmojify(data.title)
        data.article = deEmojify(data.article)
    return dataset


def not_CJK_filter(dataset: news.parse.db.schema.ParsedNews):
    r"""
    Remove text other than Chinese and English.
    Remove too special punctuation and keep only punctuation below.
    `[，、。?,.!~「」><《》+-/:：＋－＊／！]`
    """
    for data in tqdm(dataset):
        rp_title = ""
        rp_article = ""
        for i in data.title:
            if re.match(r'[\w\s]', i):
                try:
                    c_type = unicodedata.name(i).split(' ')[0]
                except Exception as err:
                    continue
                if c_type == 'LATIN' or c_type == 'CJK' or c_type == 'SPACE' or c_type == 'DIGIT':
                    rp_title += i
            else:
                if re.match(r'[，、。?,.!~「」><《》+-/:：＋－＊／！]', i):
                    rp_title += i
        for i in data.article:
            if re.match(r'[\w\s]', i):
                try:
                    c_type = unicodedata.name(i).split(' ')[0]
                except Exception as err:
                    continue
                if c_type == 'LATIN' or c_type == 'CJK' or c_type == 'SPACE' or c_type == 'DIGIT':
                    rp_article += i
            else:
                if re.match(r'[，、。?,.!~「」><《》+-/:：＋－＊／！]', i):
                    rp_article += i
        data.title = rp_title
        data.article = rp_article
    return dataset


def NER_dataset(
    dataset: news.parse.db.schema.ParsedNews,
):
    # Initial NER model.
    ner_driver = CkipNerChunker(level=3, device=0)

    # Get id, article and title.
    data = [[i.index, i.title, i.article] for i in dataset]

    # NER titles.
    titles_ner = ner_driver(list(zip(*data))[1], batch_size=8)

    # NER article.
    articles_ner = ner_driver(list(zip(*data))[2], batch_size=8)

    ner_result = []
    for d, title_ner, article_ner in zip(data, titles_ner, articles_ner):
        ner_result.append(
            {
                'id': d[0],
                'title': d[1],
                'article': d[2],
                'title_NER': [
                    {
                        'word': e.word,
                        'ner': e.ner,
                        'idx': e.idx
                    } for e in title_ner
                ],
                'article_NER': [
                    {
                        'word': e.word,
                        'ner': e.ner,
                        'idx': e.idx
                    } for e in article_ner
                ]
            }
        )

    return ner_result


def read_NER_result(result_path: str):
    NER_result = pickle.load(open(result_path, 'rb'))
    return NER_result


def ner_tag_subs(
    dataset: news.parse.db.schema.ParsedNews,
    tag_dict: List,
    result_path: str
):
    r"""
    Replace the names of people, places, and organizations based on NER results.

    `tag_dict` 用來指定需要用tag替換的NER entity以及tag的名稱，範例如下
    `tag_dict` = [
        {'type': ['ORG'], 'tag': 'org', 'NeedID': False},
        {'type': ['LOC', 'GPE'], 'tag': 'loc', 'NeedID': True}
    ]
    表示所有ORG的entity要被換為`<org>`這個tag，以及LOC和GPE都被換為`<loc1>`這種格式的tag(ID會根據名稱不同改變)
    """

    NER_result = read_NER_result(result_path)
    for data in tqdm(dataset):
        index = data.index

        # Find data that have same id.
        ner_data = next(i for i in NER_result if i['id'] == index)

        a_ner = ner_data['article_NER']
        t_ner = ner_data['title_NER']
        tot_ner = copy.deepcopy(a_ner)
        tot_ner.extend(copy.deepcopy(t_ner))

        # Build type table.
        type_table = dict((k, {'id': idx, 'NeedID': tag_dict[idx]['NeedID'], 'tag': tag_dict[idx]['tag']}) for idx in range(
            len(tag_dict)) for k in tag_dict[idx]['type'])

        # Build word2tag table.
        word2tag_dict = [{} for i in range(len(tag_dict))]
        for word in tot_ner:
            if word['ner'] in type_table.keys():
                if word['word'] not in word2tag_dict[type_table[word['ner']]['id']].keys():
                    if type_table[word['ner']]['NeedID']:
                        tag_id = len(
                            word2tag_dict[type_table[word['ner']]['id']])
                        tag_str = type_table[word['ner']]['tag']
                        word2tag_dict[type_table[word['ner']]['id']
                                      ][word['word']] = f'<{tag_str}{tag_id}>'
                    else:
                        tag_str = type_table[word['ner']]['tag']
                        word2tag_dict[type_table[word['ner']]['id']
                                      ][word['word']] = f'<{tag_str}>'

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
                tag_dic.items(), key=lambda x: len(x[0]), reverse=True)
            for k, v in tag_dic:
                rp_title = rp_title.replace(k, v)
                rp_article = rp_article.replace(k, v)

        data.title = rp_title
        data.article = rp_article

    return dataset


def date_filter(
    dataset: news.parse.db.schema.ParsedNews,
    result_path: str
):
    r"""
    Replace number in date tag with `<num>`.
    """
    def date_preprocess(date):
        if re.match('.*年.*月.*日', date):
            return r'<num>年<num>月<num>日'
        elif re.match('.*月.*日', date):
            return r'<num>月<num>日'
        else:
            return False
    NER_result = read_NER_result(result_path)
    for data in tqdm(dataset):
        index = data.index
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


def base_preprocess(
    dataset: news.parse.db.schema.ParsedNews,
    min_length: int,
    max_length: int,
):
    # Not replace word to tag.
    dataset = NFKC(dataset)
    dataset = url_filter(dataset)
    dataset = whitespace_filter(dataset)
    dataset = length_filter(dataset, min_length, max_length)
    dataset = parentheses_filter(dataset)
    dataset = emoji_filter(dataset)
    dataset = not_CJK_filter(dataset)
    dataset = language_filter(dataset)
    dataset = length_filter(dataset, min_length, max_length)
    return dataset
