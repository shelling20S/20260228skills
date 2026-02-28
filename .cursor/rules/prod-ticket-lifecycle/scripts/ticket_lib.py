#!/usr/bin/env python3
import datetime as dt
import pathlib
import re
from typing import Dict, Tuple


FRONTMATTER_RE = re.compile(r"(?s)^---\n(.*?)\n---\n(.*)$")


def now_jst(fmt: str = "%Y-%m-%d %H:%M") -> str:
    jst = dt.timezone(dt.timedelta(hours=9))
    return dt.datetime.now(jst).strftime(fmt)


def parse_frontmatter(path: pathlib.Path) -> Tuple[Dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    raw_meta, body = match.group(1), match.group(2)
    meta: Dict[str, str] = {}
    for line in raw_meta.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, body


def write_frontmatter(path: pathlib.Path, meta: Dict[str, str], body: str):
    ordered_keys = [
        "role",
        "depends_on",
        "ticket_status",
        "test_status",
        "test_timeout_sec",
        "test_retry_count",
        "retry_count",
        "last_error",
        "test_evidence",
        "status_updated_at",
        "priority",
        "type",
        "created_at",
        "reporter",
    ]
    lines = []
    for key in ordered_keys:
        if key in meta:
            lines.append(f"{key}: {meta[key]}")
    for key, value in meta.items():
        if key not in ordered_keys:
            lines.append(f"{key}: {value}")

    content = "---\n" + "\n".join(lines) + "\n---\n" + body
    path.write_text(content, encoding="utf-8")


def ensure_meta_defaults(meta: Dict[str, str]):
    meta.setdefault("role", "ticket")
    meta.setdefault("depends_on", "[]")
    meta.setdefault("ticket_status", "open")
    meta.setdefault("test_status", "pending")
    meta.setdefault("test_retry_count", "0")
    meta.setdefault("retry_count", "0")
    meta.setdefault("last_error", '""')
    meta.setdefault("test_evidence", '""')


def clean_line(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def quote_value(text: str) -> str:
    t = clean_line(text).replace('"', "'")
    return f'"{t}"'


def strip_quotes(text: str) -> str:
    s = str(text).strip()
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    return s


def append_status_history(body: str, when: str, status: str, note: str):
    row = f"| {when} | {status} | {note or '-'} |"
    heading = "## ステータス履歴"

    idx = body.find(heading)
    if idx == -1:
        addition = (
            "\n\n## ステータス履歴\n\n"
            "| 日時 | 状態 | 備考 |\n"
            "|------|------|------|\n"
            f"{row}\n"
        )
        return body.rstrip() + addition + "\n"

    next_idx = body.find("\n## ", idx + 1)
    if next_idx == -1:
        section = body[idx:]
        suffix = ""
    else:
        section = body[idx:next_idx]
        suffix = body[next_idx:]

    if "|------|------|------|" not in section:
        section = (
            "## ステータス履歴\n\n"
            "| 日時 | 状態 | 備考 |\n"
            "|------|------|------|\n"
        )

    section = section.rstrip() + "\n" + row + "\n\n"
    return body[:idx] + section + suffix.lstrip("\n")
