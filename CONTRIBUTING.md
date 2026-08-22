# Contributing

Thanks for your interest in this project.

## Getting started

```bash
git clone https://github.com/hel-isa/appsec-contextual-triage.git
cd appsec-contextual-triage
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Making changes

1. Create a branch off `main` for your change.
2. Run the test suite before opening a PR:
   ```bash
   python -m unittest discover -s tests -v
   ```
3. Run `phase1-deterministic/appsec_triage.py` to confirm the deterministic gate still behaves as expected.
4. Open a pull request describing what changed and why. CI runs the test suite, a dependency audit (`pip-audit`), and the Phase 1 check on every push and pull request.

## Reporting bugs or proposing features

Use the issue templates under **Issues → New Issue**.

## Reporting security vulnerabilities

Do not open a public issue. See [SECURITY.md](SECURITY.md).

## Code of conduct

This project follows the [Code of Conduct](CODE_OF_CONDUCT.md).
