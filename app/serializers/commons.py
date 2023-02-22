import json
import typing as yi

from app.settings import ENCODING

class PayloadJSONSerializer:
    @staticmethod
    def as_json(data_obj: str):
        return json.loads(data_obj)

    @staticmethod
    def as_string(data_obj: dict):
        return json.dumps(data_obj)

    @staticmethod
    def from_bytes(data_obj: bytes):
        return data_obj.decode(ENCODING)

    @staticmethod
    def as_bytes(data_obj: str):
        return data_obj.encode(ENCODING)

    @classmethod
    def decompress(cls, payload: bytes) -> dict[str, yi.Any]:
        as_str = cls.from_bytes(payload)
        return cls.as_json(as_str)

    @classmethod
    def compress(cls, obj: dict[str, yi.Any]):
        as_str = cls.as_string(obj)
        as_byte = cls.as_bytes(as_str)
        content_size = len(as_byte)
        content = cls.as_bytes(f'{content_size:04d}') + as_byte
        return content
