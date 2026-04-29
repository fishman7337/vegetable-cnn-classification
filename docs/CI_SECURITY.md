# CI and Security

## GitHub Actions

The repository includes CI workflows for:

- linting and formatting with Ruff
- unit tests with pytest
- notebook split integrity checks
- static security scanning with Bandit
- dependency auditing with pip-audit
- CodeQL static analysis

## Dependabot

Dependabot is configured for:

- Python dependencies
- GitHub Actions versions

Review dependency updates before merging, especially TensorFlow and notebook tooling updates that can affect reproducibility.

## Secret Handling

Do not commit:

- `.env`
- API keys
- Google Drive credentials
- Kaggle credentials
- model registry tokens
- private dataset links

Use environment variables or GitHub Actions secrets.

## Security Reporting

Security reporting guidance is in `SECURITY.md`.
