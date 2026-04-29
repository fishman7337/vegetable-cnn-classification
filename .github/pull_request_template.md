## Summary

- 

## Validation

- [ ] `ruff format --check src tests scripts`
- [ ] `ruff check src tests scripts`
- [ ] `pytest --cov=vegetable_vision --cov-report=term-missing`
- [ ] `bandit -q -r src scripts`
- [ ] `pip-audit -r requirements-dev.txt --skip-editable --progress-spinner off`
- [ ] `pip-audit -r requirements.txt --skip-editable --progress-spinner off`
- [ ] `python scripts/split_notebook.py --check`

## Notes

- 
