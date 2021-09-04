import argparse

from news.merge.merge import merge_db


def parse_argument():
    r'''
    `dir_path` example: 'raw/split_test'.
    `save_db` example: 'merge_test.db'
    `reserve_id` example: `True` or `False`
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dir_path',
        type=str,
        help='select dir to merge.(selected ' +
        'dir must under `data` floder).',
    )
    parser.add_argument(
        '--save_db',
        type=str,
        help='Specify database to save all data.',
    )

    def boolean_type(string):
        return string == 'True'
    parser.add_argument(
        '--reserve_id',
        type=boolean_type,
        help='Specify if reserve origin id.',
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # example: `python -m news.merge.main --dir_path ftv_split --save_db ftv_merge.db --reserve_id False`
    args = parse_argument()

    merge_db(
        dir_path=args.dir_path,
        save_db=args.save_db,
        reserve_id=args.reserve_id
    )
