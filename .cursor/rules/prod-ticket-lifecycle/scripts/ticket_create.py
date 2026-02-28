#!/usr/bin/env python3
import argparse
import datetime as dt
import pathlib

from ticket_lib import now_jst, quote_value


def parse_args():
    p = argparse.ArgumentParser(description="Create ticket markdown file")
    p.add_argument("--summary", required=True)
    p.add_argument("--goal", action="append", default=[], help="goal item (repeatable)")
    p.add_argument(
        "--regression-check",
        action="append",
        default=[],
        help="regression check item for ゴール（デグレ含む） (repeatable)",
    )
    p.add_argument("--detail", default="")
    p.add_argument("--expected", default="")
    p.add_argument("--impact", default="")
    p.add_argument("--priority", default="medium", choices=["critical", "high", "medium", "low"])
    p.add_argument("--type", dest="ticket_type", default="improvement", choices=["bug", "feature", "improvement", "question"])
    p.add_argument("--reporter", default="ユーザー")
    p.add_argument("--tickets-dir", default="docs/tickets")
    return p.parse_args()


def pick_filename(dir_path: pathlib.Path, base_dt: dt.datetime) -> pathlib.Path:
    candidate_dt = base_dt
    for _ in range(180):
        name = candidate_dt.strftime("ticket_%Y-%m-%d-%H%M.md")
        path = dir_path / name
        if not path.exists():
            return path
        candidate_dt += dt.timedelta(minutes=1)
    raise RuntimeError("failed to choose unique ticket filename")


def main():
    args = parse_args()
    jst = dt.timezone(dt.timedelta(hours=9))
    now = dt.datetime.now(jst)
    now_str = now.strftime("%Y-%m-%d %H:%M")

    tickets_dir = pathlib.Path(args.tickets_dir)
    tickets_dir.mkdir(parents=True, exist_ok=True)
    ticket_path = pick_filename(tickets_dir, now)

    detail = args.detail or "- [要望/不具合の詳細を記載]"
    expected = args.expected or "- [期待する動作を記載]"
    impact = args.impact or "- [影響箇所を記載]"
    goals = args.goal[:] if args.goal else []
    regressions = args.regression_check[:] if args.regression_check else []

    if not goals:
        goals = ["[実現したいゴールを記載]"]
    if not regressions:
        regressions = ["[既存機能のデグレ確認項目を記載]"]

    goal_lines = [f"- ゴール: {g}" for g in goals]
    goal_lines.extend([f"- デグレ確認: {r}" for r in regressions])
    goal_block = "\n".join(goal_lines)

    content = f"""---
role: ticket
depends_on: []
ticket_status: open
test_status: pending
test_retry_count: 0
retry_count: 0
last_error: ""
test_evidence: ""
status_updated_at: {now_str}
priority: {args.priority}
type: {args.ticket_type}
created_at: {now_str}
reporter: {quote_value(args.reporter)}
---

# チケット

**日時**: {now_str}
**報告者**: {args.reporter}
**優先度**: {args.priority}
**種類**: {args.ticket_type}

## 概要

{args.summary}

## ゴール（デグレ含む）

{goal_block}

## 詳細

### 現象・要望
{detail}

## 期待する動作

{expected}

## 影響範囲

{impact}

## 発見した不具合

- なし

## 対応方針

- [対応方針を記載]

## 対応内容（実施結果）

### 実施ログ
| 日時 | 対応者 | 内容 | 関連ファイル |
|------|--------|------|--------------|

## テスト結果

### テスト実施情報
- **実施日時**:
- **テスト方法**:
- **テスト環境**:

### 結果
| # | テスト項目 | 結果 | 備考 |
|---|----------|------|------|

### 発見した不具合
| # | 重要度 | 内容 | 該当箇所 |
|---|--------|------|---------|
| - | - | なし | - |

### 総合判定
- **主要機能**:
- **残課題**:

## ステータス履歴

| 日時 | 状態 | 備考 |
|------|------|------|
| {now_str} | open | 報告受付 |
"""

    ticket_path.write_text(content, encoding="utf-8")
    print(ticket_path)


if __name__ == "__main__":
    main()
