from typing import List, Dict, Tuple
from alerts.alert_1100_single_large_withdrawal import SingleLargeWithdrawal
from alerts.alert_30_three_consecutive_withdrawals import ThreeWithdrawals
from alerts.alert_300_increasing_deposits import IncreasingDeposits
from alerts.alert_123_deposit_volume import HighDepositVolume
from alerts.alert_500_pair_within_minute import DepositWithdrawalPair

def check_alerts(history: List[Dict]) -> Tuple[bool, List[int]]:
    alert_rules = [
        SingleLargeWithdrawal(),
        ThreeWithdrawals(),
        IncreasingDeposits(),
        HighDepositVolume(),
        DepositWithdrawalPair()
    ]

    triggered = []
    for rule in alert_rules:
        is_triggered, code = rule.check(history)
        if is_triggered:
            triggered.append(code)

    return len(triggered) > 0, triggered
