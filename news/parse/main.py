import argparse

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
    `raw_db_name` example: `chinatimes.db`
    `parsed_db_name` example: `chinatimes.db`
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--company',
        choices=COMPANY_DICT.keys(),
        type=str,
        help='Select parser.',
    )
    parser.add_argument(
        '--raw_db_name',
        type=str,
        help='Select the db to parse.(From `data/raw` folder.)',
    )
    parser.add_argument(
        '--parsed_db_name',
        type=str,
        help='Specify saved db name.',
    )
    parser.add_argument(
        '--debug',
        type=bool,
        default=False,
        help='Select whether use debug mode.',
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_argument()

    # Read raw data.
    raw_dataset = news.crawlers.db.read.AllRecords(db_name=args.raw_db_name)

    # Parse raw data.
    parsed_data = []
    data_iter = raw_dataset
    if args.debug:
        data_iter = tqdm(raw_dataset)
    for raw_data in data_iter:
        try:
            parsed_data.append(COMPANY_DICT[args.company](raw_data))
        except Exception as err:
            if args.debug:
                print(err.args[0])

    # Connect to target database.
    parsed_db_conn = news.parse.db.util.get_conn(db_name=args.parsed_db_name)
    db_cursor = parsed_db_conn.cursor()

    # Create `news` table if target database didn't contain this table.
    news.parse.db.create.create_table(cur=db_cursor)

    # Write parsed data in target db.
    news.parse.db.write.write_new_records(
        cur=db_cursor,
        news_list=parsed_data
    )

    parsed_db_conn.commit()
    parsed_db_conn.close()
