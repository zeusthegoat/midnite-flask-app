from typing import List, Dict, Tuple
from alerts.base import AlertRule

class HighDepositVolume(AlertRule):
    def check(self, history: List[Dict]) -> Tuple[bool, int]:
        now = history[-1]["time"]
        recent = [float(x["amount"]) for x in history if x["type"] == "deposit" and now - x["time"] <= 30]
        if sum(recent) > 200:
            return True, 123
        return False, -1
