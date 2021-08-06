# Parse

## parameters

- `company`: Select parser.
- `raw_db_name`: Select the database to parse.(Path root: `data/raw`)
- `parsed_db_name`: Specify saved db name.(Path root: `data/parsed`)
- `debug`: Select whether use debug mode.

## example

```sh
python -m --company ftv --raw_db_name raw_ftv.db --parsed_db_name parsed_ftv.db --debug True
```