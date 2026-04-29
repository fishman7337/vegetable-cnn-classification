# Security Policy

## Supported Scope

This repository is an academic machine learning project. Security maintenance focuses on:

- source code in `src/`
- CI workflows
- development tooling
- dependency hygiene
- secret handling guidance

Datasets and trained model artifacts are not committed to this repository.

## Reporting a Vulnerability

Report vulnerabilities privately to the repository owner. Include:

- affected file or workflow
- reproduction steps
- impact
- suggested remediation, if known

Do not publish exploit details in public issues before the owner has had time to respond.

## Secret Management

Never commit credentials, `.env`, dataset tokens, API keys, Google Drive tokens, or model registry secrets. Use environment variables or GitHub Actions secrets.

## Automated Checks

CI includes Bandit, pip-audit, and CodeQL. These checks reduce risk but do not replace manual review.
