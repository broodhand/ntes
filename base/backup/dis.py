import json


def dicttojson(item):
    if isinstance(item, (list, tuple)):
        print(item)
        return list(map(dicttojson, item))
    if isinstance(item, dict):
        return json.dumps(item)
    else:
        return item


