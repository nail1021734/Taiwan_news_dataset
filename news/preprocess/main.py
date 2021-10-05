import argparse
import json
import os
import pickle

import news.parse.db
import news.preprocess.db
from news.parse.db.schema import ParsedNews
from news.preprocess.preprocess import *

PREPROCESS_FUNCTION = {
    'NFKC': NFKC,
    'length_filter': length_filter,
    'url_filter': url_filter,
    'whitespace_filter': whitespace_filter,
    'parentheses_filter': parentheses_filter,
    'number_filter': number_filter,
    'guillemet_filter': guillemet_filter,
    'language_filter': language_filter,
    'emoji_filter': emoji_filter,
    'not_CJK_filter': not_CJK_filter,
    'NER_dataset': NER_dataset,
    'ner_tag_subs': ner_tag_subs,
    'date_filter': date_filter,
    'base_preprocess': base_preprocess,
}


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--function',
        choices=PREPROCESS_FUNCTION.keys(),
        type=str,
        help='Select preprocess function.',
    )
    parser.add_argument(
        '--source',
        type=str,
        help='Specify database or dir to perform preprocess.',
    )
    parser.add_argument(
        '--save_path',
        type=str,
        help='Specify save path.',
    )
    parser.add_argument(
        '--min_length',
        type=int,
        default=None,
        help='Specify min article length when use length filter.',
    )
    parser.add_argument(
        '--max_length',
        type=int,
        default=None,
        help='Specify max article length when use length filter.',
    )
    parser.add_argument(
        '--NER_format',
        type=json.loads,
        default=None,
        help='Specify replace format when use `ner_tag_subs` method.'
    )
    parser.add_argument(
        '--NER_result',
        type=str,
        default=None,
        help='Specify NER_result path when use `ner_tag_subs` or `date_filter` method.'
    )

    args = parser.parse_args()
    return args


def preprocess(
    dataset: ParsedNews,
    args: argparse.Namespace,
):
    # 根據使用者選擇的function改變輸入的參數
    if args.function == 'length_filter' or args.function == 'base_preprocess':
        # 如果輸入的function包含`length_filter`，則需要輸入min_length和max_length
        result = PREPROCESS_FUNCTION[args.function](
            dataset=dataset,
            min_length=args.min_length,
            max_length=args.max_length
        )
    elif args.function == 'date_filter':
        # `date_filter`需要讀取NER的資訊，因此要判斷輸入的source是資料夾還是db檔
        if args.source.split('.')[-1] == 'db':
            # 若是db檔則直接讀取`args.NER_result`路徑，取得NER分析的結果
            result_file_path = os.path.join('data', args.NER_result)
            result = PREPROCESS_FUNCTION[args.function](
                dataset=dataset,
                result_path=result_file_path
            )
        else:
            # 若是資料夾則取出`args.NER_result`路徑下和`args.source`名稱相同的
            # NER分析結果
            result_file_name = args.filename.split('.')[0] + '.pickle'
            result_file_path = os.path.join(
                'data', args.NER_result, result_file_name)
            result = PREPROCESS_FUNCTION[args.function](
                dataset=dataset,
                result_path=result_file_path
            )
    elif args.function == 'ner_tag_subs':
        # `ner_tag_subs`需要讀取NER的資訊，因此要判斷輸入的source是資料夾還是db檔
        if args.source.split('.')[-1] == 'db':
            # 若是db檔則直接讀取`args.NER_result`路徑，取得NER分析的結果
            result_file_path = os.path.join('data', args.NER_result)
            result = PREPROCESS_FUNCTION[args.function](
                dataset=dataset,
                tag_dict=args.NER_format,
                result_path=result_file_path
            )
        else:
            # 若是資料夾則取出`args.NER_result`路徑下和`args.source`名稱相同的
            # NER分析結果
            result_file_name = args.filename.split('.')[0] + '.pickle'
            result_file_path = os.path.join(
                'data', args.NER_result, result_file_name)
            result = PREPROCESS_FUNCTION[args.function](
                dataset=dataset,
                tag_dict=args.NER_format,
                result_path=result_file_path
            )
    elif args.function == 'NER_dataset':
        NER_result = PREPROCESS_FUNCTION[args.function](
            dataset=dataset
        )
        if args.source.split('.')[-1] == 'db':
            # 如果輸入的`args.source`為db檔，則直接保存成名稱為`args.save_path`的
            # pickle檔
            target_path = os.path.join('data', args.save_path)
            pickle.dump(NER_result, open(target_path, 'wb'))
        else:
            # 如果輸入的`args.source`為資料夾，則將NER結果保存到資料夾中

            # 初始化目標資料夾路徑
            target_path = os.path.join('data', args.save_path)

            # 檢查目標資料夾是否存在，如果不存在則建立資料夾
            if not (os.path.exists(target_path)
                    or os.path.isfile(target_path)):
                os.makedirs(target_path)

            # 初始化保存的檔案名稱
            filename = args.filename.split('.')[0] + '.pickle'

            # 保存成pickle檔
            pickle.dump(
                NER_result,
                open(os.path.join(target_path, f'{filename}'), 'wb'),
            )
        # NER結果由於已經保存為pickle檔所以不需回傳
        return None
    else:
        # 不需額外處理的function則直接執行
        result = PREPROCESS_FUNCTION[args.function](dataset=dataset)
    return result


def main():
    args = parse_argument()

    # 檢查輸入的`args.source`是資料夾還是db檔
    if args.source.split('.')[-1] == 'db':
        # 如果是db檔則直接保存到`data/preprocess`資料夾下

        # 取得來源資料庫的資料
        dataset = news.parse.db.read.AllRecords(db_name=args.source)

        # 取得前處理完的結果
        result = preprocess(dataset=dataset, args=args)

        # 如果result是`None`就跳過
        if result is not None:
            # 取得寫入資料庫的連線
            tgt_conn = news.preprocess.db.util.get_conn(db_name=args.save_path)

            # 在目標資料庫建立table
            news.preprocess.db.create.create_table(cur=tgt_conn.cursor())

            # 寫入目標資料庫
            news.preprocess.db.write.write_new_records(
                cur=tgt_conn.cursor(),
                news_list=result
            )

            # Commit and close.
            tgt_conn.commit()
            tgt_conn.close()
    else:
        # 如果是資料夾則在`data/preprocess`建立名為`args.save_path`的資料夾，並
        # 將結果保存在此資料夾下

        for filename in os.listdir(
            os.path.join(
                'data',
                'parsed',
                args.source)):
            # Add filename in `args`.
            args.filename = filename

            # Initial source file path and tgt file path.
            src_file_path = os.path.join(args.source, filename)
            tgt_file_path = os.path.join(args.save_path, filename)

            # 取得來源資料庫的資料
            dataset = news.parse.db.read.AllRecords(db_name=src_file_path)
            result = preprocess(dataset=dataset, args=args)

            # 如果result是`None`就跳過
            if result is not None:
                # Get target database connection.
                tgt_conn = news.preprocess.db.util.get_conn(
                    db_name=tgt_file_path)

                # Create table.
                news.preprocess.db.create.create_table(cur=tgt_conn.cursor())

                # Write in database.
                news.preprocess.db.write.write_new_records(
                    cur=tgt_conn.cursor(),
                    news_list=result
                )

                # Commit and close.
                tgt_conn.commit()
                tgt_conn.close()


if __name__ == '__main__':
    main()
