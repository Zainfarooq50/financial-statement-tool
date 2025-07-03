# app.py
from flask import Flask, render_template, request
import pandas as pd
from financial_logic import (
    generate_income_statement,
    generate_balance_sheet,
    generate_kpis,
    group_by_period
)
from ai_summary import generate_ai_summary_and_risks

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_csv(file, parse_dates=["Date"])
            df['Date'] = pd.to_datetime(df['Date'])

            income_stmt = generate_income_statement(df)
            balance_sheet = generate_balance_sheet(df)
            kpi_table = generate_kpis(df)
            monthly_grouped = group_by_period(df)

            ai_summary, ai_risks = generate_ai_summary_and_risks(df)

            result = {
                "income": income_stmt.to_html(classes='table table-bordered'),
                "balance": balance_sheet.to_html(classes='table table-bordered'),
                "kpis": kpi_table.to_html(classes='table table-bordered'),
                "monthly": monthly_grouped.to_html(classes='table table-bordered'),
                "summary": ai_summary,
                "risks": ai_risks
            }

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
