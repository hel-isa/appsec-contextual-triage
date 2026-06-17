# AppSec Contextual Triage

Privacy-first proof of concept for automated AppSec triage in CI/CD.

The project shows how a pipeline can distinguish between a vulnerable package version and a truly reachable exploit path before deciding whether to block or allow a build.

## Why this exists

Security tooling (SCA, SAST, CNAPP) often blocks deployments based on vulnerable package versions even when the risky function is not used by the app.

This causes:
- security team overload with repetitive allow-list requests
- slower releases due to manual triage bottlenecks
- privacy concerns when source code is sent to external services

This repository demonstrates a local, auditable triage approach that can be integrated into GitHub Actions.

## Project story

The repo is built around one practical question: if a scanner flags a vulnerable dependency, can the application actually reach the risky function?

The demo answers that question with two layers:
- Phase 1: a deterministic gate that looks for direct risky usage
- Phase 2: a local LLM audit step that explains the deterministic verdict and fails closed when the model is unavailable

That makes the project useful for regulated environments where raw source code should stay local and security decisions need to be explainable.

## What this project does

The demo focuses on a known scenario:
- dependency: `pandas==1.5.3`
- vulnerable sink to check: `pd.read_pickle`

Triage behavior:
- if risky usage is found in the target code, pipeline fails
- if risky usage is not found, pipeline passes with a contextual justification

## Project structure

```text
.
|- .github/workflows/appsec-pipeline.yml
|- phase1-deterministic/
|  |- app.py
|  |- appsec_triage.py
|- phase2-local-llm/
|  |- appsec_llm_triage.py
|- requirements.txt
|- README.md
```

## Phase overview

### Phase 1: Deterministic triage

Script: `phase1-deterministic/appsec_triage.py`

How it works:
- reads target source code
- searches for usage of the critical function name (`read_pickle`)
- exits `1` on reachable risk, exits `0` otherwise

This gives a fast and explainable baseline gate.

### Phase 2: Local LLM triage (fail-secure design)

Script: `phase2-local-llm/appsec_llm_triage.py`

How it works:
- runs the deterministic verdict first
- sends vulnerability context plus source code to a local LLM endpoint for an audit note only
- blocks the pipeline if the model is unavailable and the build would otherwise be auto-approved

Goal: richer contextual reasoning while keeping the final decision local and auditable.

### Phase 2 runtime notes

- `localhost:11434` means the machine running the script, not your personal laptop when the job is in GitHub Actions.
- In GitHub-hosted Actions runners, a local LLM server is not available *unless* you start one (for example, the Phase 2 workflow in this repo starts an Ollama container when manually dispatched), or you point `OLLAMA_URL` to a reachable service.
- The `urllib3` warning about `LibreSSL` is separate from the LLM failure; it is an environment warning, not the reason the triage endpoint is unavailable.

## Local setup

### Prerequisites

- Python 3.10+
- Git

### Install

```bash
git clone https://github.com/hel-isa/appsec-contextual-triage.git
cd appsec-contextual-triage
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run locally

### Run Phase 1

```bash
cd phase1-deterministic
python appsec_triage.py
```

Expected behavior:
- returns success when `read_pickle` is not used
- returns error when `read_pickle` is detected

### Run Phase 2

```bash
cd ../phase2-local-llm
python appsec_llm_triage.py
```

Notes:
- if your local LLM endpoint is offline, the script intentionally fails closed
- this is by design to avoid accidental insecure bypasses

## GitHub Actions pipeline

Workflow file: `.github/workflows/appsec-pipeline.yml`

Current workflow runs:
- checkout
- Python setup
- dependency installation from `requirements.txt`
- Phase 1 deterministic check
- Phase 2 local-LLM audit on a GitHub-hosted runner when the workflow is manually dispatched

Phase 2 notes:
- the Phase 2 job is opt-in and starts an Ollama container inside the GitHub-hosted runner
- `localhost:11434` points to that runner container during the job, not to your personal machine
- if the workflow is only triggered by push or pull_request, the Phase 2 job is skipped

## Security and privacy posture

- local-first analysis path
- deterministic baseline for auditability
- fail-secure behavior when AI triage is unavailable
- minimal dependencies (`pandas` in this demo)

## Limitations

- current reachability check is string-based and intentionally simple
- no AST/dataflow analysis yet
- no centralized policy engine yet

## Roadmap

- AST-aware reachability analysis
- policy-as-code rules for waiver governance
- signed triage evidence artifacts for audit trails
- optional integration with CodeQL/Semgrep outputs

## License

No license file is included yet. Add a license before public reuse.