# AppSec Contextual Triage (TriageGate) 🛡️

An automated, privacy-first AppSec triage pipeline designed to resolve CI/CD deployment bottlenecks. This tool analyzes vulnerability **reachability** (using static analysis principles) to safely auto-approve false-positives and non-exploitable SCA/CNAPP alerts without exposing sensitive code to the cloud.

---

## 🎯 The Problem (Business Bottleneck)
In mature DevSecOps environments (especially regulated sectors like Finance and Banking), security scanners (SCA, SAST, CNAPP) often block CI/CD pipelines due to high-severity vulnerabilities. 

However, **up to 70% of these alerts are non-exploitable contextually** (e.g., a vulnerable function in a library like `Pandas` or `Pickle` is imported, but the application code never actually invokes that specific function). This leads to:
* **Developer Fatigue:** Security teams are overwhelmed by "Allow List" or bypass requests.
* **Deployment Delays:** Pipelines stay blocked for days waiting for manual security reviews.
* **Cloud Privacy Fears:** Strict corporate governance often prohibits sending full source code to third-party Cloud LLMs for analysis.

## 🚀 The Solution (How it Works)
This project serves as a Proof of Concept (PoC) for an **Automated Reachability Filter**. Instead of blindly trusting or manually reviewing every scanner block, this pipeline uses lightweight, deterministic local analysis combined with a localized context check.

1. **SCA/CNAPP Trigger:** The pipeline simulates an alert blocking the build (e.g., `Pandas v1.5.3` with an RCE vulnerability in `read_pickle`).
2. **Reachability Analysis:** A local python script parses the application code (`app.py`) to verify if the vulnerable function/sink is actually present or reachable.
3. **Smart Verdict:** * If the function **is not** used, the pipeline auto-approves the Allow List request, logs the technical justification, and passes the build.
   * If the function **is** used, the build is hard-blocked with immediate feedback provided directly in the commit/Pull Request.

---

## 🏗️ Architecture & Privacy-First Design



This architecture is built strictly to comply with banking-grade security constraints:
* **Zero Cloud Exposure:** No code leaves the environment. The parsing happens entirely within the runner.
* **Deterministic & Scalable:** Uses fast abstract/pattern matching principles (similar to Semgrep/CodeQL logic) ensuring execution takes mere seconds.

---

## 💻 Quick Start & Testing Locally

### Prerequisites
* Python 3.10+
* Git

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/hel-isa/appsec-contextual-triage.git](https://github.com/hel-isa/appsec-contextual-triage.git)
   cd appsec-contextual-triage