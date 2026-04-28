def detect_cost_spikes(daily_costs):
    spikes = []

    if len(daily_costs) < 2:
        return spikes

    for i in range(1, len(daily_costs)):
        previous_day = daily_costs[i - 1]
        current_day = daily_costs[i]

        previous_cost = previous_day["cost"]
        current_cost = current_day["cost"]

        if previous_cost == 0:
            continue

        increase_percentage = ((current_cost - previous_cost) / previous_cost) * 100

        if current_cost >= previous_cost * 2 and current_cost >= 1:
            spikes.append({
                "date": current_day["date"],
                "previous_cost": previous_cost,
                "current_cost": current_cost,
                "increase_percentage": round(increase_percentage, 2),
                "message": f"Cost spike detected on {current_day['date']}: cost increased from ${previous_cost} to ${current_cost}."
            })

    return spikes