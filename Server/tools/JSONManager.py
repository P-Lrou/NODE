from tools.DLog import DLog
import json

def json_decode(data: str) -> dict:
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        DLog.LogError(f"String can't be decode: {data}")
        return None
    
def json_encode(data: dict) -> str:
    try:
        return json.dumps(data)
    except json.JSONDecodeError:
        DLog.LogError(f"Data can't be encode: {data}")
        return None