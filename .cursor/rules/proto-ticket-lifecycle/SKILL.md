---
name: proto-ticket-lifecycle
description: |
  proto-06-code-review後のユーザーレビューで発生した修正依頼・バグ報告をチケットで管理する。
  open → in_progress → implemented → closed の遷移を強制し、テスト完了後のみcloseを許可。
  本番チケット（docs/tickets）は prod-ticket-lifecycle を使う。
  トリガー：「プロトタイプチケット運用」「修正依頼」「バグ報告」「proto-ticket-lifecycle」「UI修正チケット」「プロトタイプ修正チケット」
---

# Proto Ticket Lifecycle

prototype/tickets のチケット運用を統一する。

## 重要ルール

- ステータス遷移は `open -> in_progress -> implemented -> closed` を守る。
- `closed` はテスト完了後のみ。
- 起票時に `## ゴール（デグレ含む）` を必ず記載する（箇条書き）。
- `## ゴール（デグレ含む）` にはデグレ/回帰確認を最低1項目含める。
- `closed` 遷移時にチケットは `prototype/tickets/archive/` へ自動移動する（`archived` ステータスは使わない）。
- 本番案件には使わず、`prod-ticket-lifecycle` を使う。

## ワークフロー

1. `prototype/tickets` に起票する。
2. `in_progress` に遷移して修正する。
3. 実施ログをチケットに追記する。
4. `implemented` に遷移する。
5. テスト後、合格なら `closed` に遷移する。

## チケットテンプレート

```markdown
---
ticket_status: open
created: YYYY-MM-DD HH:mm
updated: YYYY-MM-DD HH:mm
---

# [チケットタイトル]

## 概要
[修正・改善の背景と内容]

## ゴール（デグレ含む）
- [ ] [達成すべき条件1]
- [ ] [達成すべき条件2]
- [ ] [デグレ確認] [既存機能Xが引き続き動作すること]

## 実施ログ
<!-- 作業内容を時系列で追記 -->
```

## スクリプト使用方法

`prod-ticket-lifecycle/scripts` を `--tickets-dir` オプション付きで流用する。

```bash
# 起票
python /Users/kiyogon/Desktop/skills/prod-ticket-lifecycle/scripts/ticket_create.py \
  --tickets-dir prototype/tickets \
  --summary "ボタンの配色を修正"

# ステータス遷移（open → in_progress）
python /Users/kiyogon/Desktop/skills/prod-ticket-lifecycle/scripts/ticket_transition.py \
  prototype/tickets/ticket_YYYY-MM-DD-HHmm.md \
  --to in_progress --note "着手"

# ステータス遷移（in_progress → implemented）
python /Users/kiyogon/Desktop/skills/prod-ticket-lifecycle/scripts/ticket_transition.py \
  prototype/tickets/ticket_YYYY-MM-DD-HHmm.md \
  --to implemented --note "修正完了"

# ステータス遷移（implemented → closed）※テスト完了後のみ
python /Users/kiyogon/Desktop/skills/prod-ticket-lifecycle/scripts/ticket_transition.py \
  prototype/tickets/ticket_YYYY-MM-DD-HHmm.md \
  --to closed --note "テスト合格"
# → 自動で prototype/tickets/archive/ に移動される
```

## 参照

- [references/lifecycle_rules.md](references/lifecycle_rules.md)
