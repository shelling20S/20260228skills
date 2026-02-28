#!/usr/bin/env python3
import argparse
import pathlib

from ticket_lib import ensure_meta_defaults, now_jst, parse_frontmatter, write_frontmatter


def parse_args():
    p = argparse.ArgumentParser(description="Append development execution log to ticket")
    p.add_argument("ticket")
    p.add_argument("--content", required=True)
    p.add_argument("--files", default="-")
    p.add_argument("--actor", default="Claude")
    return p.parse_args()


def ensure_dev_log_table(body: str):
    if "## 対応内容（実施結果）" not in body:
        body += (
            "\n\n## 対応内容（実施結果）\n\n"
            "### 実施ログ\n"
            "| 日時 | 対応者 | 内容 | 関連ファイル |\n"
            "|------|--------|------|--------------|\n"
        )
        return body

    if "### 実施ログ" not in body:
        body = body.replace(
            "## 対応内容（実施結果）",
            "## 対応内容（実施結果）\n\n### 実施ログ\n| 日時 | 対応者 | 内容 | 関連ファイル |\n|------|--------|------|--------------|",
            1,
        )
        return body

    if "| 日時 | 対応者 | 内容 | 関連ファイル |" not in body:
        body = body.replace(
            "### 実施ログ",
            "### 実施ログ\n| 日時 | 対応者 | 内容 | 関連ファイル |\n|------|--------|------|--------------|",
            1,
        )
    return body


def append_row_to_dev_log(body: str, row: str):
    marker = "### 実施ログ"
    start = body.find(marker)
    if start == -1:
        return body + "\n" + row + "\n"

    next_section = body.find("\n## ", start + 1)
    if next_section == -1:
        section = body[start:]
        suffix = ""
    else:
        section = body[start:next_section]
        suffix = body[next_section:]

    section = section.rstrip() + "\n" + row + "\n\n"
    return body[:start] + section + suffix.lstrip("\n")


def main():
    args = parse_args()
    ticket_path = pathlib.Path(args.ticket)
    meta, body = parse_frontmatter(ticket_path)
    ensure_meta_defaults(meta)

    now = now_jst()
    row = f"| {now} | {args.actor} | {args.content} | {args.files} |"

    body = ensure_dev_log_table(body)
    body = append_row_to_dev_log(body, row)

    meta["status_updated_at"] = now
    write_frontmatter(ticket_path, meta, body)
    print(f"appended dev log: {ticket_path}")


if __name__ == "__main__":
    main()
