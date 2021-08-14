import argparse
import os

from tqdm import tqdm

import news.crawlers.db
import news.parse
import news.parse.db

COMPANY_DICT = {
    'chinatimes': news.parse.chinatimes.parse,
    'cna': news.parse.cna.parse,
    'epochtimes': news.parse.epochtimes.parse,
    'ettoday': news.parse.ettoday.parse,
    'ftv': news.parse.ftv.parse,
    'ltn': news.parse.ltn.parse,
    'ntdtv': news.parse.ntdtv.parse,
    'setn': news.parse.setn.parse,
    'storm': news.parse.storm.parse,
    'tvbs': news.parse.tvbs.parse,
    'udn': news.parse.udn.parse,
}


def parse_argument():
    r'''
    `company` example: 'cna'
    `raw` example: `chinatimes.db`
    `save_path` example: `chinatimes.db`
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--company',
        choices=COMPANY_DICT.keys(),
        type=str,
        help='Select parser.',
    )
    parser.add_argument(
        '--raw',
        type=str,
        help='Select db or dir to parse.(From `data/raw` folder.)',
    )
    parser.add_argument(
        '--save_path',
        type=str,
        help='Specify save path.',
    )
    parser.add_argument(
        '--debug',
        type=bool,
        default=False,
        help='Select whether use debug mode.',
    )

    args = parser.parse_args()
    return args


def parse(
    raw_dataset: news.crawlers.db.schema.RawNews,
    company: str
) -> news.parse.db.schema.ParsedNews:

    data_iter = raw_dataset

    parsed_data = []
    for raw_data in tqdm(data_iter):
        try:
            parsed_data.append(COMPANY_DICT[company](raw_data))
        except Exception:
            continue

    return parsed_data


def main():
    args = parse_argument()

    # Check if raw path is dir.
    if args.raw.split('.')[-1] == 'db':
        # Read raw data.
        raw_dataset = news.crawlers.db.read.AllRecords(db_name=args.raw)

        # Parse raw data.
        parsed_data = parse(
            raw_dataset=raw_dataset,
            company=args.company
        )

        # Connect to target database.
        parsed_db_conn = news.parse.db.util.get_conn(db_name=args.save_path)

        # Create `news` table if target database didn't contain this table.
        news.parse.db.create.create_table(
            cur=parsed_db_conn.cursor()
        )

        # Write parsed data in target db.
        news.parse.db.write.write_new_records(
            cur=parsed_db_conn.cursor(),
            news_list=parsed_data
        )

        parsed_db_conn.commit()
        parsed_db_conn.close()
    else:
        raw_path = os.path.join('data', 'raw', args.raw)
        for filename in os.listdir(raw_path):
            # Read raw data.
            raw_dataset = news.crawlers.db.read.AllRecords(
                db_name=os.path.join(args.raw, filename)
            )

            # Parse raw data.
            parsed_data = parse(
                raw_dataset=raw_dataset,
                company=args.company
            )

            # Connect to target database.
            parsed_db_conn = news.parse.db.util.get_conn(
                db_name=os.path.join(args.save_path, filename)
            )

            # Create `news` table if target database didn't contain this table.
            news.parse.db.create.create_table(
                cur=parsed_db_conn.cursor()
            )

            # Write parsed data in target db.
            news.parse.db.write.write_new_records(
                cur=parsed_db_conn.cursor(),
                news_list=parsed_data
            )

            parsed_db_conn.commit()
            parsed_db_conn.close()


if __name__ == '__main__':
    main()
