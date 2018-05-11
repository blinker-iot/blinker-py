import json

def check_json_format(raw_msg):
    if isinstance(raw_msg, str):
        if raw_msg[0] == '{':
            try:
                json.loads(raw_msg, encoding='utf-8')
            except ValueError:
                return False
            return True
        else:
            return False
    else:
        return False

def json_encode(key, value):
    data = {}
    data[key] = value
    data = json.dumps(data)
    return data