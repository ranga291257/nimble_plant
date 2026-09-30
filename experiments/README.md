# Jev experiment (does not change `main`)

This folder compares **TypeSafe Jev** (hosted) to the working **Nimble** (local Ollama) setup without modifying [`nimble_classifier_workbook.xlsx`](../nimble_classifier_workbook.xlsx).

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
source .venv/bin/activate
export TYPESAFE_API_KEY=...   # required for hosted Jev
python nimble_runner.py experiments/jev_classifier_workbook.xlsx --test
```

Results are written as `output_*` sheets in `experiments/jev_classifier_workbook.xlsx`.

## Compare to Nimble

```bash
python nimble_runner.py nimble_classifier_workbook.xlsx --test
```

Compare each workbook’s `output_Summary` (accuracy needs `expected_*` columns).

## Security

- Prefer `TYPESAFE_API_KEY` env over Config `api_key`.
- If a key was pasted into chat or a ticket, rotate it in the TypeSafe console.
