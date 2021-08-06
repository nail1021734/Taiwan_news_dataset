# Split

## parameters

- `src`: select database to split.(Path root: `data`)
- `save_dir`: Specify floder to save splited database.(Path root: `data`)
- `id_interval`: Specify data amount in every splited database.

## Example

```sh
python -m news.split.main --src raw/ftv.db --save_dir ftv_split --id_interval 50
```