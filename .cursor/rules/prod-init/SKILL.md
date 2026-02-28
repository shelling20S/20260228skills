---
name: prod-init
description: 本番プロジェクトの初期化。docs/配下にドキュメント構造を作成し、README.md、CLAUDE.md、STATUS.mdを生成する。トリガー：「プロジェクト初期化」「新規プロジェクト」「prod-init」「ドキュメント構造作成」
---

# Prod Init

本番プロジェクトのドキュメント構造を初期化する。

## 実行内容

1. ルートファイルを作成
   - `README.md` - プロジェクト概要/セットアップ
   - `CLAUDE.md` - AI向け技術ガイド
   - `STATUS.md` - プロジェクト状況サマリ

2. `docs/` ディレクトリ構造を作成
   ```
   docs/
   ├── README.md              # ドキュメント索引
   ├── 01_spec/               # 要件定義
   │   ├── overview.md
   │   ├── glossary.md
   │   ├── requirements.md
   │   ├── constraints.md
   │   └── use_cases.md
   ├── 02_design/             # 設計
   │   ├── domain_model.md
   │   ├── ui_flows.md
   │   ├── api_contracts.md
   │   ├── technical_architecture.md
   │   ├── tech_stack.md
   │   ├── basic_design.md
   │   └── detailed_design.md
   ├── 03_prompts/            # AIプロンプト（必要時）
   ├── 04_impl/               # 実装計画
   │   └── implementation_plan.md
   ├── 05_test/               # テスト
   │   └── test_plan.md
   └── 90_decisions/          # 決定履歴
       └── decision_log.md
   ```

3. `~/.claude/settings.json` にプロジェクトへの権限を追加

## ドキュメントメタデータ規約

すべてのドキュメントは YAML Front Matter を持つ:

```yaml
---
role: spec | design | plan | test | prompt | decision | guide | index
depends_on: []  # 依存ファイルのパス（docs/を省略した相対パス）
---
```

## テンプレート

### README.md（ルート）

```markdown
# [プロジェクト名]

[プロジェクトの簡潔な説明]

## セットアップ

\`\`\`bash
npm install
npm run dev
\`\`\`

## 開発コマンド

\`\`\`bash
npm run dev      # 開発サーバー起動
npm run build    # ビルド
npm run test     # テスト実行
npm run lint     # Lint実行
\`\`\`

## ドキュメント

詳細は [docs/README.md](docs/README.md) を参照。
```

### CLAUDE.md（ルート）

```markdown
# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

**[プロジェクト名]** - [プロジェクトの説明]

## Tech Stack

- **Frontend**: [フレームワーク]
- **Backend**: [バックエンド]
- **Database**: [データベース]

## Commands

\`\`\`bash
npm install
npm run dev
npm run build
npm run test
\`\`\`

## Documentation Structure

Start with `docs/README.md` for the full structure.

## Documentation Priority

When specs conflict, follow the order defined in `docs/README.md`.
```

### STATUS.md（ルート）

```markdown
# STATUS.md

## 現在の状況

- **フェーズ**: 初期化
- **進捗**: 0%
- **最終更新**: [YYYY-MM-DD]

## 完了した作業

- [ ] プロジェクト初期化

## 次のアクション

1. 要件定義（docs/01_spec/）の作成
2. 基本設計（docs/02_design/）の作成

## ブロッカー

なし
```

### docs/README.md

```markdown
---
role: index
depends_on: []
---
# ドキュメント全体像

## 目的
- ディレクトリ構造、各ファイルの役割、参照順の唯一の定義をここに集約する。

## リポジトリ構造
\`\`\`
/
├── README.md              # プロジェクト概要/セットアップ
├── STATUS.md              # プロジェクト状況のサマリ/次アクション
├── CLAUDE.md              # AI向け技術ガイド
└── docs/
    ├── README.md          # ドキュメントの唯一の索引（本ファイル）
    ├── 01_spec/           # 要件定義
    ├── 02_design/         # 設計
    ├── 03_prompts/        # AIプロンプト
    ├── 04_impl/           # 実装計画
    ├── 05_test/           # テスト
    └── 90_decisions/      # 決定履歴
\`\`\`

## メタデータ（必須）
- すべてのドキュメントは YAML Front Matter を持つ。
- 必須キー: role / depends_on

## ドキュメントマップ

### 01_spec（要件定義）
- overview.md: プロダクトの位置づけ、目的/非目的
- glossary.md: 用語定義
- requirements.md: 機能要件と受入条件
- constraints.md: 非機能要件と制約
- use_cases.md: ユースケース詳細

### 02_design（設計）
- domain_model.md: ドメインエンティティ/属性
- ui_flows.md: 画面構成、導線
- api_contracts.md: API I/F契約
- technical_architecture.md: 技術アーキテクチャ
- tech_stack.md: フレームワーク/ライブラリ方針
- basic_design.md: 基本設計の骨子
- detailed_design.md: 実装に必要な具体例

### 04_impl（実装計画）
- implementation_plan.md: マイルストーン、作業順序

### 05_test（テスト）
- test_plan.md: テスト方針、範囲、実行手順

### 90_decisions（決定履歴）
- decision_log.md: 重要な決定と理由の要約

## 参照順（矛盾時）
1. Spec（docs/01_spec/*）
2. Design（docs/02_design/*）
3. Impl/Test（docs/04_impl/*, docs/05_test/*）
4. Decisions（docs/90_decisions/*）
```

### 01_spec/overview.md

```markdown
---
role: spec
depends_on: []
---
# プロダクト概要

## 目的
[このプロダクトが解決する問題]

## 非目的
[このプロダクトでは扱わないこと]

## 提供範囲
[提供する機能の概要]

## ターゲットユーザー
[想定ユーザー]
```

### 01_spec/requirements.md

```markdown
---
role: spec
depends_on:
  - 01_spec/overview.md
---
# 機能要件

## REQ-001: [機能名]
- **概要**: [機能の説明]
- **受入条件**:
  - [ ] [条件1]
  - [ ] [条件2]
```

### 90_decisions/decision_log.md

```markdown
---
role: decision
depends_on: []
---
# 決定履歴

## [YYYY-MM-DD] [決定タイトル]
- **背景**: [なぜこの決定が必要だったか]
- **選択肢**: [検討した選択肢]
- **決定**: [最終的な決定]
- **理由**: [決定の理由]
```

## 次のステップ

初期化完了後:
1. `docs/01_spec/overview.md` でプロダクト概要を定義
2. `docs/01_spec/requirements.md` で機能要件を定義
3. `docs/02_design/` で設計を進める

## settings.json 更新例

```json
{
  "permissions": {
    "allow": [
      "Skill",
      "Read(path:/path/to/project/**)",
      "Edit(path:/path/to/project/**)",
      "Write(path:/path/to/project/**)"
    ],
    "deny": []
  }
}
```
