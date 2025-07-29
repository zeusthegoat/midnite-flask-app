from typing import List, Dict, Tuple
from alerts.base import AlertRule

class SingleLargeWithdrawal(AlertRule):
    def check(self, history: List[Dict]) -> Tuple[bool, int]:
        if history[-1]["type"] == "withdrawal" and float(history[-1]["amount"]) > 100:
            return True, 1100
        return False, -1