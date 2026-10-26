#!/usr/bin/env python3
"""TypeSafe-style /v1/systemone front-end for JevK5 GGUF (fits 8 GB GPUs).

Requires a running llama-server with a JevK5 GGUF, e.g.:

  /usr/lib/ollama/llama-server \\
      --hf-repo alibiserikbay/JevK5-GGUF \\
      --hf-file jevk5-4b-v0.3-Q5_K_M.gguf \\
      -c 8192 -ngl 99 --port 8080

Then:

  .venv-jevk5/bin/python scripts/jevk5_gguf_serve.py --port 8090

nimble_runner --engine jevk5 talks to this process on :8090.
"""
from __future__ import annotations

import argparse
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from jevk5 import JevK5GGUF


def normalized(question: dict) -> dict:
    if question.get("type") not in ("noul", "choice", "score"):
        raise ValueError(f"unknown question type {question.get('type')!r}")
    if "instructions" not in question:
        raise ValueError("question is missing instructions")
    criteria = question.get("criteria")
    if question["type"] == "choice":
        if isinstance(criteria, list):
            criteria = dict.fromkeys(criteria)
        if not isinstance(criteria, dict) or len(criteria) < 2:
            raise ValueError("choice criteria must name at least two options")
    if question["type"] == "score" and (not isinstance(criteria, list) or len(criteria) < 2):
        raise ValueError("score criteria must list at least two levels")
    return {**question, "criteria": criteria}


def make_handler(model: JevK5GGUF, name: str):
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def _send(self, status: int, payload: dict) -> None:
            data = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self) -> None:
            path = self.path.rstrip("/")
            if path in ("/health", "/v1/models"):
                self._send(200, {"ok": True, "model": name})
            else:
                self._send(404, {"error": "not found"})

        def do_POST(self) -> None:
            if self.path.rstrip("/") != "/v1/systemone":
                self._send(404, {"error": "not found"})
                return
            started = time.perf_counter()
            try:
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
                with lock:
                    answers = {
                        qid: model.decide(body["state"], normalized(q))
                        for qid, q in body["questions"].items()
                    }
            except (ValueError, KeyError, TypeError) as error:
                self._send(400, {"error": str(error)})
                return
            tokens = sum(a.pop("input_tokens", 0) for a in answers.values())
            self._send(
                200,
                {
                    "model": body.get("model") or name,
                    "answers": answers,
                    "usage": {"input_tokens": tokens, "output_tokens": 0},
                    "latency_ms": round((time.perf_counter() - started) * 1e3, 2),
                },
            )

        def log_message(self, *args) -> None:
            pass

    return Handler


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--llama-url", default="http://127.0.0.1:8080",
                   help="running llama-server base URL")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8090)
    p.add_argument("--model-name", default="alibiserikbay/JevK5-GGUF")
    # v0.3 4B GGUF card values
    p.add_argument("--temperature", type=float, default=1.22)
    p.add_argument("--knockout-temperature", type=float, default=0.93)
    args = p.parse_args(argv)

    model = JevK5GGUF(
        url=args.llama_url,
        temperature=args.temperature,
        knockout_temperature=args.knockout_temperature,
    )
    server = ThreadingHTTPServer(
        (args.host, args.port), make_handler(model, args.model_name)
    )
    print(
        f"serving {args.model_name} (GGUF via {args.llama_url}) "
        f"on http://{args.host}:{args.port}/v1/systemone",
        flush=True,
    )
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
