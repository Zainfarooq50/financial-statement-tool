# financial_logic.py
import pandas as pd

def generate_income_statement(df):
    revenue = df[df['Type'].str.lower() == 'revenue']['Amount'].sum()
    expense = df[df['Type'].str.lower() == 'expense']['Amount'].sum()
    net_income = revenue - expense
    return pd.DataFrame({
        'Category': ['Total Revenue', 'Total Expenses', 'Net Income'],
        'Amount': [revenue, expense, net_income]
    })

def generate_balance_sheet(df):
    assets = df[df['Type'].str.lower() == 'asset']['Amount'].sum()
    liabilities = df[df['Type'].str.lower() == 'liability']['Amount'].sum()
    equity = df[df['Type'].str.lower() == 'equity']['Amount'].sum()
    return pd.DataFrame({
        'Category': ['Total Assets', 'Total Liabilities', 'Total Equity', 'Difference (A - L - E)'],
        'Amount': [assets, liabilities, equity, assets - liabilities - equity]
    })

def generate_kpis(df):
    revenue = df[df['Type'].str.lower() == 'revenue']['Amount'].sum()
    expense = df[df['Type'].str.lower() == 'expense']['Amount'].sum()
    net_income = revenue - expense
    assets = df[df['Type'].str.lower() == 'asset']['Amount'].sum()
    liabilities = df[df['Type'].str.lower() == 'liability']['Amount'].sum()
    equity = df[df['Type'].str.lower() == 'equity']['Amount'].sum()

    kpis = {
        "Net Profit Margin": round((net_income / revenue) * 100, 2) if revenue else 0,
        "Current Ratio": round((assets / liabilities), 2) if liabilities else 0,
        "Debt-to-Equity Ratio": round((liabilities / equity), 2) if equity else 0
    }
    return pd.DataFrame(list(kpis.items()), columns=["KPI", "Value"])

def group_by_period(df):
    grouped = df[df['Type'].isin(['Revenue', 'Expense'])].copy()
    grouped['Month'] = df['Date'].dt.to_period('M').astype(str)
    summary = grouped.groupby(['Month', 'Type'])['Amount'].sum().unstack().fillna(0)
    summary['Net Income'] = summary.get('Revenue', 0) - summary.get('Expense', 0)
    return summary.reset_index()
