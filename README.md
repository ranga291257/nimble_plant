# nimble_plant

This tool classifies plant-operations text (pumps, exchangers, columns, and so on) into structured answers.

**It supports two engines in the same workbook:**

| Engine | What it is | How you run it |
|---|---|---|
| **Nimble** | Local decision model through Ollama on your machine | `--engine nimble` |
| **Jev** | Hosted decision model on TypeSafe’s cloud | `--engine jev` (needs an API key) |

You edit questions and records once. You run Nimble, or Jev, or both. Each engine writes its **own** result sheets. If both have been run, the workbook also gets a side-by-side **compare** sheet.

You start runs from the terminal with Python (not from a button inside Excel).

> This branch is **`v1.0-dev`** (Nimble + Jev). The older Nimble-only snapshot is tag [`v0.1.0`](https://github.com/ranga291257/nimble_plant/tree/v0.1.0).

---

## Setup

```bash
git clone https://github.com/ranga291257/nimble_plant.git
cd nimble_plant
git checkout v1.0-dev
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### If you use Nimble (local)

1. Install and start [Ollama](https://ollama.com) **0.35 or later**.
2. Pull the model:

```bash
ollama pull nimble
```

### If you use Jev (hosted)

1. Create a key at [TypeSafe console](https://console.typesafe.ai/keys).
2. Put it in your environment (do **not** put it in the Excel file or in git):

```bash
export TYPESAFE_API_KEY=...
```

You can use one engine or both. Same setup steps either way; only the engine you call needs to be available.

---

## The workbook

Open [`nimble_classifier_workbook.xlsx`](nimble_classifier_workbook.xlsx) in **LibreOffice or Excel**.  
Close the file before you run the classifier (otherwise the file may be locked).

### Sheets you edit

| Sheet | Purpose |
|---|---|
| Config | Default engine, timeouts, review threshold, test size |
| Questions | What to ask (`choice`, `noul` yes/no, or `score`) |
| Labels | Answer options for choice and score questions |
| Records | The text to classify (optional `expected_*` columns for checking accuracy) |
| Lists | Dropdown values (equipment types) |

### Sheets the runner writes

| Sheet | Purpose |
|---|---|
| `output_nimble_*` | Results (one row per answer for that asset only) / Raw / Summary / Run_info |
| `output_jev_*` | Same from a **Jev** run |
| `output_compare` | Nimble vs Jev answers (created when **both** Results sheets exist) |

Shared reliability questions (Failure mode, Containment, Urgency, Impact) apply to all equipment; Labels may list different choices per equipment class. Only asset-specific phenomena (e.g. Cross-contamination on exchangers) set Questions.equipment_type. Results are long-format: `title` + `question_id` + answer.

A Nimble run does **not** delete Jev results, and a Jev run does **not** delete Nimble results.

Editing tips for the sheets are on the workbook’s own **Read Me** tab.  
Detailed behavior and UML: [`docs/functional-spec.md`](docs/functional-spec.md).

---

## How to run

From the repo folder, with the venv activated:

```bash
# Check the workbook (no model calls)
python nimble_runner.py nimble_classifier_workbook.xlsx --validate-only
```

### Run Nimble

```bash
python nimble_runner.py nimble_classifier_workbook.xlsx --engine nimble --test
python nimble_runner.py nimble_classifier_workbook.xlsx --engine nimble
```

### Run Jev

```bash
export TYPESAFE_API_KEY=...
python nimble_runner.py nimble_classifier_workbook.xlsx --engine jev --test
python nimble_runner.py nimble_classifier_workbook.xlsx --engine jev
```

### Useful flags

| Flag | Meaning |
|---|---|
| `--engine nimble` or `--engine jev` | Which engine to use (overrides Config) |
| `--test` | Only the first N records (`N` = Config `test_first_n`) |
| `--validate-only` | Check the workbook, then exit |
| `--resume <file.jsonl>` | Continue an interrupted run |

Checkpoints look like `nimble_classifier_workbook_nimble_YYYYMMDD_HHMMSS.jsonl` (gitignored).

---

## Compare Nimble and Jev

1. Run Nimble on the workbook.  
2. Run Jev on the **same** workbook.  
3. Open the `output_compare` sheet.

Rows where the two engines disagree are highlighted.

---

## Security

- Prefer `TYPESAFE_API_KEY` in the environment.
- Leave Config `api_key` blank.
- Never commit keys or a `.env` file.
