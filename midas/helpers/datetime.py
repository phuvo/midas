from datetime import datetime

def from_ms(ms: int):
    return datetime.fromtimestamp(ms / 1000)

def to_ms(dt: datetime):
    return round(dt.timestamp() * 1000)
