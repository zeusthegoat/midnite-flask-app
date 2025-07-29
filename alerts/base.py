from typing import List, Dict, Tuple 

class AlertRule:
    def check(self, history: List[Dict]) -> Tuple[bool, int]:
        raise NotImplementedError("Must implement check method")