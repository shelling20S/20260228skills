---
name: proto-01-init
description: |
  プロトタイプ開発プロジェクトの初期化。prototype/ディレクトリ構造の作成とprototype_status.mdの生成を行う。
  proto-00-ideation の成果物（IDEATION_RESULT.md）があれば引き継ぐ。初期化後は proto-02-design へ進む。
  トリガー：「プロトタイプ作成開始」「新規プロトタイプ」「プロジェクト初期化」「proto-init」
---

# Proto Init

プロトタイプ開発プロジェクトを初期化する。

## 実行内容

1. `prototype/` ディレクトリを作成
2. `prototype/prototype_status.md` を作成（状態: 開始）
3. `prototype/tickets/` ディレクトリを作成
4. `prototype/history/` ディレクトリを作成（バージョン履歴用）
5. `~/.claude/settings.json` にプロジェクトへの権限を追加（Read/Edit/Write）

## settings.json 更新例

プロトタイプ段階では広めの権限を設定する（denyは空）。`<PROJECT_ROOT>` は実際のプロジェクトパスに置き換える。

```json
{
  "enabledPlugins": {
    "example-skills@anthropic-agent-skills": true
  },
  "permissions": {
    "allow": [
      "Skill",
      "Read(path:<PROJECT_ROOT>/**)",
      "Edit(path:<PROJECT_ROOT>/**)",
      "Write(path:<PROJECT_ROOT>/**)"
    ],
    "deny": []
  }
}
```

## prototype_status.md テンプレート

```markdown
# プロトタイプ状態

## 基本情報
- プロジェクト名: [プロジェクト名]
- 開始日: [YYYY-MM-DD]
- 現在のバージョン: v0

## 現在の状態
- **ステータス**: 開始
- **最終更新**: [YYYY-MM-DD HH:mm]

## 状態履歴
| 日時 | 状態 | 備考 |
|------|------|------|
| [YYYY-MM-DD HH:mm] | 開始 | プロジェクト初期化 |

## 成果物
- [ ] PROTOTYPE.md
- [ ] index.html
```

## IDEATION_RESULT.md の引き継ぎ

`prototype/IDEATION_RESULT.md` が既に存在する場合（proto-00-ideation の成果物）、初期化時にその存在を確認し、`prototype_status.md` の備考欄に「IDEATION_RESULT.md あり」と記録する。proto-02-design がこのファイルを参照してヒアリングを短縮する。

## 次のステップ

初期化完了後、`proto-02-design` を実行して要件ヒアリング＋仕様書作成を開始する。

## 外部レビュー（任意）

スキル完了後、`dev-codex-review` で外部AIによるセカンドオピニオンを取得可能:

```bash
codex review --uncommitted
```
