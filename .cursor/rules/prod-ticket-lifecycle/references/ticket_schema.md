# Ticket Schema (prod)

## Frontmatter Required

- `role: ticket`
- `depends_on: []`
- `ticket_status: open|in_progress|implemented|closed`
- `test_status: pending|running|passed|failed|blocked`
- `test_retry_count`
- `retry_count`
- `last_error`
- `test_evidence`
- `status_updated_at`
- `priority: critical|high|medium|low`
- `type: bug|feature|improvement|question`
- `created_at: YYYY-MM-DD HH:mm` (JST)
- `reporter: ...`

## Frontmatter Optional

- `test_timeout_sec`

## Body Required Headings

- `## 概要`
- `## ゴール（デグレ含む）`
- `## 期待する動作`
- `## 影響範囲`
- `## 対応方針`
- `## 対応内容（実施結果）`
- `## テスト結果`
- `## ステータス履歴`

## Goal Rules

- `## ゴール（デグレ含む）` は箇条書きで記載する。
- ゴール箇条書きにはデグレ/回帰確認を最低1項目含める（例: `デグレ確認: ...`）。
