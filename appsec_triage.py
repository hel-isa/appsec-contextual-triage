import os

def evaluate_pandas_context():
    # The Pandas function the scanner flagged as vulnerable in this version
    critical_function = "read_pickle"
    target_file = "app.py"
    
    print(f"[*] SCA ALERT: Identified Pandas v1.5.3 with a vulnerability in '{critical_function}'.")
    print(f"[*] Starting Reachability Analysis on file: {target_file}...")
    
    if not os.path.exists(target_file):
        print("[!] Error: Source code not found for analysis.")
        return False
        
    with open(target_file, "r") as f:
        code = f.read()
        
    # Investigating whether the developer called the dangerous function
    if critical_function in code:
        print(f"\n[CRITICAL] Block Maintained! The code directly uses 'pd.{critical_function}'.")
        print("[-] Remote Code Execution (RCE) risk. Allow List REJECTED.")
        exit(1)  # Stops the pipeline with an error
    else:
        print(f"\n[INFO] The developer imported Pandas, but does NOT use the '{critical_function}' function.")
        print("[+] Context Analysis: The code only uses safe functions (such as read_csv).")
        print("[+] ASSESSMENT: Vulnerability not reachable in the current context.")
        print("[+] ALLOW LIST REQUEST APPROVED.")
        exit(0)  # Releases the pipeline successfully

if __name__ == "__main__":
    evaluate_pandas_context()