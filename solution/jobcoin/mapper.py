from typing import Dict
from typing import List
import json
import threading;

class SingletonMap:
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        self.map = {}
        
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            # another thread could have created the instance
            # before we acquired the lock. So check that the
            # instance is still nonexistent.
            if not cls._instance:
                cls._instance = super(SingletonMap, cls).__new__(cls)

        return cls._instance
    
    def getKeys(self):
        # force copying keys
        return list(self.map.keys())
    
    def get(self, key: str) -> List[str]:
        return self.map[key]
    
    def containsKey(self, key: str) -> bool:
        return key in self.map
    
    def remove(self, key: str) -> None:
        del self.map[key]
        
    def put(self, key: str, mapping) -> None:
        self.map[key] = mapping
        
    def echo(self):
        print(json.dumps(self.map))