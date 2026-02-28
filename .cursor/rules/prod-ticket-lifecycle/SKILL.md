---
name: prod-ticket-lifecycle
description: |
  本番プロジェクト（docs/tickets）のチケットを、起票→開発→テスト→クローズまで一貫管理する。
  ステータス遷移と記録は scripts を必須経由とし、closed条件（test_status=passed + test_evidence非空）を強制する。
  起票時に「ゴール（デグレ含む）」を必須化し、回帰確認付きで開発・テストを進める。
  closed になったチケットは scripts が docs/tickets/archive へ自動移動する。
  トリガー：「本番チケット運用」「チケットライフサイクル」「チケット起票」「チケット更新」「prod-ticket-lifecycle」
---

# Prod Ticket Lifecycle

docs/tickets のチケット運用をスクリプトで強制する。

## 重要ルール

- チケット更新は `scripts/` のコマンド経由で行う。
- 起票時に `## ゴール（デグレ含む）` を必ず作成する（箇条書き）。
- `## ゴール（デグレ含む）` にはデグレ/回帰確認の項目を最低1つ含める。
- Frontmatterの必須項目（`test_status` / `test_retry_count` / `retry_count` / `last_error` / `test_evidence` / `status_updated_at` を含む）を欠落させない。
- `ticket_status: closed` は `test_status=passed` かつ `test_evidence` 非空の場合のみ許可。
- 起票後は `open -> in_progress -> implemented -> closed` を守る。
- `closed` 遷移時にチケットは `docs/tickets/archive/` へ自動移動される（`archived` ステータスは使わない）。
- Chromeテスト実行は `dev-ticket-chrome-test` を使う。
- 日常運用はまず [quickstart.md](quickstart.md) の順番を使う。

## 使うスクリプト

- `scripts/ticket_create.py`
- `scripts/ticket_validate.py`
- `scripts/ticket_transition.py`
- `scripts/ticket_append_dev_log.py`
- `scripts/ticket_append_test_log.py`

## 標準ワークフロー

1. 起票
```bash
python scripts/ticket_create.py \
  --summary "問題/要望の要約" \
  --goal "実現したいゴール" \
  --regression-check "既存機能のデグレ確認" \
  --priority medium \
  --type improvement
```

2. 妥当性確認
```bash
python scripts/ticket_validate.py docs/tickets/ticket_YYYY-MM-DD-HHmm.md
```

3. 着手（open -> in_progress）
```bash
python scripts/ticket_transition.py docs/tickets/ticket_YYYY-MM-DD-HHmm.md --to in_progress --note "着手"
```

4. 実装ログ追記
```bash
python scripts/ticket_append_dev_log.py docs/tickets/ticket_YYYY-MM-DD-HHmm.md --content "実施内容" --files "対象ファイル"
```

5. 実装完了（in_progress -> implemented）
```bash
python scripts/ticket_transition.py docs/tickets/ticket_YYYY-MM-DD-HHmm.md --to implemented --note "実装完了"
```

6. テスト（`dev-ticket-chrome-test`）

7. テストログ追記
```bash
python scripts/ticket_append_test_log.py docs/tickets/ticket_YYYY-MM-DD-HHmm.md --status passed --summary "主要ケース" --evidence "操作証跡"
```

8. クローズ（implemented -> closed）
```bash
python scripts/ticket_transition.py docs/tickets/ticket_YYYY-MM-DD-HHmm.md --to closed --note "テスト合格"
```

## 参照

- 形式: [references/ticket_schema.md](references/ticket_schema.md)
- 遷移: [references/lifecycle_rules.md](references/lifecycle_rules.md)
- 定型コマンド: [quickstart.md](quickstart.md)
