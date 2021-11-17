import gc
import os
import uuid
from datetime import datetime, timezone
from typing import Final, List, Optional, Tuple

from tqdm import trange

import news.db
import news.parse.db.create
import news.parse.db.read
import news.parse.db.util
import news.parse.db.write
from news.parse.db.schema import ParsedNews


class ParsedNewsBucket:
    # Bucket is full when bucket contains 100 records.
    flush_threshold: Final[int] = 100

    def __init__(self, bucket_db_path: str):
        self.container: List[ParsedNews] = []
        self.news_counter = 0
        self.bucket_db_path = bucket_db_path

    def update(self, parsed_news: ParsedNews) -> None:
        r"""Insert records into container.

        When container is full, bucket will automatically flush records.
        """
        self.container.append(parsed_news)
        self.news_counter += 1

        # Container is full.
        if self.news_counter >= self.__class__.flush_threshold:
            self.flush()
            self.container = []
            self.news_counter = 0
            # Avoid using too many memories.
            gc.collect()

    def flush(self):
        r"""Write records in the bucket to `self.bucket_db_path`."""
        conn = news.db.get_conn(db_path=self.bucket_db_path)
        cur = conn.cursor()
        news.parse.db.create.create_table(cur=cur)
        conn.commit()
        news.parse.db.write.write_new_records(
            cur=conn.cursor(),
            news_list=self.container,
        )
        conn.commit()
        conn.close()

    def delete_bucket(self):
        r"""Delete bucket files."""
        self.flush()

        if os.path.exists(self.bucket_db_path):
            os.remove(self.bucket_db_path)


class ParsedNewsBucketList:
    BucketType = ParsedNewsBucket

    def __init__(
        self,
        db_paths: List[str],
        *,
        batch_size: Optional[int] = 1000,
        debug: Optional[bool] = False,
    ):
        # Later on we use `db_paths` to scatter records to bucket in the list.
        self.db_paths = db_paths
        self.batch_size = batch_size

        # Get datetime boundary for later bucket hashing calculation.
        (
            self.min_datetime,
            self.max_datetime,
        ) = self.__class__.get_datetime_bounds(db_paths=db_paths)

        # Create bucket list.
        self.bucket_list = self.__class__.create_bucket_list(
            min_datetime=self.min_datetime,
            max_datetime=self.max_datetime,
        )

    @classmethod
    def get_datetime_bounds(
        cls,
        db_paths: List[str],
    ) -> Tuple[datetime, datetime]:
        r"""Find datetime boundaries among merging databases.

        Later on we will use datetime boundaries to perform bucket sort.
        """
        # Recording earliest and latest datetime among merging databases.  `g_`
        # here stands for "global".  `g_min_timestamp` is initialized to
        # timestamp of now (but in UTC timezone), this guarantee any timestamp
        # in database will be smaller than `g_min_timestamp` since one cannot
        # crawl news in the future (unless you are a crazy scientist and invent
        # time travling).  `g_max_timestamp` is initialized to `0`, this
        # guarantee any timestamp in database will be larger than
        # `g_max_timestamp` since no one can publish news on Internet before
        # Internet was invented (again unless you can time travel, but I don't
        # think so).
        g_min_timestamp = int(datetime.utcnow().timestamp())
        g_max_timestamp = 0

        # A flag used to check at least one database containing `parsed_news`
        # table with actuall records inside.  If this flag remains `False` at
        # the end of this function, then no `parsed_news` tables exist.
        is_timestamp_change = False

        for db_path in db_paths:
            try:
                # Get datetime boundary from the current datebase files. `l_`
                # here stands for "local".
                (
                    l_min_timestamp,
                    l_max_timestamp,
                ) = cls.get_timestamp_bounds(db_name=db_path)

                g_min_timestamp = min(
                    g_min_timestamp,
                    l_min_timestamp,
                )
                g_max_timestamp = max(
                    g_max_timestamp,
                    l_max_timestamp,
                )
                is_timestamp_change = True
            except Exception:
                # This happened when SQLite database files do not contain
                # `parsed_news` table.  We simply skip these cases.
                continue

        # If no `parsed_news` table were found, we return current datetime with
        # UTC timezone.
        if not is_timestamp_change:
            datetime_now = datetime.utcnow().astimezone(timezone.utc)
            return (datetime_now, datetime_now)

        # Return datetime boundary with UTC timezone.
        return (
            datetime.fromtimestamp(g_min_timestamp).astimezone(timezone.utc),
            datetime.fromtimestamp(g_max_timestamp).astimezone(timezone.utc),
        )

    @classmethod
    def get_timestamp_bounds(cls, db_path: str) -> Tuple[int, int]:
        r"""Subclass need to overwrite this classmethod."""
        return news.parse.db.read.get_timestamp_bounds(db_name=db_path)

    @classmethod
    def create_bucket_list(
        cls,
        min_datetime: datetime,
        max_datetime: datetime,
    ) -> List[ParsedNewsBucket]:
        r"""Create datebase for each bucket.

        Bucket interval is set to month.
        """
        bucket_name_prefix = str(uuid.uuid4())
        start_year_and_month = datetime(
            year=min_datetime.year,
            month=min_datetime.month,
            day=1,
            tzinfo=timezone.utc,
        )
        end_year_and_month = datetime(
            year=max_datetime.year + (max_datetime.month // 12),
            month=max_datetime.month % 12 + 1,
            day=1,
            tzinfo=timezone.utc,
        )

        bucket_list: List[ParsedNewsBucket] = []
        cur_year_and_month = start_year_and_month
        while cur_year_and_month < end_year_and_month:
            bucket_name_suffix = f"{cur_year_and_month.strftime('%Y%m')}.db"
            bucket_list.append(
                cls.BucketType(
                    bucket_db_path=cls.get_db_path(
                        db_name=f'{bucket_name_prefix}__{bucket_name_suffix}'
                    )
                )
            )
            # Increment one month.
            cur_year_and_month = datetime(
                year=(
                    cur_year_and_month.year + (cur_year_and_month.month // 12)
                ),
                month=cur_year_and_month.month % 12 + 1,
                day=1,
                tzinfo=timezone.utc,
            )

        return bucket_list

    @classmethod
    def get_db_path(cls, db_name: str) -> str:
        r"""Subclass need to overwrite this classmethod."""
        return news.parse.db.util.get_db_path(db_name=db_name)

    def scatter(self):
        for db_path in self.db_paths:
            num_of_records = self.__class__.get_num_of_records(db_name=db_path)
            for offset in trange(
                    0,
                    num_of_records,
                    self.batch_size,
                    desc=f'Scattering {db_path}',
                    disable=not self.debug,
                    dynamic_ncols=True,
            ):
                for parsed_news in self.__class__.read_some_records(
                        db_name=db_path,
                        limit=self.batch_size,
                        offset=offset,
                ):
                    # Use hash to get
                    bucket_idx = self.get_bucket_idx_by_hash(parsed_news)
                    self.bucket_list[bucket_idx].update(parsed_news)

    @classmethod
    def get_num_of_records(cls, db_name: str) -> int:
        return news.parse.db.read.get_num_of_records(db_name=db_name)

    @classmethod
    def read_some_records(
        cls,
        db_name: str,
        limit: int,
        offset: int,
    ) -> List[ParsedNews]:
        r"""Subclass need to overwrite this classmethod."""
        return news.parse.db.read.read_some_records(
            db_name=db_name,
            limit=limit,
            offset=offset,
        )

    def get_bucket_idx_by_hash(self, parsed_news: ParsedNews) -> int:
        datetime_obj = datetime.fromtimestamp(parsed_news.timestamp)
        year = datetime_obj.year
        month = datetime_obj.month

        return (year - self.min_datetime.year
               ) * 12 + (month - self.min_datetime.month) % 12

    def delete_bucket_list(self):
        pass
