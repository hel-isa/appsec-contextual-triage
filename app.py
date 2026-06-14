import pandas as pd

def process_financial_data():
    print("[*] Reading monthly financial report...")
    
    # The developer uses read_csv (COMPLETELY SAFE)
    df = pd.read_csv("fictitious_data.csv")
    
    # Performs a simple average operation
    average_expenses = df['expenses'].mean()
    print(f"[+] Average expenses processed: {average_expenses}")

if __name__ == "__main__":
    # Creating a fake CSV just so the script does not break if executed
    with open("fictitious_data.csv", "w") as f:
        f.write("month,expenses\njanuary,1500\nfebruary,2000")
        
    process_financial_data()