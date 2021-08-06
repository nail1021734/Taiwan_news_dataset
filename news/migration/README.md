# migration

## parameters

- `src`: Select db to perform migration.(PATH root: `data`)
- `migrate_version`: Select migrate version.
- `save_path`: Specify path to save result.(PATH root: `data/raw`)

## example

```sh
python -m news.migration.main --src ettoday_split --save_path ettoday_migration --migrate_version v1
```