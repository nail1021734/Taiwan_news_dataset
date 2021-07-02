# Crawler Scripts

## Chinatimes

```sh
python run_crawler.py --crawler_name chinatimes --db_name chinatimes.db --debug True --past_datetime=2010-01-01T00:00:00Z
```

## CNA

```sh
python run_crawler.py --crawler_name cna --db_name cna.db --debug True --past_datetime=2014-01-01T00:00:00Z
```

## Epochtimes

```sh
python run_crawler.py --crawler_name epochtimes --db_name epochtimes.db --debug True --past_datetime=2001-01-01T00:00:00Z
```

## ETtoday

```sh
python run_crawler.py --crawler_name ettoday --db_name ettoday.db --debug True --first_idx=1
```

## NTDTV

```sh
python run_crawler.py --crawler_name ntdtv --db_name ntdtv.db --debug True --past_datetime=2002-01-01T00:00:00Z
```

## SETN

```sh
python run_crawler.py --crawler_name setn --db_name setn.db --debug True --first_idx 1
```

## STORM

```sh
# The first available index of storm is 21016.
python run_crawler.py --crawler_name storm --db_name storm.db --debug True --first_idx 21016
```

## TVBS

```sh
python run_crawler.py --crawler_name tvbs --db_name tvbs.db --debug True --first_idx 1
```
