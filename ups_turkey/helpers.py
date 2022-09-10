import json
from ups_turkey.encoders import DecimalEncoder

def to_json(data):
    return json.dumps(data, ensure_ascii=False, cls=DecimalEncoder)