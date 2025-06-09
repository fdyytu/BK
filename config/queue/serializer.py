import json
from typing import Any

def serialize_message(message: Any, format: str = "json") -> bytes:
    if format == "json":
        return json.dumps(message).encode("utf-8")
    elif format == "str":
        return str(message).encode("utf-8")
    else:
        raise ValueError("Unsupported serialization format")

def deserialize_message(data: bytes, format: str = "json") -> Any:
    if format == "json":
        return json.loads(data.decode("utf-8"))
    elif format == "str":
        return data.decode("utf-8")
    else:
        raise ValueError("Unsupported deserialization format")