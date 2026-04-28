def generate_cost_alerts(monthly_cost, forecasted_cost):
    alerts = []

    if monthly_cost >= 50:
        alerts.append({
            "level": "danger",
            "message": "High monthly cost detected. Review running AWS resources immediately."
        })
    elif monthly_cost >= 20:
        alerts.append({
            "level": "warning",
            "message": "Monthly cost is increasing. Monitor expensive services carefully."
        })

    if forecasted_cost >= 100:
        alerts.append({
            "level": "danger",
            "message": "Forecasted monthly cost is very high. Immediate optimization is recommended."
        })
    elif forecasted_cost >= 50:
        alerts.append({
            "level": "warning",
            "message": "Forecasted cost may exceed expected budget. Review usage trends."
        })

    if monthly_cost == 0:
        alerts.append({
            "level": "info",
            "message": "No AWS cost detected yet. Cost Explorer may need more billing data."
        })

    return alerts