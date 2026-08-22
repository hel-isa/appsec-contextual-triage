import pandas as pd

def process_financial_data():
    print("[*] Reading monthly financial report...")

    # The developer uses read_csv (COMPLETELY SAFE)
    df = pd.read_csv("fictitious_data.csv")

    # Performs a simple average operation
    average_expenses = df['expenses'].mean()
    print(f"[+] Average expenses processed: {average_expenses}")

def process_quarterly_export():
    print("[*] Reading quarterly export from the reporting system...")

    # New feature: another pandas entry point (COMPLETELY SAFE, no risky deserialization)
    df = pd.read_json("fictitious_quarterly.json")

    total = df['total'].sum()
    print(f"[+] Quarterly total processed: {total}")

if __name__ == "__main__":
    # Creating a fake CSV just so the script does not break if executed
    with open("fictitious_data.csv", "w") as f:
        f.write("month,expenses\njanuary,1500\nfebruary,2000")

    # Creating a fake JSON export for the new quarterly report feature
    with open("fictitious_quarterly.json", "w") as f:
        f.write('[{"quarter": "Q1", "total": 3500}, {"quarter": "Q2", "total": 4200}]')

    process_financial_data()
    process_quarterly_export()
