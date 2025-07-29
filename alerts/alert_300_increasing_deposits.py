from typing import List, Dict, Tuple
from alerts.base import AlertRule

class IncreasingDeposits(AlertRule):
    def check(self, history: List[Dict]) -> Tuple[bool, int]:
        deposits = [float(x["amount"]) for x in history if x["type"] == "deposit"]
        if len(deposits) >= 3 and deposits[-1] > deposits[-2] > deposits[-3]:
            return True, 300
        return False, -1
