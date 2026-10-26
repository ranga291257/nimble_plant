# nimble_plant

Classify plant **statements** (pumps, exchangers, columns, …) into structured answers.

**Engines (same workbook):**

| Engine | Where | Command |
|---|---|---|
| **Nimble** | Local Ollama | `--engine nimble` |
| **Jev** | TypeSafe cloud | `--engine jev` (needs `TYPESAFE_API_KEY`) |
| **JevK5** | Local [JevK5](https://huggingface.co/alibiserikbay/JevK5) runtime | `--engine jevk5` |

Edit questions and records in Excel. Run from the terminal. Each engine writes its own result sheets; when two or more have run, `output_compare` appears.

> Branch **`v1.0-dev`**. Older Nimble-only snapshot: tag [`v0.1.0`](https://github.com/ranga291257/nimble_plant/tree/v0.1.0).

---

## How questions work (keep it simple)

1. **`Records.statement`** — the statement to classify.
2. **Common questions** — leave `Questions.equipment_type` blank (asked for every asset): failure mode, containment, load, urgency, impact, potential impact.
3. **Unit-op questions** — set `equipment_type` (only that class): e.g. cross-contamination (heat exchanger), off-spec / stability (column).
4. **Three answer types only:**
   - **choice** — pick one label from Labels  
   - **noul** — yes/no  
   - **score** — ordered scale from Labels (not a free 1–10; levels are the label rows, usually 3)

Labels may set `equipment_type` so **choices differ by class** under the same common question (e.g. failure mode: seal vs fouling vs flooding).

More detail: [`docs/functional-spec.md`](docs/functional-spec.md).  
Ops use cases: [`operations_maintenance_use_cases.md`](operations_maintenance_use_cases.md).

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
**JevK5:** needs `/v1/systemone` on `:8090`. On an 8 GB GPU use the **GGUF** path (bf16 needs ~9 GB and will OOM):

```bash
# one-time: runtime (stdlib only) + download Q5 GGUF (~3 GB)
python3 -m venv .venv-jevk5
.venv-jevk5/bin/pip install --no-deps "jevk5 @ git+https://github.com/allebee/jevk5@v0.3.3"
.venv-jevk5/bin/pip install huggingface-hub
.venv-jevk5/bin/python -c "from huggingface_hub import hf_hub_download; hf_hub_download('alibiserikbay/JevK5-GGUF','jevk5-4b-v0.3-Q5_K_M.gguf', local_dir='models/JevK5-GGUF')"

# terminal 1 — llama.cpp backend (unload Ollama models first if VRAM is tight)
ollama stop nimble   # optional, frees GPU
/usr/lib/ollama/llama-server -m models/JevK5-GGUF/jevk5-4b-v0.3-Q5_K_M.gguf -c 8192 -ngl 99 --host 127.0.0.1 --port 8080

# terminal 2 — /v1/systemone wrapper for nimble_runner
.venv-jevk5/bin/python scripts/jevk5_gguf_serve.py --port 8090
```

On ≥16 GB VRAM you can instead `pip install "jevk5 @ git+https://github.com/allebee/jevk5@v0.3.3"` and run `jevk5-serve --model alibiserikbay/JevK5 --port 8090` (not chat/vLLM).
---

## Workbook

[`nimble_classifier_workbook.xlsx`](nimble_classifier_workbook.xlsx) — open in LibreOffice/Excel; **close it before running**.

| Sheet | Role |
|---|---|
| Config | Defaults (engine, timeouts, test size) |
| Questions | What to ask (common vs unit-op; type choice/noul/score) |
| Labels | Options / score levels (optional equipment filter) |
| Records | Statements (`statement`) + equipment + tag |
| `output_<engine>_*` | Results (one row per answer), Raw, Summary, Run_info |
| `output_compare` | Side-by-side when two or more engines have Results |

---

## Run

```bash
python nimble_runner.py nimble_classifier_workbook.xlsx --validate-only

python nimble_runner.py nimble_classifier_workbook.xlsx --engine nimble --test
python nimble_runner.py nimble_classifier_workbook.xlsx --engine nimble

export TYPESAFE_API_KEY=...
python nimble_runner.py nimble_classifier_workbook.xlsx --engine jev --test

# with jevk5-serve running on :8090
python nimble_runner.py nimble_classifier_workbook.xlsx --engine jevk5 --test
```

`--test` = first N records (`Config.test_first_n`).  
`--engine` overrides Config. Checkpoints are `*.jsonl` (gitignored).

## Security

Use `TYPESAFE_API_KEY` in the environment for cloud Jev. Leave Config `api_key` blank. Never commit keys. JevK5 and Nimble need no cloud key.
