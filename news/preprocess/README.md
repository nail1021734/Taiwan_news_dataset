# preprocess

## parameters

- `function`: select preprocess function.
- `source`: Specify database or dir to perform preprocess.(Path root: `data/parsed`)
- `save_path`: Specify save path.(Path root: `data/preprocess`)
- `min_length`(optional): Specify min article length when use length filter.
- `max_length`(optional): Specify max article length when use length filter.
- `NER_format`(optional): Specify replace format when use `ner_tag_subs` method.
- `NER_result`(optional): Specify NER_result path when use `ner_tag_subs` or `date_filter` method.(Path root: `data`)

## NER_format

`Ner_format` need to input a list comtain one or many dictionarys.

- `type`: Specify one or many NER type to replace by `tag`.
- `tag`: Specify tag pattern.(Example `"loc"` will be `"<loc>"`)
- `NeedID`: If true then every tag of same word will have same ID.(Example: when tag is `"loc"` will be `"<loc0>"`)

### NER_format example

**Notice!! boolean value must be lower case.**

```python
[
    {"type":["ORG"、"loc"], "tag":"loc","NeedID":false},
    {"type":['PERSON'], "tag":"per","NeedID":true}
]
```

## preprocess example
```sh
python -m news.preprocess.main --source ftv_split --function ner_tag_subs --save_path ftv_ner_subs --NER_format '[{"type":["ORG"],"tag":"org","NeedID":true}]' --NER_result ftv_NER_result

python -m news.preprocess.main --source ftv_split --function NER_dataset --save_path ftv_NER_result

python -m news.preprocess.main --source ftv_split --function length_filter --save_path ftv_len --min_length 200 --max_length 1000

python -m news.preprocess.main --source ftv_split --function date_filter --save_path date --NER_result ftv_NER_result
```