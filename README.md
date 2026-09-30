# nimble_plant

Classify plant **statements** (pumps, exchangers, columns, …) into structured answers.

**Engines (same workbook):**

| Engine | Where | Command |
|---|---|---|
| **Nimble** | Local Ollama | `--engine nimble` |
| **Jev** | TypeSafe cloud | `--engine jev` (needs `TYPESAFE_API_KEY`) |

Edit questions and records in Excel. Run from the terminal. Each engine writes its own result sheets; when both have run, `output_compare` appears.

> Branch **`v1.0-dev`**. Older Nimble-only snapshot: tag [`v0.1.0`](https://github.com/ranga291257/nimble_plant/tree/v0.1.0).

---

## How questions work (keep it simple)

1. **`Records.text`** — the statement to classify.
2. **Common questions** — leave `Questions.equipment_type` blank (asked for every asset): failure mode, containment, load, urgency, impact, potential impact.
3. **Unit-op questions** — set `equipment_type` (only that class): e.g. cross-contamination (heat exchanger), off-spec / stability (column).
4. **Three answer types only:**
   - **choice** — pick one label from Labels  
   - **noul** — yes/no  
   - **score** — ordered scale from Labels (not a free 1–10; levels are the label rows, usually 3)

Labels may set `equipment_type` so **choices differ by class** under the same common question (e.g. failure mode: seal vs fouling vs flooding).

More detail / UML: [`docs/functional-spec.md`](docs/functional-spec.md).

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

**Nimble:** Ollama ≥ 0.35, then `ollama pull nimble`  
**Jev:** `export TYPESAFE_API_KEY=...` ([keys](https://console.typesafe.ai/keys))

---

## Workbook

[`nimble_classifier_workbook.xlsx`](nimble_classifier_workbook.xlsx) — open in LibreOffice/Excel; **close it before running**.

| Sheet | Role |
|---|---|
| Config | Defaults (engine, timeouts, test size) |
| Questions | What to ask (common vs unit-op; type choice/noul/score) |
| Labels | Options / score levels (optional equipment filter) |
| Records | Statements (`text`) + optional `expected_*` |
| Lists | Equipment types for dropdowns |
| `output_nimble_*` / `output_jev_*` | Results (one row per answer), Raw, Summary, Run_info |
| `output_compare` | Side-by-side when both engines have Results |

---

## Run

```bash
python nimble_runner.py nimble_classifier_workbook.xlsx --validate-only

python nimble_runner.py nimble_classifier_workbook.xlsx --engine nimble --test
python nimble_runner.py nimble_classifier_workbook.xlsx --engine nimble

export TYPESAFE_API_KEY=...
python nimble_runner.py nimble_classifier_workbook.xlsx --engine jev --test
```

`--test` = first N records (`Config.test_first_n`).  
`--engine` overrides Config. Checkpoints are `*.jsonl` (gitignored).

## Security

Use `TYPESAFE_API_KEY` in the environment. Leave Config `api_key` blank. Never commit keys.
