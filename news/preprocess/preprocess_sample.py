import copy
import json
import os
import re
import sqlite3
import unicodedata

from ckip_transformers import __version__
from ckip_transformers.nlp import CkipNerChunker
from dataset import Allcolumn
from tqdm import tqdm


def load_database(db_name):
    r"""
    Load database by database filename.
    Return a list of dictionary.
    The keys in dictionary is every column of database except `raw_xml`.
    """
    dataset = Allcolumn(db_name)
    dataset = [i for i in dataset]
    return dataset


def length_filter(dataset, min_bound, max_bound):
    r"""
    Remove articles that are too long or too short.
    """
    result = []
    for i in tqdm(dataset):
        if len(i['article']) > min_bound and len(i['article']) < max_bound:
            result.append(i)
    return result


def NFKC(dataset):
    r"""
    Use NFKC normalize `title` and `article`.
    """
    for i in tqdm(dataset):
        i['title'] = unicodedata.normalize('NFKC', i['title'])
        i['article'] = unicodedata.normalize('NFKC', i['article'])

    return dataset


def read_ner_result(NER_result_dir):
    r"""
    Load NER result.
    """
    print('Loading ner result...')
    filenames = os.listdir(NER_result_dir)
    title_NER_results = []
    article_NER_results = []
    for filename in tqdm(filenames):
        if 'title' in filename:
            temp = json.load(
                open(f'{NER_result_dir}/{filename}', 'r', encoding='utf8'))
            title_NER_results.extend(temp)
        if 'article' in filename:
            temp = json.load(
                open(f'{NER_result_dir}/{filename}', 'r', encoding='utf8'))
            article_NER_results.extend(temp)

    return title_NER_results, article_NER_results


def NER_dataset(dataset, save_dir):

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    ner_driver = CkipNerChunker(level=3, device=0)
    # NER title.
    index = 0
    while index < len(dataset):
        end = index + 20000
        if end > len(dataset):
            end = len(dataset)
        sentences = [[dic['id'], unicodedata.normalize(
            'NFKC', dic['title'])] for dic in dataset[index: end]]

        ner = ner_driver(list(zip(*sentences))[1], batch_size=8)

        ner_result = []
        for sentence, sentence_ner in zip(sentences, ner):
            ner_result.append(
                {
                    'id': sentence[0],
                    'title': sentence[1],
                    'NER_result': [{'word': enty.word, 'ner': enty.ner, 'idx': enty.idx} for enty in sentence_ner]
                }
            )
        json.dump(ner_result, open(
            f'{save_dir}/title-{index}.json', 'w', encoding='utf8'))
        index = end

    # NER article.
    index = 0
    while index < len(dataset):
        end = index + 20000
        if end > len(dataset):
            end = len(dataset)
        sentences = [[dic['id'], unicodedata.normalize(
            'NFKC', dic['article'])] for dic in dataset[index: end]]

        ner = ner_driver(list(zip(*sentences))[1], batch_size=8)

        ner_result = []
        for sentence, sentence_ner in zip(sentences, ner):
            ner_result.append(
                {
                    'id': sentence[0],
                    'article': sentence[1],
                    'NER_result': [{'word': enty.word, 'ner': enty.ner, 'idx': enty.idx} for enty in sentence_ner]
                }
            )
        json.dump(ner_result, open(
            f'{save_dir}/article-{index}.json', 'w', encoding='utf8'))
        index = end


def ner_tag_subs(dataset, tag_dict, NER_result):
    r"""
    Replace the names of people, places, and organizations based on NER results.

    `tag_dict` 用來指定需要用tag替換的NER entity以及tag的名稱，範例如下
    `tag_dict` = [
        {'type': ['ORG'], 'tag': 'org', 'NeedID': False},
        {'type': ['LOC', 'GPE'], 'tag': 'loc', 'NeedID': True}
    ]
    表示所有ORG的entity要被換為`<org>`這個tag，以及LOC和GPE都被換為`<loc1>`這種格式的tag(ID會根據名稱不同改變)
    """

    title_ner, article_ner = read_ner_result(NER_result_dir)
    for data in tqdm(dataset):
        index = data['id']
        a_ner = next(i for i in article_ner if i['id'] == index)['NER_result']
        t_ner = next(i for i in title_ner if i['id'] == index)['NER_result']
        tot_ner = copy.deepcopy(a_ner)
        tot_ner.extend(t_ner)

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
        ori_title = next(i for i in title_ner if i['id'] == index)['title']
        ori_article = next(i for i in article_ner if i['id'] == index)[
            'article']
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

        data['title'] = rp_title
        data['article'] = rp_article

    return dataset


def date_filter(dataset, NER_result_dir):
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
    title_ner, article_ner = read_ner_result(NER_result_dir)
    for data in tqdm(dataset):
        index = data['id']
        ner_result = next(i for i in article_ner if i['id'] == index)[
            'NER_result']
        ner_result.extend(
            next(i for i in title_ner if i['id'] == index)['NER_result'])

        rp_title = data['title']
        rp_article = data['article']
        for word in ner_result:
            if word['ner'] == 'DATE':
                sub = date_preprocess(word['word'])
                if sub:
                    rp_article = rp_article.replace(word['word'], sub)
                    rp_title = rp_title.replace(word['word'], sub)
        data['title'] = rp_title
        data['article'] = rp_article

    return dataset


def url_filter(dataset):
    r"""
    Remove urls in title or article.
    """
    reg = re.compile(r'https?://[a-zA-Z0-9/\?\=\-\.]+')
    for i in tqdm(dataset):
        i['title'] = reg.sub('', i['title'])
        i['article'] = reg.sub('', i['article'])
    return dataset


def whitespace_filter(dataset):
    r"""
    Use single space to replace continuously space.
    """
    reg = re.compile(r'\s+')
    for i in tqdm(dataset):
        i['title'] = reg.sub(' ', i['title'])
        i['article'] = reg.sub(' ', i['article'])
    return dataset


def parentheses_filter(dataset):
    r"""
    Remove various brackets and words in brackets
    """
    reg = re.compile(r'.([^(]*\)|[^（]*）|[^[]*\]|[^［]*］|[^【]*】)')
    for i in tqdm(dataset):
        i['title'] = reg.sub('', i['title'])
        i['article'] = reg.sub('', i['article'])
    return dataset


def number_filter(dataset):
    r"""
    Replace Arabic numerals with `<num>`
    """
    reg = re.compile(r'\d+(?![^<]*>)')
    for i in tqdm(dataset):
        i['title'] = reg.sub('<num>', i['title'])
        i['article'] = reg.sub('<num>', i['article'])
    return dataset


def guillemet_filter(dataset):
    r"""
    Replace guillemet with `<unk>`
    """
    reg = re.compile('《(.*?)》')
    for i in tqdm(dataset):
        i['title'] = reg.sub('<unk>', i['title'])
        i['article'] = reg.sub('<unk>', i['article'])
    return dataset


def language_filter(dataset):
    r"""
    Replace Japanese or Korean with `<unk>` and english with `<en>`
    """
    def lang_replace(context):
        index = 0
        last_type = None
        while index < len(context):
            if context[index] == '<':
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
            if char_type == 'SPACE' and last_type != None:
                context = ''.join([context[:index], context[index+1:]])
                index -= 1
            if char_type == 'DIGIT' and last_type != None:
                context = ''.join([context[:index], context[index+1:]])
                index -= 1
            if char_type == 'CJK':
                last_type = None
            index += 1
        return context

    for i in tqdm(dataset):
        i['title'] = lang_replace(i['title'])
        i['article'] = lang_replace(i['article'])
    return dataset


def save_in_db(db_name, data):
    def create_table(db_name):
        # If `db_name` not exist then create db file.
        if not os.path.exists(db_name):
            open(db_name, 'w').close()

        instruct = u"""CREATE TABLE IF NOT EXISTS news_table (
            id integer PRIMARY KEY,
            url text,
            time text,
            company text,
            label text,
            reporter text,
            title text,
            article text,
            raw_xml text
        ); """
        conn_db = sqlite3.connect(db_name)
        c = conn_db.cursor()
        c.execute(instruct)
        conn_db.commit()
        conn_db.close()

    def write_in_db(data, db_name):
        conn_db = sqlite3.connect(db_name)
        c = conn_db.cursor()
        # db_url = list(c.execute('SELECT url from news_table'))
        # db_url = list(map(lambda x: x[0], db_url))

        # preprocessed_data = [tuple(i.values())
        #                      for i in data if i['url'] not in db_url]
        data = [list(i.values()) for i in data]
        for i in data:
            i.append(None)
        c.executemany(
            'INSERT INTO news_table(id, url, time, company, label, reporter, title, article, raw_xml) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', tuple(data))
        conn_db.commit()
        conn_db.close()
    create_table(db_name)
    write_in_db(data, db_name)


def deEmojify(text):
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


def emoji_filter(dataset):
    r"""
    Remove emoji of all text in dataset.
    """
    for data in tqdm(dataset):
        data['title'] = deEmojify(data['title'])
        data['article'] = deEmojify(data['article'])
    return dataset


def not_CJK_filter(dataset):
    r"""
    Remove text other than Chinese and English.
    Remove too special punctuation and keep only punctuation below.
    `[，、。?,.!~「」><《》+-/:：＋－＊／！]`
    """
    for data in tqdm(dataset):
        rp_title = ""
        rp_article = ""
        for i in data['title']:
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
        for i in data['article']:
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
        data['title'] = rp_title
        data['article'] = rp_article
    return dataset


def get_id_data(id_list, dataset):
    r"""
    Get `id_list` specified data from dataset.
    """
    return [i for i in dataset if i['id'] in id_list]


def merge_db(input_db, save_db):
    r"""
    Put `input_db` in `save_db`.
    """
    def write_in_db(data, db_name):
        conn_db = sqlite3.connect(db_name)
        c = conn_db.cursor()
        db_url = list(c.execute('SELECT url from news_table'))
        db_url = list(map(lambda x: x[0], db_url))

        preprocessed_data = [tuple(i.values())
                             for i in data if i['url'] not in db_url]
        data = [list(i.values())[1:] for i in data]
        for i in data:
            i.append(None)
        c.executemany(
            'INSERT INTO news_table(url, time, company, label, reporter, title, article, raw_xml) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', tuple(data))
        conn_db.commit()
        conn_db.close()

    print('Loading `input_db` ...')
    dataset = load_database(input_db)

    print('Merging two db ...')
    write_in_db(dataset, save_db)

    # Load merged database as return value.
    print('Loading return value ...')
    dataset = load_database(save_db)

    return dataset


def base_preprocess(db_name, save_db_name):
    # Not replace word to tag.
    dataset = load_database(db_name)
    dataset = NFKC(dataset)
    dataset = url_filter(dataset)
    dataset = whitespace_filter(dataset)
    dataset = length_filter(dataset, 200, 1000)
    dataset = parentheses_filter(dataset)
    dataset = emoji_filter(dataset)
    dataset = not_CJK_filter(dataset)
    dataset = length_filter(dataset, 200, 1000)
    save_in_db(save_db_name, dataset)


def main():
    dataset = load_database('temp_v2.3.db')

    # Not replace word to tag.
    # dataset = NFKC(dataset)
    # dataset = url_filter(dataset)
    # dataset = whitespace_filter(dataset)
    # dataset = length_filter(dataset, min_bound=200, max_bound=1000)
    # dataset = parentheses_filter(dataset)
    # dataset = emoji_filter(dataset)
    # dataset = not_CJK_filter(dataset)
    # dataset = length_filter(dataset, min_bound=200, max_bound=1000)

    # NER dataset and save result.
    # NER_dataset(dataset, 'temp_v2.3')

    # Replace tag preprocess.
    tag_dict = [
        {'type': ['ORG'], 'tag': 'org', 'NeedID': True},
        {'type': ['LOC'], 'tag': 'loc', 'NeedID': True},
        {'type': ['PERSON'], 'tag': 'per', 'NeedID': True},
        {'type': ['FAC'], 'tag': 'fac', 'NeedID': True}
    ]
    dataset = ner_tag_subs(
        dataset,
        tag_dict=tag_dict,
        NER_result_dir='v2.3result'
    )
    dataset = date_filter(dataset, NER_result_dir='v2.3result')
    dataset = language_filter(dataset)
    dataset = guillemet_filter(dataset)
    dataset = number_filter(dataset)
    save_in_db(db_name='news_FAC_v2.4.2.db', data=dataset)


if __name__ == '__main__':
    main()
