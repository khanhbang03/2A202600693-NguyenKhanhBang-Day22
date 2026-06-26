# Python Tutor DPO v0

## What This Model Is For

This experimental adapter is for Vietnamese first-year students learning Python fundamentals. It is aligned to behave like a scaffolded tutor: ask the learner to identify inputs and outputs, suggest tiny examples, encourage tracing with `print()`, and avoid giving the complete final answer too early.

## What This Model Is Not For

It is not a homework-answer machine, grading system, plagiarism tool, or replacement for a teacher. It should not produce full solutions when the prompt asks for learning support. It also should not pretend to execute code or guarantee that a student's program is correct without seeing the actual code and tests.

## Data

The bonus dataset contains 200 native-Vietnamese preference pairs in `bonus/data/pairs.parquet`. Chosen responses use Vietnamese tutoring language and stepwise hints. Rejected responses are deliberately direct, generic, or English-heavy. The data is synthetic but hand-designed around common Python 101 topics: variables, types, conditionals, loops, lists, dictionaries, functions, recursion, and file I/O.

## Training

Run the main lab through NB1 first so `adapters/sft-mini/` exists. Then run:

```bash
python bonus/data/generate_pairs.py
python bonus/train.py
```

The wrapper calls `scripts/train_dpo.py` with `--pref-path bonus/data/pairs.parquet` and writes `bonus/adapters/dpo-python-tutor/`.

## Evaluation Plan

The intended evaluation is a small blind comparison with learners or classmates:

1. Ask 10 Python 101 questions.
2. Compare SFT-only and bonus-DPO outputs.
3. Prefer the answer that helps the learner take the next step without copying a final solution.
4. Track three labels: scaffolded, too direct, or too vague.

Success means the DPO version is more often scaffolded and less often a direct answer.

## Known Limitations

The dataset is small and template-generated, so the adapter may overuse phrases like "khong dua dap an ngay" or "thu vi du nho". It covers Python basics only and does not handle advanced debugging, packages, web frameworks, or performance topics. A real v1 should add student-written prompts, teacher review, and examples where a direct answer is appropriate after the student has already solved most of the problem.

## Vibe-Coding Log

The most useful prompt pattern was: "write chosen as a tutor who asks the next diagnostic question, rejected as a generic answer-giver." The less useful pattern was asking for "better answer vs worse answer" without naming pedagogy; that produced vague politeness rather than a concrete learning behavior.
