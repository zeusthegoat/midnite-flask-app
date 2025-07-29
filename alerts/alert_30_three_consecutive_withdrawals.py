from typing import List, Dict, Tuple
from alerts.base import AlertRule

class ThreeWithdrawals(AlertRule):
    def check(self, history: List[Dict]) -> Tuple[bool, int]:
        if len(history) >= 3 and all(x["type"] == "withdrawal" for x in history[-3:]):
            return True, 30
        return False, -1
