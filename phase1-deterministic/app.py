import pandas as pd

def process_financial_data():
    print("[*] Reading monthly financial report...")

    # The developer uses read_csv (COMPLETELY SAFE)
    df = pd.read_csv("fictitious_data.csv")

    # Performs a simple average operation
    average_expenses = df['expenses'].mean()
    print(f"[+] Average expenses processed: {average_expenses}")

def load_cached_summary():
    print("[*] Loading cached quarterly summary for faster startup...")

    # Safe alternative: persist the cache as CSV instead of pickle,
    # avoiding the RCE sink flagged in pandas==1.5.3.
    cached_summary = pd.read_csv("cached_summary.csv")
    print(f"[+] Cached summary loaded: {cached_summary.to_dict()}")

if __name__ == "__main__":
    # Creating a fake CSV just so the script does not break if executed
    with open("fictitious_data.csv", "w") as f:
        f.write("month,expenses\njanuary,1500\nfebruary,2000")

    process_financial_data()

    # Seed a fake cache file so load_cached_summary() has something to read
    pd.DataFrame({"quarter": ["Q1"], "total": [3500]}).to_csv("cached_summary.csv", index=False)
    load_cached_summary()