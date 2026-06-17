import json
import os
from pathlib import Path

import requests


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1")


def get_local_verdict(source_code):
    if "read_pickle" in source_code:
        return "BLOCK"
    return "ALLOW"


def ask_local_llm(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"num_predict": 500},
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        content = data.get("response", "") or data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return json.loads(content) if content else {}
    except requests.exceptions.RequestException as e:
        print(f"[!] Error communicating with local LLM: {e}")
        return ""
    except json.JSONDecodeError as e:
        print(f"[!] Error parsing local LLM response: {e}")
        return {}


def print_audit_note(result):
    print("\n=== Local AppSec Audit Note ===")
    print(json.dumps(result, indent=4))
    print("================================\n")
    
def run_phase2_triage():
    repo_root = Path(__file__).resolve().parents[1]
    target_file = repo_root / "phase1-deterministic" / "app.py"
    vuln_context = "SCA Alert: Pandas version 1.5.3 contains a Critical RCE in pd.read_pickle()."

    print(f"[*] Phase 2: Local AppSec audit layer started with model '{MODEL_NAME}'.")

    if not target_file.exists():
        print(f"[!] Unable to continue: target file '{target_file}' was not found.")
        exit(1)

    with open(target_file, "r") as f:
        source_code = f.read()

    local_verdict = get_local_verdict(source_code)

    # The deterministic gate decides the final verdict.
    # The LLM is only used to generate a short audit note.
    prompt = f"""
    You are an AppSec assistant writing a short audit note.
    Do not change the decision. The local verdict is already set to: {local_verdict}.
    Explain whether the vulnerable sink is present in the code and keep the response concise.

    Vulnerability Context: {vuln_context}
    
    Application Source Code:
    ```python
    {source_code}
    ```
    Respond strictly in JSON format with the exact keys:
    {{
        "summary": "Short audit note",
        "technical_justification": "Why the local verdict makes sense",
        "confidence_score": 0-100
    }}
    """

    result = ask_local_llm(prompt)
    
    if result:
        print_audit_note(result)
        if local_verdict == "BLOCK":
            print("[-] Final decision: BLOCK. The deterministic check found a reachable sink.")
            exit(1)
        print("[+] Final decision: ALLOW. The deterministic check found no reachable sink.")
        exit(0)
    else:
        if local_verdict == "BLOCK":
            print("[-] Final decision: BLOCK. The deterministic check found a reachable sink.")
        else:
            print("[!] Final decision: BLOCK. The LLM audit layer is unavailable, so the build fails closed.")
        exit(1)

if __name__ == "__main__":
    run_phase2_triage()
