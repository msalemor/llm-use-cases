from collections import defaultdict
from threading import Lock


class ThreadSafeDict:
    def __init__(self):
        self.lock = Lock()
        self.data = defaultdict(list)

    def set(self, key, value):
        with self.lock:
            self.data[key] = value

    def get(self, key):
        with self.lock:
            return self.data.get(key, None)

    def append(self, key, value):
        with self.lock:
            self.data[key].append(value)

    def items(self):
        with self.lock:
            return list(self.data.items())
