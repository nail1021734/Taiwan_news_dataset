import argparse

from news.split.split import split_db


def parse_argument():
    r"""
    `src` example: 'raw/ftv.db' or 'parse/ftv.db'.
    `save_dir` example: 'split_test'
    `id_interval` example: 100
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--src',
        type=str,
        help='select database to split.(selected '
        + 'database must under `data` floder).',
    )
    parser.add_argument(
        '--save_dir',
        type=str,
        help='Specify floder to save splited database',
    )
    parser.add_argument(
        '--id_interval',
        type=int,
        help='Specify data amount in every splited database.',
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # example: `python -m news.split.main --src raw/ftv.db --save_dir
    # ftv_split --id_interval 50`
    args = parse_argument()

    split_db(
        db_path=args.src, save_path=args.save_dir, id_interval=args.id_interval
    )
