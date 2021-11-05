import json


def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        raw_json = f.read()
        if not raw_json:
            return []
        return json.loads(raw_json)


def write_json(filename,json_data):
    with open(filename, 'w', encoding='utf-8',) as f:
        json.dump(json_data, f, ensure_ascii=False, indent='\t')
