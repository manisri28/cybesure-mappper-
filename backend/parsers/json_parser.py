import json

def parse_json(file):
    data = json.load(file)
    return json.dumps(data)
