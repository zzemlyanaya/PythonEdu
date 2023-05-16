import datetime
import time
import pickle
from threading import Lock, Thread


class HideousCache:
    def __init__(self):
        self.cache = {}  # dict[(qname, qtype, qclass): (rr, time received)]
        self.lock = Lock()

    def __getitem__(self, item):
        with self.lock:
            return self.cache[item]

    def __contains__(self, item):
        with self.lock:
            return item in self.cache

    def append(self, key, item):
        with self.lock:
            if key in self.cache:
                self.cache[key].append(item)
            else:
                self.cache[key] = [item]

    def remove_expired(self):
        now = time.time()
        with self.lock:
            for k in self.cache:
                records = self.cache[k]
                for rr in records:
                    if rr[0].ttl < (now - rr[1]):
                        records.remove(rr)


class HideousCacheController:
    def __init__(self):
        self.cache = HideousCache()
        self.filename = 'HideousCache.json'
        print('Loading cache from file')
        self.cache.cache = self.load_cache()
        print('Cache loaded')

        print('Starting cache daemon')
        self.daemon = Thread(target=cache_daemon, args=[self.cache], daemon=True, name='Cache Daemon')

    def save_cache(self):
        file = open(self.filename, 'wb')
        pickle.dump(self.cache.cache, file)
        file.close()

    def load_cache(self):
        try:
            file = open(self.filename, 'rb')
            new_cache = pickle.load(file)
            file.close()
            return new_cache
        except:
            return {}


def cache_daemon(cache: HideousCache):
    print('Daemon started')
    while True:
        time.sleep(10)
