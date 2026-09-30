# nimble_plant (v1.0-dev)

Batch classifier for plant-operations text. One control workbook; choose **Nimble** (local Ollama) or **Jev** (TypeSafe). Each run writes `output_<engine>_*` sheets and never clears the other engine. When both Results sheets exist, `output_compare` is refreshed.

| Ref | Role |
|---|---|
| [`v1.0-dev`](https://github.com/ranga291257/nimble_plant/tree/v1.0-dev) (this branch) | Unified two-engine workflow — **under development** |
| [`v0.1.0`](https://github.com/ranga291257/nimble_plant/tree/v0.1.0) / [`main`](https://github.com/ranga291257/nimble_plant/tree/main) | Stable Nimble-only original |

## Documentation

| Doc | Audience |
|---|---|
| This README | Quick start |
| [`docs/functional-spec.md`](docs/functional-spec.md) | As-built functional spec + UML |
| Workbook **Read Me** sheet | In-Excel editing rules |
| [`experiments/README.md`](experiments/README.md) | Archived dual-workbook experiment |

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
| `nimble` | Ollama ≥ 0.35; `ollama pull nimble` |
| `jev` | `export TYPESAFE_API_KEY=...` ([keys](https://console.typesafe.ai/keys)) |

## Workbook

[`nimble_classifier_workbook.xlsx`](nimble_classifier_workbook.xlsx) — open in LibreOffice or Excel (close it before running).

| Sheet | Purpose |
|---|---|
| Config | `engine` (`nimble`\|`jev`), timeouts, review threshold; preset overrides model/URL |
| Questions | `choice` / `noul` / `score` by equipment type |
| Labels | Options for choice and score |
| Records | Text to classify (+ optional `expected_*`) |
| Lists | Equipment-type dropdown values |
| `output_nimble_*` | Results, Raw, Summary, Run_info (Nimble) |
| `output_jev_*` | Results, Raw, Summary, Run_info (Jev) |
| `output_compare` | Side-by-side answers when both Results exist |

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

# Resume (after interrupt)
python nimble_runner.py nimble_classifier_workbook.xlsx --engine nimble --resume nimble_classifier_workbook_nimble_YYYYMMDD_HHMMSS.jsonl
```

- CLI `--engine` overrides Config `engine`.
- Each run clears only that engine’s `output_<engine>_*` (and any legacy unprefixed `output_*`).
- Checkpoints: `<workbook>_<engine>_<timestamp>.jsonl` (gitignored).

## Compare

Run both engines on the same workbook, then open `output_compare` (disagreements highlighted).

## Security

Use `TYPESAFE_API_KEY` in the environment. Leave Config `api_key` blank. Never commit keys or `.env`.
