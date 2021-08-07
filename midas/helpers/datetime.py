from datetime import datetime

_local_tz = datetime.now().astimezone().tzinfo

def get_tz():
    return _local_tz

def from_ms(ms: int):
    return datetime.fromtimestamp(ms / 1000, _local_tz)

def to_ms(dt: datetime):
    return round(dt.timestamp() * 1000)
