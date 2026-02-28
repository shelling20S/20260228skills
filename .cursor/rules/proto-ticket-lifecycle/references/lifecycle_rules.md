# Lifecycle Rules (prototype)

## 対象

- チケット格納先: `prototype/tickets`
- 遷移: `open -> in_progress -> implemented -> closed`

## 強制ルール

- `closed` はテスト完了後のみ。
- 起票時に `## ゴール（デグレ含む）` を記載し、デグレ/回帰確認を最低1項目含める。
- `implemented -> closed` 成功時にファイルは `prototype/tickets/archive/` へ自動移動される。
- `archived` という `ticket_status` は使用しない。
- 変更記録は必ずチケット本文に残す。
- 本番チケット（docs/tickets）は `prod-ticket-lifecycle` を使う。

## 実行コマンド（prodスクリプト流用）

```bash
# 起票
python /Users/kiyogon/Desktop/skills/prod-ticket-lifecycle/scripts/ticket_create.py \
  --tickets-dir prototype/tickets \
  --summary "..."

# 遷移
python /Users/kiyogon/Desktop/skills/prod-ticket-lifecycle/scripts/ticket_transition.py \
  prototype/tickets/ticket_YYYY-MM-DD-HHmm.md --to in_progress --note "着手"
```
