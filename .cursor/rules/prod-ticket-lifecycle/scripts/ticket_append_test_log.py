#!/usr/bin/env python3
import argparse
import pathlib
import re

from ticket_lib import ensure_meta_defaults, now_jst, parse_frontmatter, quote_value, write_frontmatter


def parse_args():
    p = argparse.ArgumentParser(description="Append test result to ticket and update test metadata")
    p.add_argument("ticket")
    p.add_argument("--status", required=True, choices=["passed", "failed", "running", "pending", "blocked"])
    p.add_argument("--summary", required=True)
    p.add_argument("--evidence", required=True)
    p.add_argument("--method", default="Chrome MCP")
    p.add_argument("--environment", default="localhost:3000")
    p.add_argument("--error", default="")
    return p.parse_args()


def ensure_test_sections(body: str):
    if "## テスト結果" not in body:
        body += (
            "\n\n## テスト結果\n\n"
            "### テスト実施情報\n"
            "- **実施日時**:\n"
            "- **テスト方法**:\n"
            "- **テスト環境**:\n\n"
            "### 結果\n"
            "| # | テスト項目 | 結果 | 備考 |\n"
            "|---|----------|------|------|\n\n"
            "### 発見した不具合\n"
            "| # | 重要度 | 内容 | 該当箇所 |\n"
            "|---|--------|------|---------|\n"
            "| - | - | なし | - |\n\n"
            "### 総合判定\n"
            "- **主要機能**:\n"
            "- **残課題**:\n"
        )
        return body

    if "### 結果" not in body:
        body = body.replace(
            "## テスト結果",
            "## テスト結果\n\n### 結果\n| # | テスト項目 | 結果 | 備考 |\n|---|----------|------|------|\n",
            1,
        )

    if "| # | テスト項目 | 結果 | 備考 |" not in body:
        body = body.replace(
            "### 結果",
            "### 結果\n| # | テスト項目 | 結果 | 備考 |\n|---|----------|------|------|",
            1,
        )

    return body


def next_case_no(section: str) -> int:
    nums = []
    for line in section.splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|", line)
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) + 1) if nums else 1


def append_result_row(body: str, summary: str, status: str, note: str):
    marker = "### 結果"
    start = body.find(marker)
    if start == -1:
        return body

    next_heading = body.find("\n### ", start + 1)
    if next_heading == -1:
        section = body[start:]
        suffix = ""
    else:
        section = body[start:next_heading]
        suffix = body[next_heading:]

    no = next_case_no(section)
    row = f"| {no} | {summary} | {status.upper()} | {note} |"
    section = section.rstrip() + "\n" + row + "\n\n"
    return body[:start] + section + suffix.lstrip("\n")


def upsert_exec_info(body: str, executed_at: str, method: str, environment: str):
    if "### テスト実施情報" not in body:
        return body

    start = body.find("### テスト実施情報")
    next_heading = body.find("\n### ", start + 1)
    if next_heading == -1:
        section = body[start:]
        suffix = ""
    else:
        section = body[start:next_heading]
        suffix = body[next_heading:]

    section = (
        "### テスト実施情報\n"
        f"- **実施日時**: {executed_at}\n"
        f"- **テスト方法**: {method}\n"
        f"- **テスト環境**: {environment}\n\n"
    )
    return body[:start] + section + suffix.lstrip("\n")


def main():
    args = parse_args()
    ticket_path = pathlib.Path(args.ticket)
    meta, body = parse_frontmatter(ticket_path)
    ensure_meta_defaults(meta)

    now = now_jst()
    body = ensure_test_sections(body)
    body = upsert_exec_info(body, now, args.method, args.environment)
    note = args.error if args.error else args.evidence
    body = append_result_row(body, args.summary, args.status, note)

    meta["test_status"] = args.status
    meta["test_evidence"] = quote_value(args.evidence)
    meta["last_error"] = quote_value(args.error if args.error else "")
    meta["status_updated_at"] = now

    write_frontmatter(ticket_path, meta, body)
    print(f"appended test log: {ticket_path} ({args.status})")


if __name__ == "__main__":
    main()
