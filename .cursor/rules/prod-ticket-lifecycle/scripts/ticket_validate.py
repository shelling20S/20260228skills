#!/usr/bin/env python3
import argparse
import pathlib
import re
import sys

from ticket_lib import parse_frontmatter, strip_quotes


REQUIRED_META = [
    "role",
    "depends_on",
    "ticket_status",
    "test_status",
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

ALLOWED_TICKET_STATUS = {"open", "in_progress", "implemented", "closed"}
ALLOWED_TEST_STATUS = {"pending", "running", "passed", "failed", "blocked", ""}

REQUIRED_HEADINGS = [
    "## 概要",
    "## ゴール（デグレ含む）",
    "## 期待する動作",
    "## 影響範囲",
    "## 対応方針",
    "## 対応内容（実施結果）",
    "## テスト結果",
    "## ステータス履歴",
]

REGRESSION_KEYWORDS = ["デグレ", "回帰", "regression", "既存機能"]


def extract_section(body: str, heading: str):
    start = body.find(heading)
    if start == -1:
        return ""
    next_heading = body.find("\n## ", start + len(heading))
    if next_heading == -1:
        return body[start:]
    return body[start:next_heading]


def extract_goal_bullets(section: str):
    goals = []
    for line in section.splitlines():
        text = line.strip()
        if text.startswith("- "):
            goals.append(text[2:].strip())
        else:
            m = re.match(r"^\d+\.\s+(.*)$", text)
            if m:
                goals.append(m.group(1).strip())
    return [g for g in goals if g]


def validate_one(path: pathlib.Path):
    errors = []
    warnings = []

    if not path.exists():
        return [f"{path}: file not found"], warnings

    meta, body = parse_frontmatter(path)

    for key in REQUIRED_META:
        if key not in meta or not str(meta[key]).strip():
            errors.append(f"{path}: missing frontmatter key '{key}'")

    ts = meta.get("ticket_status", "")
    if ts not in ALLOWED_TICKET_STATUS:
        errors.append(f"{path}: invalid ticket_status '{ts}'")

    test_status = meta.get("test_status", "")
    if test_status not in ALLOWED_TEST_STATUS:
        errors.append(f"{path}: invalid test_status '{test_status}'")

    for heading in REQUIRED_HEADINGS:
        if heading not in body:
            errors.append(f"{path}: missing heading '{heading}'")

    goal_section = extract_section(body, "## ゴール（デグレ含む）")
    if goal_section:
        goal_items = extract_goal_bullets(goal_section)
        if not goal_items:
            errors.append(f"{path}: goal section must contain bullet items")
        lower_blob = " ".join(goal_items).lower()
        if not any(keyword.lower() in lower_blob for keyword in REGRESSION_KEYWORDS):
            errors.append(
                f"{path}: goal section must include at least one regression check item "
                f"(デグレ/回帰/regression/既存機能)"
            )

    if ts == "closed":
        if test_status != "passed":
            errors.append(f"{path}: closed ticket must have test_status=passed")
        evidence = strip_quotes(meta.get("test_evidence", ""))
        if not evidence:
            errors.append(f"{path}: closed ticket must have test_evidence")

    return errors, warnings


def parse_args():
    p = argparse.ArgumentParser(description="Validate ticket format")
    p.add_argument("paths", nargs="*", help="ticket files")
    p.add_argument("--tickets-dir", default="docs/tickets")
    p.add_argument("--all", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    targets = []

    if args.all:
        tdir = pathlib.Path(args.tickets_dir)
        targets.extend(sorted(tdir.glob("ticket_*.md")))
    else:
        targets.extend(pathlib.Path(p) for p in args.paths)

    if not targets:
        print("no target tickets", file=sys.stderr)
        return 1

    all_errors = []
    for target in targets:
        errors, warnings = validate_one(target)
        all_errors.extend(errors)
        for w in warnings:
            print(f"WARN: {w}")

    if all_errors:
        for e in all_errors:
            print(f"ERROR: {e}")
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
