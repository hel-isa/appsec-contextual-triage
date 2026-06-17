import sys
from pathlib import Path

# Make the repo-root shared module importable regardless of current directory
REPO_ROOT = Path(__file__).resolve().parents[1]
_repo_root = str(REPO_ROOT)
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

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
        print(f"\n[CRITICAL] Block maintained - '{CRITICAL_FUNCTION}' was found in the source file (string-based check).")
        print("[-] Remote Code Execution (RCE) risk. Allow-list REJECTED.")
        sys.exit(1)

    print(f"\n[INFO] '{CRITICAL_FUNCTION}' was not found in the source file.")
    print("[+] Context: string-based reachability check did not detect the sink.")
    print("[+] Assessment: vulnerability appears not reachable in the current context.")
    print("[+] Allow-list request APPROVED.")
    sys.exit(0)


if __name__ == "__main__":
    evaluate_pandas_context()
