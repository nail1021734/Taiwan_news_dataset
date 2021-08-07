# Parse

## parameters

- `company`: Select parser.
- `raw`: Select the database or dir to parse.(Path root: `data/raw`)
- `save_path`: Specify saved db or dir name.(Path root: `data/parsed`)
- `debug`: Select whether use debug mode.

## example

```sh
python -m news.parse.main --company ftv --raw raw_ftv.db --save_path parsed_ftv.db --debug True
```