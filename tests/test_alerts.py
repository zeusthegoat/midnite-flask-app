import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from alerts.alert_1100_single_large_withdrawal import SingleLargeWithdrawal
from alerts.alert_30_three_consecutive_withdrawals import ThreeWithdrawals
from alerts.alert_300_increasing_deposits import IncreasingDeposits

def test_single_large_withdrawal():
    rule = SingleLargeWithdrawal()
    history = [
        {"type": "withdrawal", "amount": "150", "time": 1000}
    ]
    result, code = rule.check(history)
    assert result is True
    assert code == 1100

def test_three_consecutive_withdrawals():
    rule = ThreeWithdrawals()
    history = [
        {"type": "withdrawal", "amount": "50", "time": 100},
        {"type": "withdrawal", "amount": "30", "time": 110},
        {"type": "withdrawal", "amount": "70", "time": 120},
    ]
    result, code = rule.check(history)
    assert result is True
    assert code == 30

def test_increasing_deposits():
    rule = IncreasingDeposits()
    history = [
        {"type": "deposit", "amount": "10", "time": 10},
        {"type": "deposit", "amount": "20", "time": 20},
        {"type": "deposit", "amount": "30", "time": 30},
    ]
    result, code = rule.check(history)
    assert result is True
    assert code == 300
