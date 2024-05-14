from tools.DLog import DLog
import json

def json_decode(str_data):
    try:
        return json.loads(str_data)
    except json.JSONDecodeError:
        DLog.LogError(f"String can't be decode: {str_data}")
        return None
    
def json_encode(data):
    try:
        return json.dumps(data)
    except json.JSONDecodeError:
        DLog.LogError(f"Data can't be encode: {data}")
        return None