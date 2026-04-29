# Raw Data

Place the original assessment dataset here without committing image files.

Expected layout:

```text
data/raw/Dataset (A)/
  train/<class_name>/*.jpg
  validation/<class_name>/*.jpg
  test/<class_name>/*.jpg
```

The original notebook references `/content/DELE_CA1/Dataset (A)` for Google Colab. For local work, set `DATASET_DIR` in `.env` or pass `--data-dir` to the training CLI.
