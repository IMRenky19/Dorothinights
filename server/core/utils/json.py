import json

def read_json(filepath: str, **args) -> dict:
    with open(filepath, **args, encoding="utf-8") as f:
        return json.load(f)


def write_json(data: dict, filepath: str) -> None:
    with open(filepath, 'w', encoding="utf-8") as f:
        json.dump(data, f, sort_keys=False, indent=4, ensure_ascii=False)