import sys
from pathlib import Path

# Make the repo-root shared module importable regardless of current directory
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from triage_core import CRITICAL_FUNCTION, get_verdict  # noqa: E402


def evaluate_pandas_context() -> None:
    target_file = REPO_ROOT / "phase1-deterministic" / "app.py"

    print(f"[*] SCA ALERT: Pandas v1.5.3 flagged for a vulnerability in '{CRITICAL_FUNCTION}'.")
    print(f"[*] Starting reachability check on: {target_file} ...")

    if not target_file.exists():
        print("[!] Error: source code not found for analysis.")
        sys.exit(1)

    verdict = get_verdict(target_file.read_text())

    if verdict == "BLOCK":
        print(f"\n[CRITICAL] Block maintained - the code directly uses 'pd.{CRITICAL_FUNCTION}'.")
        print("[-] Remote Code Execution (RCE) risk. Allow-list REJECTED.")
        sys.exit(1)

    print(f"\n[INFO] Pandas is imported, but '{CRITICAL_FUNCTION}' is not used.")
    print("[+] Context: only safe functions (e.g. read_csv) are called.")
    print("[+] Assessment: vulnerability not reachable in the current context.")
    print("[+] Allow-list request APPROVED.")
    sys.exit(0)


if __name__ == "__main__":
    evaluate_pandas_context()
