# nimble_plant

Batch classifier for plant operations text using **Nimble** via local Ollama (`/v1/systemone`).

Edit questions and records in the control workbook, run the classifier, and results are written back into the **same** workbook as `output_*` sheets. A JSONL file next to the workbook supports resume if a run is interrupted.

**Repo:** https://github.com/ranga291257/nimble_plant (public)  
**Stable snapshot (shared link / original workflow):** tag [`v0.1.0`](https://github.com/ranga291257/nimble_plant/tree/v0.1.0)

| Ref | What it is |
|---|---|
| [`main`](https://github.com/ranga291257/nimble_plant/tree/main) / [`v0.1.0`](https://github.com/ranga291257/nimble_plant/tree/v0.1.0) | Original shared Nimble / Ollama workflow (this README) |
| [`v1.0-dev`](https://github.com/ranga291257/nimble_plant/tree/v1.0-dev) | **Under development** — one workbook, choose Nimble or Jev, keep both outputs for compare |
| [`experiment/jev-compare`](https://github.com/ranga291257/nimble_plant/tree/experiment/jev-compare) | Earlier Jev experiment (superseded by v1.0-dev) |

People with the shared repo link keep this Nimble flow on `main`. The frozen tag `v0.1.0` remains available even after a future v1.0 release.

## Setup

```bash
git clone https://github.com/ranga291257/nimble_plant.git
cd nimble_plant
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
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
