---
name: proto-05-html-builder
description: |
  DESIGN_DECISION.md + PROTOTYPE.md を元にindex.html（1ファイル完結プロトタイプ）を作成する。
  DESIGN_DECISION.mdがない場合はフォールバックテンプレートを使用。完了後は自動で proto-06-code-review を実行。
  パイプライン: proto-04-design-gallery → **proto-05-html-builder** → proto-06-code-review。
  トリガー：「プロトタイプ実装」「HTML作成」「HTML実装」「index.html作成」「proto-html-builder」
---

# Proto HTML Builder

PROTOTYPE.mdを元にindex.htmlを作成する（1ファイル完結）。

## コア原則

- **引き算のデザイン**: 一人のデザイナーの目線で、一貫したビジョンを貫く
- **モック優先**: 外部API禁止、localStorage永続化、疑似ローディング(300-800ms)
- **反応必須**: 全アクションに視覚的反応、行き止まり禁止

## 技術制約

- 素のHTML/CSS/JS（ビルドツール不使用）
- 画面サイズ: 375px × 812px（モバイルファースト）
- データ永続化: localStorage / IndexedDB

## ワークフロー

1. `prototype/DESIGN_DECISION.md` を読み込む（存在する場合）
2. `prototype/PROTOTYPE.md` を読み込む
3. デザイン方針の決定:
   - **DESIGN_DECISION.md がある場合**: 記載されたデザイン方針（カラー・フォント・アニメーション等）に従う
   - **DESIGN_DECISION.md がない場合**: `references/css_patterns.md` のフォールバックテンプレートから選択（retro/minimal/dark/nature/pop）
4. 差別化チェック実施
5. index.html 作成
6. prototype_status.md 更新

## 必須チェック（実装前）

- [ ] 共感ファースト（機能説明より悩みへの共感）
- [ ] メタファーの視覚化（サービス名をアニメーションに）
- [ ] Before/After の可視化
- [ ] SaaSテンプレ色（青+グレー）を回避
- [ ] 具体的な数字の約束

## 参照ファイル（詳細が必要な時に読む）

| ファイル | 内容 |
|---------|------|
| `prototype/DESIGN_DECISION.md` | デザイン決定事項（proto-04の出力。カラー・フォント・アニメーション方針） |
| `references/design_principles.md` | 設計原則、プロトタイプ基本方針 |
| `references/bug_prevention.md` | バグ防止ルール（HTML/CSS/JS） |
| `references/css_patterns.md` | CSSパターン、タイポグラフィ、フォールバックテンプレート |
| `references/js_patterns.md` | JSパターン（状態管理、モーダル等） |
| `references/differentiation.md` | 差別化デザインパターン |

## 出力

1. `prototype/index.html`
2. `prototype/prototype_status.md` 更新（状態: 実装完了）

## 次のステップ

`proto-06-code-review` を実行してコードレビュー
