from flask import Flask, render_template, Response
from services.recommendations import generate_recommendations
from services.alerts import generate_cost_alerts
from services.spike_detector import detect_cost_spikes
from services.report_generator import generate_csv, generate_pdf
from services.cost_explorer import (
    get_monthly_cost,
    get_daily_costs,
    get_service_costs,
    get_forecasted_monthly_cost
)

app = Flask(__name__)


@app.route("/")
def dashboard():
    monthly_cost = get_monthly_cost()
    daily_costs = get_daily_costs()
    service_costs = get_service_costs()
    forecasted_cost = get_forecasted_monthly_cost()

    recommendations = generate_recommendations(service_costs)
    alerts = generate_cost_alerts(monthly_cost, forecasted_cost)
    spikes = detect_cost_spikes(daily_costs)

    return render_template(
        "dashboard.html",
        monthly_cost=monthly_cost,
        daily_costs=daily_costs,
        service_costs=service_costs,
        recommendations=recommendations,
        forecasted_cost=forecasted_cost,
        alerts=alerts,
        spikes=spikes
    )


@app.route("/export/csv")
def export_csv():
    service_costs = get_service_costs()
    csv_data = generate_csv(service_costs)

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=cloudcostiq_report.csv"}
    )


@app.route("/export/pdf")
def export_pdf():
    monthly_cost = get_monthly_cost()
    forecasted_cost = get_forecasted_monthly_cost()
    service_costs = get_service_costs()
    recommendations = generate_recommendations(service_costs)

    pdf = generate_pdf(monthly_cost, forecasted_cost, service_costs, recommendations)

    return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment;filename=cloudcostiq_report.pdf"}
    )


if __name__ == "__main__":
    app.run(debug=True)