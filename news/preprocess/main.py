import argparse
import gc
import sys
import textwrap
from typing import Callable, List

from tqdm import trange

import news.db
import news.parse.db.read
import news.parse.db.util
import news.parse.db.write
import news.path
import news.preprocess.db.create
import news.preprocess.db.util
from news.preprocess.filters import (
    NFKC, brackets_filter, curly_brackets_filter, emoji_filter, length_filter,
    lenticular_brackets_filter, non_CJK_filter, parentheses_filter, url_filter
)
from news.preprocess.ner_preprocessor import TAG_TABLE, ner_entity_replacer
from news.preprocess.replacer import (
    english_replacer, guillemet_replacer, number_replacer
)


def parse_args(argv: List[str]) -> argparse.Namespace:
    r"""Preprocess command line arguments.

    Example
    =======
    python -m news.preprocess.main         \
        --batch_size 1000                  \
        --db_name rel/my.db                \
        --db_name /abs/my.db               \
        --db_dir rel_dir                   \
        --db_dir /abs_dir                  \
        --save_db_name out.db              \
        --debug                            \
        --use_min_length_filter 200        \
        --use_max_length_filter 1000       \
        --use_url_filter                   \
        --use_parentheses_filter           \
        --use_brackets_filter              \
        --use_curly_brackets_filter        \
        --use_lenticular_brackets_filter   \
        --use_not_cjk_filter               \
        --use_emoji_filter                 \
        --ner_class ORG PERSON LOC         \
        --ner_need_id_class ORG PERSON LOC \
        --use_date_replacer                \
        --use_english_replacer             \
        --use_guillemet_replacer           \
        --use_number_replacer
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        '--batch_size',
        type=int,
        default=1000,
        help=textwrap.dedent(
            """\
            Preprocess batch size. Controll batch size to avoid excess
            memories.
            """
        ),
    )
    parser.add_argument(
        '--db_name',
        action='append',
        type=str,
        help=textwrap.dedent(
            f"""\
            SQLite database file name wanted to preprocess.  If absolute path
            is given, then treat the given path as database file and read
            records directly from the given path.

            For example, excuting

                --db_name /abs/my.db

            will collect the file

                /abs/my.db

            If relative path is given, then we assume the given path is under
            the path `PROJECT_ROOT/data/preprocessed`.
            Currently project root is set to {news.path.PROJECT_ROOT}.

            For example, executing

                --db_name rel/my.db

            will collect the file

                PROJECT_ROOT/data/preprocessed/rel/my.db

            One can specify multiple database files at the same time using
            multiple `--db_name`.

            For example, executing

                --db_name rel/a.db --db_name rel/b.db --db_name /abs/c.db

            will collect all the following files

                PROJECT_ROOT/data/preprocessed/rel/a.db
                PROJECT_ROOT/data/preprocessed/rel/b.db
                /abs/c.db
            """
        ),
    )
    parser.add_argument(
        '--db_dir',
        action='append',
        type=str,
        help=textwrap.dedent(
            f"""\
            Directory contains SQLite database files.  If absolute path is
            given, then recursively search the directory to find all sqlite
            database files.

            For example, if `/abs/dir` contains

                a.db
                b.db
                subdir/c.db
                subdir/d.db

            then executing

                --db_dir /abs/dir

            will collect all the following files

                /abs/dir/a.db
                /abs/dir/b.db
                /abs/dir/subdir/c.db
                /abs/dir/subdir/d.db

            If relative path is given, then we assume the given directory is
            under the path `PROJECT_ROOT/data/parsed`.  Currently project root
            is set to {news.path.PROJECT_ROOT}.

            For example, if `PROJECT_ROOT/data/parsed/rel/dir` contains

                a.db
                b.db
                subdir/c.db
                subdir/d.db

            then executing

                --db_dir rel/dir

            will collect all the following files

                PROJECT_ROOT/data/parsed/rel/dir/a.db
                PROJECT_ROOT/data/parsed/rel/dir/b.db
                PROJECT_ROOT/data/parsed/rel/dir/subdir/c.db
                PROJECT_ROOT/data/parsed/rel/dir/subdir/d.db

            One can specify multiple directory at the same time using multiple
            `--db_dir`.

            Continue from previouse example, excuting

                --db_dir rel/dir --db_dir /abs/dir

            will collect all the following files

                /abs/dir/a.db
                /abs/dir/b.db
                /abs/dir/subdir/c.db
                /abs/dir/subdir/d.db
                PROJECT_ROOT/data/parsed/rel/dir/a.db
                PROJECT_ROOT/data/parsed/rel/dir/b.db
                PROJECT_ROOT/data/parsed/rel/dir/subdir/c.db
                PROJECT_ROOT/data/parsed/rel/dir/subdir/d.db
            """
        ),
    )
    parser.add_argument(
        '--save_db_name',
        type=str,
        required=True,
        help=textwrap.dedent(
            f"""\
            Name of the database to save preprocessed results.  Create file if
            given path does not exist (along with non-existed directories in
            the path).  If absolute path is given, then treat the given path as
            SQLite database file.

            For example, executing

                --save_db_name /abs/my.db

            will output preprocessed news to the file

                /abs/my.db

            If relative path is given, then we assume the given path is under
            the path `PROJECT_ROOT/data/preprocessed`.
            Currently project root is set to {news.path.PROJECT_ROOT}.

            For example, executing

                --save_db_name rel/my.db

            will output preprocessed news to the file

                PROJECT_ROOT/data/preprocessed/rel/my.db
            """
        ),
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help=textwrap.dedent(
            """\
            Select whether to use debug mode.  In debug mode it outputs
            progress bar to stderr and error messages to stdout.
            """
        ),
    )
    parser.add_argument(
        '--use_url_filter',
        action='store_true',
        help=textwrap.dedent(
            """\
            將輸入資料集的 url 過濾掉.
            """,
        ),
    )
    parser.add_argument(
        '--use_parentheses_filter',
        action='store_true',
        help=textwrap.dedent(
            """\
            將小括號內的句子以及括號一起過濾掉.
            """,
        ),
    )
    parser.add_argument(
        '--use_brackets_filter',
        action='store_true',
        help=textwrap.dedent(
            """\
            將中括號內的句子以及括號一起過濾掉.
            """,
        ),
    )
    parser.add_argument(
        '--use_curly_brackets_filter',
        action='store_true',
        help=textwrap.dedent(
            """\
            將大括號內的句子以及括號一起過濾掉.
            """,
        ),
    )
    parser.add_argument(
        '--use_lenticular_brackets_filter',
        action='store_true',
        help=textwrap.dedent(
            """\
            將透鏡狀括號(【】)內的句子以及括號一起過濾掉.
            """,
        ),
    )
    parser.add_argument(
        '--use_emoji_filter',
        action='store_true',
        help=textwrap.dedent(
            """\
            過濾 emoji.
            """,
        ),
    )
    parser.add_argument(
        '--use_not_cjk_filter',
        action='store_true',
        help=textwrap.dedent(
            r"""\
            將中文, 英文, 數字以及特定標點符號
            (包含 `.~<、,。《?>*\-!》:」「+%/()\[\]【】`)以外的符號過濾掉.
            """
        ),
    )
    parser.add_argument(
        '--use_min_length_filter',
        type=int,
        default=0,
        required=False,
        help=textwrap.dedent(
            """\
            將長度小於 `min_length` 的文章過濾, 預設為 0.
            """
        ),
    )
    parser.add_argument(
        '--use_max_length_filter',
        type=int,
        default=-1,
        required=False,
        help=textwrap.dedent(
            """\
            將長度大於 `max_length` 的文章過濾, -1 表示不限制文章長度, 預設為 -1.
            """
        ),
    )
    parser.add_argument(
        '--ner_class',
        type=str,
        nargs='*',
        choices=TAG_TABLE.keys(),
        required=False,
        help=textwrap.dedent(
            """\
            選擇哪些 NER 類別要被替換為 tag. 總共 10 種類別
            例如: `--ner_class GPE PERSON`, 表示要將 GPE 和 PERSON 替換成 tag.
            - GPE 替換為 `<gpe>`.
            - PERSON 替換為 `<per>`.
            - ORG 替換為 `<org>`.
            - NORP 替換為 `<nrp>`.
            - LOC 替換為 `<loc>`.
            - FAC 替換為 `<fac>`.
            - PRODUCT 替換為 `<prod>`.
            - WORK_OF_ART 替換為 `<woa>`.
            - EVENT 替換為 `<evt>`.
            - LAW 替換為 `<law>`.
            """
        ),
    )
    parser.add_argument(
        '--ner_need_id_class',
        type=str,
        nargs='*',
        choices=TAG_TABLE.keys(),
        required=False,
        help=textwrap.dedent(
            """\
            選擇要被替換為 tag 的 NER 類別相同的詞是否要用相同 id 來表示.
            例如: `--ner_need_id_class GPE PERSON`, 表示要將 GPE 和 PERSON 替換成 tag.
            同個文章內同為 GPE 類別的 "台北" 會變成 `<gpe0>` , 而 "台中" 為 `<gpe1>`
            (不同詞之間用不同 id 表示).
            """
        ),
    )
    parser.add_argument(
        '--use_date_replacer',
        action='store_true',
        help=textwrap.dedent(
            """\
            當對資料集進行 NER 類別的替換時, 是否將 DATE 類別中的數字轉換為 `<num>`.
            """
        ),
    )
    parser.add_argument(
        '--use_english_replacer',
        action='store_true',
        help=textwrap.dedent(
            """\
            將英文開頭的連續英文, 數字或空白換成 `<en>` tag.
            """
        ),
    )
    parser.add_argument(
        '--use_guillemet_replacer',
        action='store_true',
        help=textwrap.dedent(
            """\
            將書名號內的詞換為 `<unk>`, 並且留下書名號本身.
            """,
        ),
    )
    parser.add_argument(
        '--use_number_replacer',
        action='store_true',
        help=textwrap.dedent(
            """\
            將阿拉伯數字換為 `<num>` tag.
            """,
        ),
    )
    parser.add_argument(
        '--ner_device',
        type=int,
        required=False,
        default=0,
        help=textwrap.dedent(
            """\
            指定 NER 時要使用的設備, 0 表示使用 cuda:0, -1 表示使用 GPU, 預設是 0.
            """,
        ),
    )

    return parser.parse_args(argv)


def get_func_list(args: argparse.Namespace,) -> List[Callable]:
    # 為了和 parsing 結果統一格式會先對資料進行 NFKC 以及將多個空白合成一個空白的動作.
    func_list = [NFKC]

    # 以下前處理方法不會將文字替換成 tag, 因此先進行處理.
    if args.use_url_filter:
        func_list.append(url_filter)
    if args.use_parentheses_filter:
        func_list.append(parentheses_filter)
    if args.use_brackets_filter:
        func_list.append(brackets_filter)
    if args.use_curly_brackets_filter:
        func_list.append(curly_brackets_filter)
    if args.use_lenticular_brackets_filter:
        func_list.append(lenticular_brackets_filter)
    if args.use_emoji_filter:
        func_list.append(emoji_filter)
    if args.use_not_cjk_filter:
        func_list.append(non_CJK_filter)
    if not (args.use_min_length_filter == 0
            and args.use_max_length_filter == -1):
        func_list.append(length_filter)

    # 以下前處理方法會將部份文字替換成 tag.
    if 'ner_class' in args or args.use_date_replacer:
        func_list.append(ner_entity_replacer)
    if args.use_english_replacer:
        func_list.append(english_replacer)
    if args.use_guillemet_replacer:
        func_list.append(guillemet_replacer)
    if args.use_number_replacer:
        func_list.append(number_replacer)

    return func_list


def preprocess(
    dataset: List[news.parse.db.schema.ParsedNews],
    func_list: List[Callable],
    args: argparse.Namespace,
) -> List[news.parse.db.schema.ParsedNews]:

    # Run preprocess in specified order.
    for func in func_list:
        # Run preprocess function.
        dataset = func(dataset=dataset, args=args)

    return dataset


def main(argv: List[str]) -> None:
    args = parse_args(argv=argv)

    if args.db_name is None:
        args.db_name = []
    if args.db_dir is None:
        args.db_dir = []

    # Map relative paths to absolute paths under `PROJECT_ROOT/data/parse`.
    db_paths = news.db.get_db_paths(
        file_paths=list(
            map(
                news.parse.db.util.get_db_path,
                args.db_name + args.db_dir,
            )
        ),
    )

    save_db_path = news.preprocess.db.util.get_db_path(
        db_name=args.save_db_name
    )
    save_conn = news.db.get_conn(db_path=save_db_path)
    save_cur = save_conn.cursor()
    news.parse.db.create.create_table(cur=save_cur)

    # Get sorted preprocess function list.
    func_list = get_func_list(args)

    for db_path in db_paths:
        try:
            # Must use absolute path `db_path` since some absolute paths is not
            # in default locations (which is `PROJECT_ROOT/data/parsed`). This
            # is fine since `get_num_of_records` use `get_db_path` internally.
            # Note that this statement usually take a long times.
            num_of_records = news.parse.db.read.get_num_of_records(
                db_name=db_path,
            )
        except Exception as err:
            print(f'Failed to get number of records in {db_path}: {err}')

        # Preprocess `ParsedNews` by batch.
        for offset in trange(
                0,
                num_of_records,
                args.batch_size,
                desc=f'Preprocessing {db_path}',
                dynamic_ncols=True,
        ):
            try:
                parsed_news_list = news.parse.db.read.read_some_records(
                    db_name=db_path,
                    offset=offset,
                    limit=args.batch_size,
                )
                preprocessed_news = preprocess(
                    dataset=parsed_news_list,
                    func_list=func_list,
                    args=args,
                )
                news.parse.db.write.write_new_records(
                    cur=save_cur,
                    news_list=preprocessed_news,
                )

                save_conn.commit()

                # Avoid using too many memories.
                del parsed_news_list
                del preprocessed_news
                gc.collect()
            except Exception:
                print(f'Failed to write records at id {offset} of {db_path}.')

    save_conn.close()


if __name__ == '__main__':
    main(argv=sys.argv[1:])
