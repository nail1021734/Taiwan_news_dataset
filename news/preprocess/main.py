import argparse
from news.parse.db.schema import ParsedNews
import news.parse.db
import news.preprocess.db
import os
import pickle
import json
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
}


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--function',
        type=str,
        help='select preprocess function.',
    )
    parser.add_argument(
        '--source',
        type=str,
        help='Specify database or dir to perform preprocess.',
    )
    parser.add_argument(
        '--target',
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
        help='Specify NER_result path when use `ner_tag_subs` method.'
    )

    args = parser.parse_args()
    return args


def preprocess(
    dataset: ParsedNews,
    args: argparse.Namespace,
):
    # According to different function give different parameter.
    if args.function == 'length_filter':
        result = PREPROCESS_FUNCTION[args.function](
            dataset=dataset,
            min_length=args.min_length,
            max_length=args.max_length
        )
    elif args.function == 'date_filter':
        # Check if source is dir.
        if args.source.split('.')[-1] == 'db':
            result_file_path = os.path.join('data', args.NER_result)
            result = PREPROCESS_FUNCTION[args.function](
                dataset=dataset,
                result_path=result_file_path
            )
        else:
            result_file_name = args.filename.split('.')[0] + '.pickle'
            result_file_path = os.path.join(
                'data', args.NER_result, result_file_name)
            result = PREPROCESS_FUNCTION[args.function](
                dataset=dataset,
                result_path=result_file_path
            )
    elif args.function == 'ner_tag_subs':
        # Check if source is dir.
        if args.source.split('.')[-1] == 'db':
            result_file_path = os.path.join('data', args.NER_result)
            result = PREPROCESS_FUNCTION[args.function](
                dataset=dataset,
                tag_dict=args.NER_format,
                result_path=result_file_path
            )
        else:
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
        # Check if source is dir.
        if args.source.split('.')[-1] == 'db':
            # If source not dir then save as file.
            target_path = os.path.join('data', args.target)
            pickle.dump(NER_result, open(target_path, 'wb'))
        else:
            # If source is dir then save in dir.
            target_path = os.path.join('data', args.target)
            # Create target dir if not exist.
            if not (os.path.exists(target_path)
                    or os.path.isfile(target_path)):
                os.makedirs(target_path)

            # Initial Save filename.
            filename = args.filename.split('.')[0] + '.pickle'

            # Save in pickle file.
            pickle.dump(
                NER_result,
                open(os.path.join(target_path, f'{filename}'), 'wb'),
            )
        return None
    else:
        result = PREPROCESS_FUNCTION[args.function](dataset=dataset)
    return result


def main():
    args = parse_argument()

    # Check source is file or dir.
    if args.source.split('.')[-1] == 'db':
        dataset = news.parse.db.read.AllRecords(db_name=args.source)
        result = preprocess(dataset=dataset, args=args)

        # If result is `None` then pass.
        if result is not None:
            # Get target database connection.
            tgt_conn = news.preprocess.db.util.get_conn(db_name=args.target)

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
    else:
        for filename in os.listdir(os.path.join('data', 'parsed', args.source)):
            # Add filename in `args`.
            args.filename = filename

            # Initial source file path and tgt file path.
            src_file_path = os.path.join(args.source, filename)
            tgt_file_path = os.path.join(args.target, filename)

            # Read source dataset.
            dataset = news.parse.db.read.AllRecords(db_name=src_file_path)
            result = preprocess(dataset=dataset, args=args)

            # If result is `None` then pass.
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
