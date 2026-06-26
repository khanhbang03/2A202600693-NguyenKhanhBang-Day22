# Bonus Challenge: Vietnamese Python Tutor

## Audience

This bonus project targets Vietnamese first-year students or high-school students who are learning Python for the first time. The user is not trying to read a long CS textbook; they are usually stuck on a small exercise, a syntax error, or the difference between two concepts such as list index vs dictionary key. The product goal is a tutor that helps the student continue thinking instead of giving a final answer immediately.

## Domain Knowledge

The domain knowledge is Python 101 pedagogy. Beginners often copy a working solution without understanding the moving parts: which variable changes, where the loop stops, what the function returns, or why a condition is true. A useful tutor should force the problem into a tiny test case, ask for input/output expectations, and make the learner trace values. For Vietnamese students, the answer should stay in plain Vietnamese, introduce English terms only when they are the actual Python keywords, and avoid sounding like translated documentation.

## Application Objective

The aligned behavior is "scaffold first, solve later." For benign learning prompts, the model should:

- explain with a tiny example,
- ask one diagnostic question,
- suggest a next action such as adding `print()` or tracing `n = 0, 1, 2`,
- avoid dumping a complete homework solution,
- keep the language short enough for a student to act on.

The rejected behavior is a generic AI answer that gives the final pattern, mixes unnecessary English, or tells the student to memorize syntax.

## Real-World Output

This folder contains a reproducible mini portfolio piece:

- `data/generate_pairs.py` creates 200 preference pairs.
- `data/pairs.parquet` is the DPO-ready dataset after running the generator.
- `train.py` reuses the lab's `scripts/train_dpo.py` and writes `adapters/dpo-python-tutor/`.
- `demo/serve.py` is a one-file CLI demo. If `GGUF_PATH` is set, it uses `llama-cpp-python`; otherwise it shows the intended interaction contract with a deterministic fallback.
- `demo/5-samples.md` shows before/after style expectations.
- `MODEL-CARD.md` documents scope, non-goals, evaluation, and limitations.

## How To Run

```bash
python bonus/data/generate_pairs.py
python bonus/train.py
python bonus/demo/serve.py
```

For a GGUF-backed demo after NB5 export:

```bash
$env:GGUF_PATH = "gguf/lab22-dpo-Q4_K_M.gguf"
python bonus/demo/serve.py
```

## Why This Is A Good DPO Task

DPO is useful here because the difference is not simply "correct vs incorrect." Both chosen and rejected responses may mention valid Python syntax. The preference is about teaching behavior: whether the model preserves the student's agency, gives a next step, and avoids solving the exercise too early. That is exactly the kind of style and policy distinction preference learning can capture better than ordinary SFT.

## Honest Limitations

This is a v0 proof of concept. The 200 pairs are synthetic and template-based, so they are useful for demonstrating alignment intent but not enough for a production tutor. A stronger version should collect real student questions, add teacher-reviewed chosen answers, include cases where the student has already tried enough and deserves a direct answer, and test with learners in a blind comparison.
