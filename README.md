# nimble_plant

Batch classifier for plant operations text using Nimble via Ollama (`/v1/systemone`).

Edit questions and records in the control workbook, run the classifier, and results are written back into the **same** workbook as `output_*` sheets. A JSONL file next to the workbook supports resume if a run is interrupted.

## Setup

```bash
cd /mnt/d/dev/nimble_plant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Requires **Ollama ≥ 0.35** running locally, with the Nimble model available:

```bash
ollama pull nimble
```

## Workbook

[`nimble_classifier_workbook.xlsx`](nimble_classifier_workbook.xlsx) has:

| Sheet | Purpose |
|---|---|
| Read Me | How to edit the control sheets |
| Config | model, URL, timeouts, review threshold |
| Questions | choice / noul (yes-no) / score questions by equipment type |
| Labels | answer options for choice and score questions |
| Records | text to classify (+ optional `expected_*` columns) |
| Lists | equipment-type dropdown values |
| output_Results | answers, confidence, review flags (written by runner) |
| output_Raw | raw model JSON per record |
| output_Summary | accuracy / confidence stats (accuracy needs `expected_*`) |
| output_Run_info | run metadata |

Example rows cover pumps, heat exchangers, and distillation columns. Replace them with your plant data.

Open the workbook in LibreOffice or Excel (Cursor’s built-in preview often fails on this file).

## Run

Close the workbook in Excel/LibreOffice before running (the file must not be locked).

```bash
# check workbook only
python nimble_runner.py nimble_classifier_workbook.xlsx --validate-only

# first N records (Config: test_first_n)
python nimble_runner.py nimble_classifier_workbook.xlsx --test

# full run
python nimble_runner.py nimble_classifier_workbook.xlsx

# resume an interrupted run
python nimble_runner.py nimble_classifier_workbook.xlsx --resume nimble_classifier_workbook_YYYYMMDD_HHMMSS.jsonl
```

Each run clears any existing `output_*` sheets first, then writes them again when finished. A `.jsonl` checkpoint is written beside the workbook for `--resume` only; override location with `--out-dir` if needed.
