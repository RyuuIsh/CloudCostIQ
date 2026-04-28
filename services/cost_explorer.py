import boto3
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

ce = boto3.client(
    "ce",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "ap-south-1")
)


def get_monthly_cost():
    today = datetime.today()
    start = today.replace(day=1).strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")

    response = ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"]
    )

    amount = response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
    return round(float(amount), 2)


def get_daily_costs():
    today = datetime.today()
    start = today.replace(day=1).strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")

    response = ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="DAILY",
        Metrics=["UnblendedCost"]
    )

    daily_data = []

    for item in response["ResultsByTime"]:
        date = item["TimePeriod"]["Start"]
        amount = item["Total"]["UnblendedCost"]["Amount"]

        daily_data.append({
            "date": date,
            "cost": round(float(amount), 2)
        })

    return daily_data


def get_service_costs():
    today = datetime.today()
    start = today.replace(day=1).strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")

    response = ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[
            {
                "Type": "DIMENSION",
                "Key": "SERVICE"
            }
        ]
    )

    service_data = []

    for group in response["ResultsByTime"][0]["Groups"]:
        service_name = group["Keys"][0]
        amount = group["Metrics"]["UnblendedCost"]["Amount"]

        cost = round(float(amount), 2)

        if cost > 0:
            service_data.append({
                "service": service_name,
                "cost": cost
            })

    service_data = sorted(service_data, key=lambda x: x["cost"], reverse=True)

    return service_data

def get_forecasted_monthly_cost():
    try:
        today = datetime.today()

        start = today.strftime("%Y-%m-%d")
        end = (today + timedelta(days=30)).strftime("%Y-%m-%d")

        response = ce.get_cost_forecast(
            TimePeriod={
                "Start": start,
                "End": end
            },
            Metric="UNBLENDED_COST",
            Granularity="MONTHLY"
        )

        amount = response["Total"]["Amount"]
        return round(float(amount), 2)

    except Exception:
        daily_costs = get_daily_costs()

        if not daily_costs:
            return 0

        total_cost = sum(item["cost"] for item in daily_costs)
        days_passed = len(daily_costs)

        average_daily_cost = total_cost / days_passed
        forecasted_cost = average_daily_cost * 30

        return round(forecasted_cost, 2)