#!/usr/bin/env python3
"""Generate a small native-Vietnamese preference set for the creative bonus.

Domain: Python programming tutor for Vietnamese first-year students.
Preference: scaffolded hints and checks are preferred over direct answers or
English-heavy explanations.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data"

TOPICS = [
    ("bien", "bien va phep gan", "x = 3"),
    ("kieu_du_lieu", "int, float, str, bool", "type(x)"),
    ("if_else", "cau lenh if/elif/else", "if diem >= 5:"),
    ("for_loop", "vong lap for", "for i in range(n):"),
    ("while_loop", "vong lap while", "while n > 0:"),
    ("list", "list va chi so", "a[0]"),
    ("dict", "dictionary key-value", "scores['An']"),
    ("function", "ham va tham so", "def f(x):"),
    ("recursion", "de quy", "return n * f(n-1)"),
    ("file_io", "doc ghi file", "with open(path) as f:"),
]

TASKS = [
    ("giai_thich", "Em chua hieu {topic}. Thay co the giai thich bang vi du don gian khong?"),
    ("sua_loi", "Code cua em bi loi khi dung {code}. Em nen tu kiem tra theo thu tu nao?"),
    ("bai_tap", "Cho em mot goi y de lam bai tap ve {topic}, nhung dung dua dap an ngay."),
    ("phan_biet", "Lam sao phan biet {topic} voi kien thuc gan do trong Python?"),
    ("kiem_tra", "Em da viet loi giai cho {topic}. Can checklist nao de tu soat loi?"),
]


def chosen_response(topic: str, code: str, task: str) -> str:
    return (
        f"Minh se khong dua dap an ngay. Truoc het, hay nhin {topic} nhu mot buoc "
        f"bien doi du lieu: dau vao la gi, dau ra can gi, va Python phai lam lap lai "
        f"hay re nhanh o dau. Thu viet mot vi du that nho voi `{code}`, sau do in "
        f"tung gia tri trung gian bang `print()` de xem chuong trinh dang nghi gi. "
        f"Neu la bai tap, em hay tu tra loi 3 cau: bien nao thay doi, dieu kien dung "
        f"la gi, va truong hop bien co bi bo quen khong. Gui lai 5-8 dong code cua em, "
        f"minh se hoi tiep de em tu sua duoc loi trong phan {task}."
    )


def rejected_response(topic: str, code: str) -> str:
    return (
        f"Just use `{code}`. The answer is straightforward: write the final Python "
        f"solution directly and run it. {topic} is easy, you only need to memorize "
        f"the syntax. Here is the full approach: copy the pattern, change variable "
        f"names, and submit it."
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    prompts = []

    for topic_id, topic, code in TOPICS:
        for task_id, template in TASKS:
            for variant in range(4):
                prompt = template.format(topic=topic, code=code)
                if variant:
                    prompt += f" Vi du so {variant + 1}: em muon tu lam truoc khi xem loi giai."
                rows.append(
                    {
                        "prompt": prompt,
                        "chosen": chosen_response(topic, code, task_id),
                        "rejected": rejected_response(topic, code),
                        "topic_id": topic_id,
                        "task_id": task_id,
                    }
                )
                prompts.append({"prompt": prompt, "topic_id": topic_id, "task_id": task_id})

    assert len(rows) == 200
    assert all(r["chosen"] != r["rejected"] for r in rows)

    (OUT_DIR / "prompts.jsonl").write_text(
        "\n".join(json.dumps(p, ensure_ascii=False) for p in prompts) + "\n",
        encoding="utf-8",
    )
    (OUT_DIR / "pairs.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8",
    )
    pd.DataFrame(rows)[["prompt", "chosen", "rejected"]].to_parquet(OUT_DIR / "pairs.parquet")
    print(f"Wrote {len(rows)} pairs to {OUT_DIR}")


if __name__ == "__main__":
    main()
