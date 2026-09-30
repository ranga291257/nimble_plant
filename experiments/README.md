# Archived Jev experiment

The dual-workbook Jev side-by-side lived on branch `experiment/jev-compare`.

**v1.0-dev** unifies both engines in one workbook:

```bash
python nimble_runner.py nimble_classifier_workbook.xlsx --engine nimble --test
python nimble_runner.py nimble_classifier_workbook.xlsx --engine jev --test
```

Results land in `output_nimble_*` / `output_jev_*`; `output_compare` appears when both exist.

The previous Jev-only workbook is kept under [`archive/jev_classifier_workbook.xlsx`](archive/jev_classifier_workbook.xlsx) for reference only.
