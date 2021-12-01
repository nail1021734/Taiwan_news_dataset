import argparse
import gc
import sys
import textwrap
from typing import Callable, Dict, List

from tqdm import trange

import news.parse.db.read
import news.parse.db.util
import news.preprocess.db.util
import news.parse.db.write
import news.preprocess.db.create

import news.db
import news.path
from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews
from news.preprocess.preprocess import preprocess_by_flag


def parse_args(argv: List[str]) -> argparse.Namespace:
    r"""Preprocess command line arguments.

    Example
    =======
    python -m news.preprocess.main   \
        --batch_size 1000            \
        --db_name rel/my.db          \
        --db_name /abs/my.db         \
        --db_dir rel_dir             \
        --db_dir /abs_dir            \
        --save_db_name out.db        \
        --debug                      \
        --function_flag 11111111111  \
        --NER_flag 0110100000        \
        --NER_NeedID_flag 0110100000 \
        --filter_date                \
        --min_length 200             \
        --max_length 1000
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
            Preprocess batch size. Controll batch size to avoid excess memories.
            """
        ),
    )
    parser.add_argument(
        '--db_name',
        action='append',
        type=str,
        help=textwrap.dedent(
            f"""\
            SQLite database file name wanted to preprocess.  If absolute path is
            given, then treat the given path as database file and read records
            directly from the given path.

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
            given path does not exist (along with non-existed directories in the
            path).  If absolute path is given, then treat the given path as
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
        '--function_flag',
        type=str,
        required=True,
        help=textwrap.dedent(
            f"""\
            選擇要執行的前處理方法. 總共11種前處理方法分別對應到11個 bit
            每個 bit 照順序代表的前處理方法如下
            1. `NFKC`: 對輸入資料集進行 NFKC 正規化.
            2. `url_filter`: 將輸入資料集的 url 過濾掉.
            3. `whitespace_filter`: 將多個空白換成一個.
            4. `parentheses_filter`: 將小括號, 中括號, 以及【】內的句子以及括號一起過濾掉.
            5. `not_CJK_filter`: 將中文, 英文, 數字以及特定標點符號
            (包含.~<、,。《?>*\-!》:」「+%/()\[\]【】)以外的符號過濾掉.
            6. `length_filter`: 將長度小於 `min_length` 或大於 `max_length` 的文章過濾
            掉, 預設為小於200或大於1000的文章會被過慮掉.
            7. `ner_tag_subs_flag_version`: 將 NER 辨識出來的某個類別替換為 tag,
            需給定 `NER_flag` 以及 `NER_NeedID_flag` 參數, 並且預設會將日期類別中的數字
            替換為 `<num>`, 若不想將日期過濾掉可以設定 `filter_date` 參數為 `False`(
            預設為 `True`).
            8. `english_to_tag`: 將英文開頭的連續英文, 數字或空白換成 `<en>` tag.
            9. `guillemet_filter`: 將書名號內的詞換為 `<unk>`, 並且留下書名號本身.
            10. `number_filter`: 將阿拉伯數字換為 `<num>` tag.
            """
        ),
    )
    parser.add_argument(
        '--NER_flag',
        type=str,
        required=False,
        help=textwrap.dedent(
            f"""\
            選擇哪些 NER 類別要被替換為 tag, 每個 bit 對應到的類別順序如下
            1. GPE 替換為 `<gpe>`.
            2. PERSON 替換為 `<per>`.
            3. ORG 替換為 `<org>`.
            4. NORP 替換為 `<nrp>`.
            5. LOC 替換為 `<loc>`.
            6. FAC 替換為 `<fac>`.
            7. PRODUCT 替換為 `<prdt>`.
            8. WORK_OF_ART 替換為 `<woa>`.
            9. EVENT 替換為 `<evt>`.
            10. LAW 替換為 `<law>`.
            """
        ),
    )
    parser.add_argument(
        '--NER_NeedID_flag',
        type=str,
        required=False,
        help=textwrap.dedent(
            f"""\
            選擇要被替換為 tag 的 NER 類別, 相同的詞是否要有相同 id 來表示
            每個 bit 對應到的類別順序如下.
            1. `<gpe>` 後加上 id, 例如： `<gpe1>`.
            2. `<per>` 後加上 id, 例如： `<per1>`.
            3. `<org>` 後加上 id, 例如： `<org1>`.
            4. `<nrp>` 後加上 id, 例如： `<nrp1>`.
            5. `<loc>` 後加上 id, 例如： `<loc1>`.
            6. `<fac>` 後加上 id, 例如： `<fac1>`.
            7. `<prdt>` 後加上 id, 例如： `<prdt1>`.
            8. `<woa>` 後加上 id, 例如： `<woa1>`.
            9. `<evt>` 後加上 id, 例如： `<evt1>`.
            10. `<law>` 後加上 id, 例如：`<law1>` .
            """
        ),
    )
    parser.add_argument(
        '--filter_date',
        action='store_true',
        help=textwrap.dedent(
            f"""\
            當對資料集進行 NER 類別的替換時, 是否將 DATE 類別中的數字轉換為 `<num>`.
            """
        ),
    )
    parser.add_argument(
        '--min_length',
        type=int,
        required=False,
        help=textwrap.dedent(
            f"""\
            執行 `length_filter` 時, 要保留的文章最短長度.
            """
        ),
    )
    parser.add_argument(
        '--max_length',
        type=int,
        required=False,
        help=textwrap.dedent(
            f"""\
            執行 `length_filter` 時, 要保留的文章最長長度.
            """
        ),
    )
    return parser.parse_args(argv)


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
                preprocessed_news = preprocess_by_flag(
                    dataset=parsed_news_list, **args.__dict__
                )
                news.parse.db.write.write_new_records(
                    cur=save_cur,
                    news_list=preprocessed_news,
                )

                save_conn.commit()

                # Avoid using too many memories.
                gc.collect()
            except Exception as err:
                print(err.args)
                print(f'Failed to write records at id {offset} of {db_path}.')

    save_conn.close()


if __name__ == '__main__':
    main(argv=sys.argv[1:])
