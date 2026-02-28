# Lifecycle Rules (prod)

## Allowed Transition

- `open -> in_progress`
- `in_progress -> implemented`
- `implemented -> in_progress` (test failed)
- `implemented -> closed` (only after pass)
- `closed -> closed` (idempotent)

## Archive Rule

- `implemented -> closed` 成功時に、チケットファイルは `docs/tickets/archive/` に自動移動される。
- `archived` という `ticket_status` は使用しない。

## Close Guardrail

`closed` へ遷移するには両方必須:

- `test_status = passed`
- `test_evidence` が空でない

加えて運用上の必須条件:

- チケット本文に `## ゴール（デグレ含む）` があり、箇条書きのゴールが定義されている
- ゴールにはデグレ/回帰確認が最低1項目含まれている
- テスト結果JSONの `goal_checks` でゴール全件を検証する

## Core Commands

```bash
# create
python scripts/ticket_create.py --summary "..."

# validate
python scripts/ticket_validate.py docs/tickets/ticket_YYYY-MM-DD-HHmm.md

# open -> in_progress
python scripts/ticket_transition.py docs/tickets/ticket_*.md --to in_progress --note "着手"

# dev log append
python scripts/ticket_append_dev_log.py docs/tickets/ticket_*.md --content "実装内容" --files "app/page.tsx"

# in_progress -> implemented
python scripts/ticket_transition.py docs/tickets/ticket_*.md --to implemented --note "実装完了"

# test log append
python scripts/ticket_append_test_log.py docs/tickets/ticket_*.md --status passed --summary "主要ケース" --evidence "screenshot:..."

# implemented -> closed
python scripts/ticket_transition.py docs/tickets/ticket_*.md --to closed --note "テスト合格"
```
