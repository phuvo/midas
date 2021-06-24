from datetime import datetime, timezone
from midas.helpers.datetime import from_ms


def test_from_ms():
    dt = from_ms(1612345678_000).astimezone(timezone.utc)
    assert dt == datetime.fromisoformat('2021-02-03T09:47:58+00:00')
