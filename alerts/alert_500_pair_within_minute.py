from typing import List, Dict, Tuple
from alerts.base import AlertRule

class DepositWithdrawalPair(AlertRule):
    def check(self, history: List[Dict]) -> Tuple[bool, int]:
        deposits = [e for e in history if e["type"] == "deposit"]
        withdrawals = [e for e in history if e["type"] == "withdrawal"]

        for d in deposits:
            for w in withdrawals:
                if d["user_id"] == w["user_id"] and d["time"] != w["time"] and abs(d["time"] - w["time"]) <= 60:
                    return True, 500
        return False, -1
