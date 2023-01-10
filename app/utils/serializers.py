import json
import typing

from ..settings import ENCODING

def json_parse(data_payload):
    return json.loads(data_payload)
    
def json_stringify(serializable_payload):
    return json.dumps(serializable_payload)
    
def from_bytes(data: bytes):
    return data.decode(ENCODING)
    
def to_bytes(data: typing.Any):
    return data.encode(ENCODING)
    
def decompress(request: typing.Dict[str, typing.Any]):
    as_string = from_bytes(request)
    return json_parse(as_string)
    
def compress(response):
    as_string = json_stringify(response)
    return to_bytes(as_string)
