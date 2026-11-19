#!/usr/bin/env python3
"""Static gates for the two videos: no solution leak, no unsafe patterns."""
import argparse
import re
import sys
from pathlib import Path

FORBIDDEN = [
    "排序", "贪心", "统计", "前缀和", "动态规划", "二分", "哈希",
    "桶", "双指针", "并查集", "递归", "递推", "枚举", "复杂度",
]
CODE_MARKS = ["#include", "int main", "for (", "while (", "cout <<", "return 0"]


def get_html(path: Path) -> str:
    p = path / "index.html" if path.is_dir() else path
    if not p.exists():
        raise SystemExit(f"no index.html at {p}")
    return p.read_text(encoding="utf-8", errors="ignore")


def check_common(html: str) -> list[str]:
    errors = []
    if not re.search(r'data-duration="[0-9.]+"', html):
        errors.append("missing data-duration")
    if "Math.random" in html or "Date.now" in html:
        errors.append("non-deterministic call found (Math.random / Date.now)")
    if "tl.call(" in html:
        errors.append("tl.call() found: text mutation is unreliable under seek; pre-build nodes")
    return errors


def check_statement(html: str) -> list[str]:
    errors = []
    for word in FORBIDDEN:
        if word in html:
            errors.append(f"solution word in statement video: {word}")
    for mark in CODE_MARKS:
        if mark in html:
            errors.append(f"code fragment in statement video: {mark}")
    return errors


def check_solution(html: str) -> list[str]:
    warnings = []
    if re.search(r"\bint\s+res\b", html) or re.search(r"\blong\s+long\s+res\b", html):
        warnings.append("res is an integer: check the maximum answer length")
    if re.search(r"res\s*=\s*res\s*\*\s*10", html):
        warnings.append("res = res * 10: overflow risk for long answers")
    if "res.append(arr[i], '0' + i)" in html:
        warnings.append("append(count, '0'+i): second argument is int; use char('0'+i)")
    if "#include" in html and "#include <string>" not in html and "#include &lt;string&gt;" not in html:
        warnings.append("missing <string> include in the displayed code")
    return warnings


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--statement", action="store_true")
    args = ap.parse_args()

    html = get_html(Path(args.path))
    errors = check_common(html)
    warnings = []

    if args.statement:
        errors += check_statement(html)
    else:
        warnings += check_solution(html)

    for e in errors:
        print("ERROR", e)
    for w in warnings:
        print("WARN ", w)
    if not errors and not warnings:
        print("OK")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
