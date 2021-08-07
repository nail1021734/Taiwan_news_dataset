# Crawler Scripts

## Chinatimes

- Using more than `3` process will get `429`.

```sh
python -m news.crawlers.main --crawler_name chinatimes --db_name chinatimes.db --debug True --past_datetime=2010-01-01T00:00:00Z
```

## CNA

- Will not get banned for certain number of process.

```sh
python -m news.crawlers.main --crawler_name cna --db_name cna.db --debug True --past_datetime=2014-01-01T00:00:00Z
```

## Epochtimes

- Will not get banned for certain number of process.

```sh
python -m news.crawlers.main --crawler_name epochtimes --db_name epochtimes.db --debug True --past_datetime=2001-01-01T00:00:00Z
```

## ETtoday

```sh
python -m news.crawlers.main --crawler_name ettoday --db_name ettoday.db --debug True --first_idx=1
```

## FTV

- Will not get banned for certain number of process.

```sh
python -m news.crawlers.main --crawler_name ftv --db_name ftv.db --debug True --past_datetime=2017-09-17T00:00:00Z
```

## NTDTV

- Will not get banned for certain number of process.

```sh
python -m news.crawlers.main --crawler_name ntdtv --db_name ntdtv.db --debug True --past_datetime=2002-01-01T00:00:00Z
```

## SETN

```sh
python -m news.crawlers.main --crawler_name setn --db_name setn.db --debug True --first_idx 1
```

## STORM

- The first available index is `21016`.
- Will not get banned for certain number of process.

```sh
# The first available index of storm is 21016.
python -m news.crawlers.main --crawler_name storm --db_name storm.db --debug True --first_idx 21016
```

## TVBS

- Using more than `4` process will get `403`.

```sh
python -m news.crawlers.main --crawler_name tvbs --db_name tvbs.db --debug True --first_idx 1
```

## UDN

```sh
python -m news.crawlers.main --crawler_name udn --db_name udn.db --debug True --past_datetime=2014-01-01T00:00:00Z
```
