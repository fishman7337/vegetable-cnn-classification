# Dataset Documentation

## Expected Layout

The project expects the assessment dataset to be supplied locally and kept out of git:

```text
data/raw/Dataset (A)/
  train/<class_name>/*.jpg
  validation/<class_name>/*.jpg
  test/<class_name>/*.jpg
```

Set `DATASET_DIR` in `.env` if the dataset is stored elsewhere.

## Image Inputs

The original notebook compares:

- 23px by 23px grayscale inputs
- 101px by 101px grayscale inputs
- non-augmented training data
- augmented training data

The reusable CLI defaults to 101px grayscale because the notebook discussion reports stronger performance from the higher-resolution experiments.

## Known Data Quality Notes

The original notebook documents several dataset corrections:

- mislabeled carrot images inside a beans folder
- validation class naming inconsistencies, such as `with` versus `and`
- testing class naming and labeling inconsistencies

The package includes dry-run helpers for renaming class folders and moving known mislabeled files:

```python
from vegetable_vision.data import apply_folder_renames, move_matching_files
```

Keep these operations explicit and review the dry-run output before modifying dataset folders.

## Data Versioning

Image datasets are intentionally ignored by git. Recommended options:

- Store raw data in a controlled school/project drive.
- Track checksums for submitted dataset archives.
- Use DVC, MLflow artifacts, or cloud object storage if the project becomes collaborative.
- Record dataset changes in `reports/` or experiment logs.

## Privacy and Licensing

Only use datasets you are permitted to store and process. Do not commit images, student data, credentials, or personally identifiable information to this repository.
