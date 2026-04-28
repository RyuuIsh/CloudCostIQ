import csv
from io import StringIO, BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet


def generate_csv(service_costs):
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["Service", "Cost ($)"])

    for item in service_costs:
        writer.writerow([item["service"], item["cost"]])

    return output.getvalue()


def generate_pdf(monthly_cost, forecasted_cost, service_costs, recommendations):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    # Title
    elements.append(Paragraph("CloudCostIQ Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Summary
    elements.append(Paragraph(f"Month-to-Date Cost: ${monthly_cost}", styles["Normal"]))
    elements.append(Paragraph(f"Forecasted Cost: ${forecasted_cost}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Table Data
    data = [["Service", "Cost ($)"]]
    for item in service_costs:
        data.append([item["service"], str(item["cost"])])

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Recommendations
    elements.append(Paragraph("Optimization Suggestions", styles["Heading2"]))

    for rec in recommendations:
        elements.append(Paragraph(f"- {rec}", styles["Normal"]))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    return pdf