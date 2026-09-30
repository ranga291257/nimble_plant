# nimble_plant (v1.0-dev)

One control workbook, two engines: **Nimble** (local Ollama) or **Jev** (TypeSafe hosted). Each run writes **engine-prefixed** sheets and never clears the other engine. When both Results sheets exist, `output_compare` is refreshed.

**Stable original workflow:** tag [`v0.1.0`](https://github.com/ranga291257/nimble_plant/tree/v0.1.0) / branch [`main`](https://github.com/ranga291257/nimble_plant/tree/main)  
**This branch:** under development toward v1.0 — do not treat as release yet.

## Setup

```bash
git clone https://github.com/ranga291257/nimble_plant.git
cd nimble_plant
git checkout v1.0-dev
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

| Engine | Requirements |
|---|---|
| `nimble` | Ollama ≥ 0.35, `ollama pull nimble` |
| `jev` | `export TYPESAFE_API_KEY=...` ([console](https://console.typesafe.ai/keys)) |

## Workbook

[`nimble_classifier_workbook.xlsx`](nimble_classifier_workbook.xlsx)

| Sheet | Purpose |
|---|---|
| Config | `engine` (`nimble`\|`jev`), timeouts, review threshold (preset overrides model/URL) |
| Questions / Labels / Records | Same as before |
| `output_nimble_*` | Results / Raw / Summary / Run_info from Nimble |
| `output_jev_*` | Same from Jev |
| `output_compare` | Side-by-side answers when both Results sheets exist |

Open in LibreOffice or Excel (Cursor preview often fails on this file). Close the file before running.

## Run

```bash
python nimble_runner.py nimble_classifier_workbook.xlsx --validate-only

# Nimble (local)
python nimble_runner.py nimble_classifier_workbook.xlsx --engine nimble --test
python nimble_runner.py nimble_classifier_workbook.xlsx --engine nimble

# Jev (hosted)
export TYPESAFE_API_KEY=...
python nimble_runner.py nimble_classifier_workbook.xlsx --engine jev --test
python nimble_runner.py nimble_classifier_workbook.xlsx --engine jev
```

CLI `--engine` overrides Config `engine`. Each run clears only that engine’s `output_<engine>_*` sheets (and any legacy unprefixed `output_*`). JSONL checkpoints are named `<workbook>_<engine>_<timestamp>.jsonl`.

## Compare

After both engines have been run on the same workbook, open `output_compare` (disagreeing rows are highlighted).

## Security

Prefer `TYPESAFE_API_KEY` in the environment; leave Config `api_key` blank. Never commit keys.

## Specification

Full functional specification with UML (use cases, components, activity, sequences, sheet state): [`docs/functional-spec.md`](docs/functional-spec.md).
