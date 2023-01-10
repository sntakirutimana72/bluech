import json

def json_parse(data_payload):
    return json.loads(data_payload)
    
def json_stringify(serializable_payload):
    return json.dumps(serializable_payload)
