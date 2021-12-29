import dataclasses
import json


class EnhancedJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def dataclass_to_json(data):
    return json.dumps(
        data, cls=EnhancedJSONEncoder, ensure_ascii=False, indent=4
    )


def dataclass_from_dict(klass, d):
    try:
        fieldtypes = {f.name: f.type for f in dataclasses.fields(klass)}
        return klass(**{f: dataclass_from_dict(fieldtypes[f], d[f]) for f in d})
    except:
        return d  # Not a dataclass field
