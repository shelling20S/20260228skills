# Prod Ticket Lifecycle Quickstart

普段使うコマンドだけを順番でまとめた最短運用。

## 0. 変数を置く

```bash
cd /Users/kiyogon/Documents/AIchan/20260131mogi
SKILL=/Users/kiyogon/Desktop/skills/prod-ticket-lifecycle/scripts
TICKET=docs/tickets/ticket_YYYY-MM-DD-HHmm.md
```

## 1. 起票

```bash
python3 "$SKILL/ticket_create.py" \
  --summary "要約" \
  --goal "実現したいゴール" \
  --goal "実現したいゴール（2つ目）" \
  --regression-check "既存機能のデグレ確認項目" \
  --detail "- 詳細" \
  --expected "- 期待動作" \
  --impact "- 影響範囲" \
  --priority medium \
  --type improvement \
  --reporter "ユーザー"
```

出力されたパスを `TICKET` にセットする。

## 2. 形式チェック

```bash
python3 "$SKILL/ticket_validate.py" "$TICKET"
```

## 3. 開発開始

```bash
python3 "$SKILL/ticket_transition.py" "$TICKET" --to in_progress --note "着手"
```

## 4. 実装ログ追記

```bash
python3 "$SKILL/ticket_append_dev_log.py" "$TICKET" \
  --content "実装内容" \
  --files "app/page.tsx,components/CharacterSelect.tsx"
```

## 5. 実装完了

```bash
python3 "$SKILL/ticket_transition.py" "$TICKET" --to implemented --note "実装完了"
```

## 6. テスト実行

`dev-ticket-chrome-test` を使って Chrome で検証し、次のJSONを得る:

```json
{"ticket":"docs/tickets/ticket_YYYY-MM-DD-HHmm.md","test_status":"passed|failed","summary":"1-3行","error":"","evidence":"操作証跡","goal_checks":[{"goal":"ゴール文言そのまま","status":"pass|fail|not_tested","evidence":"根拠"}]}
```

## 7. テスト結果記録

```bash
python3 "$SKILL/ticket_append_test_log.py" "$TICKET" \
  --status passed \
  --summary "主要ケース" \
  --evidence "open/click/type/screenshot ..."
```

失敗時:

```bash
python3 "$SKILL/ticket_append_test_log.py" "$TICKET" \
  --status failed \
  --summary "失敗ケース" \
  --evidence "失敗時の証跡" \
  --error "失敗理由"
```

## 8. クローズ

```bash
python3 "$SKILL/ticket_transition.py" "$TICKET" --to closed --note "テスト合格"
```

`test_status=passed` かつ `test_evidence` 非空でないと失敗する（強制ガード）。
成功時はチケットが `docs/tickets/archive/` に自動移動される。

## 9. 失敗時の戻し

```bash
python3 "$SKILL/ticket_transition.py" "$TICKET" --to in_progress --note "テスト失敗で再開発"
```

## 10. 一括チェック

```bash
python3 "$SKILL/ticket_validate.py" --all --tickets-dir docs/tickets
python3 /Users/kiyogon/Documents/AIchan/20260131mogi/.claude/hooks/ticket_orchestrator.py --action status
```
