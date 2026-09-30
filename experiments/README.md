# Jev experiment (branch `experiment/jev-compare`)

This folder compares **TypeSafe Jev** (hosted) to the working **Nimble** (local Ollama) setup. The default workbook [`../nimble_classifier_workbook.xlsx`](../nimble_classifier_workbook.xlsx) stays pointed at local Nimble.

| Model | Where it runs | Config |
|---|---|---|
| Nimble (default on `main`) | Local Ollama `/v1/systemone` | `model=nimble`, `base_url=http://localhost:11434` |
| Jev (this experiment) | TypeSafe cloud | `model=jev-1.13.0`, `base_url=https://api.typesafe.ai` |
| tev1 (optional local A/B) | Local Ollama | Same as Nimble but `model=tev1` after `ollama pull tev1` |

Jev is **not** `ollama pull jev`. Ollama’s “Jev-style” API is the protocol; Nimble/Tev1 are the local models.

## TypeSafe API key

1. Sign in at https://console.typesafe.ai (new signups may be paused).
2. Create a key at https://console.typesafe.ai/keys
3. Export it (never commit the key into Excel or git):

```bash
export TYPESAFE_API_KEY="sk-..."   # or apikey_...
```

## Run Jev test

From the repo root, on branch `experiment/jev-compare`:

```bash
git checkout experiment/jev-compare
source .venv/bin/activate          # Windows: .venv\Scripts\activate
export TYPESAFE_API_KEY=...       # required for hosted Jev
python nimble_runner.py experiments/jev_classifier_workbook.xlsx --test
```

Results are written as `output_*` sheets in [`jev_classifier_workbook.xlsx`](jev_classifier_workbook.xlsx):

- `output_Results` — answers / confidence / review flags
- `output_Raw` — per-record `usage_json` (input/output tokens) and raw answers
- `output_Summary` — accuracy stats when `expected_*` is filled
- `output_Run_info` — includes `input_tokens`, `output_tokens`, `total_tokens`

## Compare to Nimble

```bash
python nimble_runner.py nimble_classifier_workbook.xlsx --test
```

Compare each workbook’s `output_Summary` (accuracy needs `expected_*` columns).

## Security

- Prefer `TYPESAFE_API_KEY` env over Config `api_key` (leave the sheet blank).
- If a key was pasted into chat or a ticket, rotate it in the TypeSafe console.
