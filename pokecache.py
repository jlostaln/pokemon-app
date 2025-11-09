import time

class CacheRecord:
    def __init__(self, value):
        self.created_at = time.time()
        self.value = value

class Cache:
    def __init__(self) -> None:
        self.cache_data = {}

    def add(self, key, value):
        self.cache_data[key] = CacheRecord(value)

    def get(self, key):
        record = self.cache_data.get(key)
        if record:
            return record.value
        return None

