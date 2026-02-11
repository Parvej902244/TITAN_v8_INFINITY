import time

class NegativeMemory:
    def __init__(self, ttl=3600):
        self.safe_paths = {}
        self.ttl = ttl

    def mark_safe(self, method, url):
        self.safe_paths[f"{method}:{url}"] = time.time()

    def is_known_safe(self, method, url):
        key = f"{method}:{url}"
        if key in self.safe_paths:
            if time.time() - self.safe_paths[key] < self.ttl:
                return True
            del self.safe_paths[key]
        return False
      
