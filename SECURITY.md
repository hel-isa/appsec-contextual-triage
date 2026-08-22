# Security Policy

## Reporting a Vulnerability

Please report security vulnerabilities privately through [GitHub's private vulnerability reporting](https://github.com/hel-isa/appsec-contextual-triage/security/advisories/new) for this repository (Security tab → "Report a vulnerability"). Do not open a public issue for security reports.

You should expect an initial response within a few days. If the issue is confirmed, a fix will be developed and coordinated before any public disclosure.

## Scope

This repository is a proof-of-concept demonstrating a triage pipeline design. The `pandas==1.5.3` dependency and the `pd.read_pickle` sink referenced throughout the code and docs are an intentional, fixed demo scenario used to exercise the triage logic — they are not a live vulnerability report about this project and should not be reported as one. Security reports about the triage scripts, CI workflows, or the local-LLM audit layer's fail-secure behavior are in scope.

## Supported Versions

This is a demo project without versioned releases; only the `main` branch is supported.
