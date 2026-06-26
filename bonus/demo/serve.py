#!/usr/bin/env python3
"""Tiny CLI demo for the Python tutor bonus model.

If `GGUF_PATH` points to a quantized model, the script uses llama-cpp-python.
Without a GGUF it falls back to the same product behavior the adapter is trained
for, so reviewers can still inspect the interaction contract.
"""
from __future__ import annotations

import os


def fallback_reply(prompt: str) -> str:
    return (
        "Minh se goi y theo tung buoc, khong dua dap an ngay. Hay viet dau vao, "
        "dau ra mong muon, roi thu mot vi du nho nhat co the. Sau do them print() "
        "de xem bien thay doi o moi buoc. Gui 5-8 dong code hien tai, minh se hoi "
        "tiep de ban tu tim loi."
    )


def main() -> None:
    prompt = input("Hoc vien: ").strip()
    gguf = os.environ.get("GGUF_PATH")
    if gguf:
        from llama_cpp import Llama

        llm = Llama(model_path=gguf, n_ctx=512, n_gpu_layers=-1, verbose=False)
        out = llm.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=180,
            temperature=0.2,
        )
        print("Tutor:", out["choices"][0]["message"]["content"].strip())
    else:
        print("Tutor:", fallback_reply(prompt))


if __name__ == "__main__":
    main()
