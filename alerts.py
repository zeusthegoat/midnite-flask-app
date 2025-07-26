def check_alerts(history):
    alerts = []

    # 1100: single withdrawal > 100 
    if history[-1]["type"] == "withdrawal" and float(history[-1]["amount"]) > 100:
        alerts.append(1100)

    # 30: 3 consecutive withdrawals
    if len(history) >= 3 and all(X["type"] == "withdrawal" for X in history[-3:]):
        alerts.append(30)

    # 300: 3 increased deposits
    deposits = [float(X["amount"]) for X in history if X["type"] == "deposit"]
    if len(deposits) >= 3 and deposits[-1] > deposits[-2] > deposits[-3]:
        alerts.append(300)

    #123: deposits > £200 in last 30 seconds
    now = history[-1]["time"]
    recent_deposits = [
        float(X["amount"])
        for X in history
        if X["type"] == "deposit" and now - X["time"] <= 30
    ]
    if sum(recent_deposits) > 200:
        alerts.append(123)

    #500: deposit & withdrawal within 60 seconds (find if there's any deposit/withdrawal pair within a minute)
    deposits = [e for e in history if e["type"] == "deposit"]
    withdrawals = [e for e in history if e["type"] == "withdrawal"]
    deposit_withdrawal_within_minute = False 
    for d in deposits:
        for w in withdrawals:
            if d["user_id"] == w["user_id"] and d["time"] != w["time"] and abs(d["time"] - w["time"]) <= 60:
                deposit_withdrawal_within_minute = True
                break
        if deposit_withdrawal_within_minute:
            break 
    if deposit_withdrawal_within_minute:
        alerts.append(500)


    return len(alerts) > 0, alerts