---
name: proto-06-code-review
description: |
  index.htmlのコード品質チェックとPROTOTYPE.mdとの整合性確認（自動実行）。CSS/JS/HTMLのバグ防止パターン、
  フォントサイズ基準、仕様整合性を検査する。OK後はユーザーレビューへ進み、修正依頼は proto-ticket-lifecycle で管理。
  パイプライン: proto-05-html-builder → **proto-06-code-review** → ユーザーレビュー。
  トリガー：proto-05-html-builder完了後に自動実行、「コードレビュー」「実装チェック」「品質チェック」「proto-code-review」
---

# Proto Code Review

`prototype/index.html` のコード品質と `prototype/PROTOTYPE.md` との整合性をチェックする（自動実行）。

## チェック項目

### 1. コード品質チェック

#### CSS
- [ ] CSS変数（カスタムプロパティ）を使用しているか
- [ ] z-index が体系的に管理されているか
- [ ] `position: fixed` の使い方は適切か（phone-frame内では absolute）
- [ ] `white-space` の設定は意図通りか
- [ ] flexbox の `min-height: 0` 問題に対応しているか
- [ ] **フォントサイズが最低基準を満たしているか（12px未満は禁止）**

#### JavaScript
- [ ] localStorage の null チェックを行っているか
- [ ] XSS 対策（escapeHtml）を行っているか
- [ ] touchイベントに `{ passive: true }` を設定しているか
- [ ] Date.getMonth() に +1 しているか

#### HTML
- [ ] lang="ja" が設定されているか
- [ ] viewport meta が設定されているか
- [ ] すべてのHTMLが1ファイル内に収まっているか
- [ ] **全 `<button>` に `type="button"` が付いているか**

### 2. 仕様整合性チェック

PROTOTYPE.md に記載された以下の内容が実装されているか確認:

- [ ] 全画面が実装されているか
- [ ] 全機能が実装されているか
- [ ] 状態遷移が仕様通りか
- [ ] サンプルデータが含まれているか
- [ ] エラー状態・空状態の表示があるか

### 3. バグ防止チェック（ChatGPT/Codex指摘ベース）

以下のバグパターンに該当していないかチェック:

#### 隠れた要素の問題（P1: 最重要）
- [ ] **画面切り替えに `opacity`/`pointer-events` を使っていないか** → `display:none`/`display:block` を使うこと
- [ ] **段階表示ボタンに `opacity:0`/`pointer-events:none` を使っていないか** → `display:none` を使うこと
- [ ] **`inert` 属性に依存していないか** → `display:none` で十分。余計な複雑性を入れない

#### 状態管理の問題（P1）
- [ ] **各遷移関数の冒頭にガード節があるか** → `if (!state.currentXxx) { switchPhase('top'); return; }`
- [ ] **タイマーコールバックにフェーズガードがあるか** → `if (state.currentPhase !== '期待値') return;`
- [ ] **タイマーコールバックにフラグガードがあるか** → `if (state.isSkipped) return;`
- [ ] **スキップ後に次フェーズへ自動遷移するか** → スキップ=次フェーズへ進む

#### HTML/JSの問題（P2）
- [ ] **全 `<button>` に `type="button"` が付いているか** → デフォルトの submit によるリロード防止
- [ ] **`className` で上書きしていないか** → `classList.add`/`classList.remove` を使うこと
- [ ] **データ参照前にnullチェックがあるか** → `CHARACTERS[id]`、`SCENARIOS.find()` 等

### 4. よくある問題

以下のパターンに該当していないかチェック:

- [ ] `pre-line` でテキストが不正改行していないか
- [ ] `position: fixed` を phone-frame 内で使っていないか（absolute を使う）
- [ ] モーダル/トーストの z-index は適切か
- [ ] アコーディオンの max-height に `auto` を使っていないか
- [ ] flex 子要素に `min-height: 0` が必要な箇所はないか
- [ ] touchイベントに `{ passive: true }` を設定しているか
- [ ] localStorage の null チェックを行っているか
- [ ] **font-size: 10px や 11px など、12px未満のサイズを使っていないか**

### 5. フォントサイズ基準

| 用途 | 最低サイズ |
|------|-----------|
| 見出し1 | 24px |
| 見出し2 | 20px |
| 本文 | 17px |
| 本文（補助） | 16px |
| キャプション | 15px |
| 月・日付 | 14px |
| タブラベル | 12px（最小）|
| バッジ | 14px |

**12px未満は使用禁止。スマートフォンでの視認性を確保するため。**

## 判定

- **問題あり**: 指摘事項を出力し、`proto-05-html-builder` へ戻る
- **問題なし**: ユーザーレビューへ進む（修正依頼は `proto-ticket-lifecycle` で管理）

## 出力フォーマット

```markdown
## コードレビュー結果

### 判定: [OK / NG]

### コード品質
| カテゴリ | チェック項目 | 結果 |
|---------|-------------|------|
| CSS | z-index管理 | OK |
| JS | XSS対策 | NG - escapeHtml未使用 |

### 仕様整合性
| 項目 | 結果 |
|------|------|
| 画面S01実装 | OK |
| 空状態表示 | NG - 未実装 |

### 指摘事項（NG時）
1. [内容]
2. [内容]

### 次のアクション
[proto-html-builderに戻る / 人間レビューへ進む]
```

## ワークフロー

1. `prototype/index.html` と `prototype/PROTOTYPE.md` を読み込む
2. コード品質チェックを実行
3. 仕様整合性チェックを実行
4. 結果を出力
5. `prototype/prototype_status.md` を更新

## 外部レビュー（任意）

スキル完了後、`dev-codex-review` で外部AIによるセカンドオピニオンを取得可能:

```bash
codex review prototype/index.html "プロトタイプのHTML/CSS/JSをレビュー:
1. phone-frame内でposition:fixedを使っていないか
2. touchイベントに{ passive: true }があるか
3. localStorage.getItemのnullチェックがあるか
4. XSS対策
5. CSS変数の使用
6. z-index管理"
```

## 人間レビュー後の対応

コードレビュー完了後、ユーザーからの**あらゆるチケット・修正依頼**は `proto-ticket-lifecycle` を経由して処理する。

### 自動トリガー条件

index.html作成後、以下のいずれかに該当する場合は `proto-ticket-lifecycle` を実行:

- ユーザーからの修正依頼
- ユーザーからの改善提案
- ユーザーからの質問（仕様・実装に関するもの）
- ユーザーからのバグ報告

### 重要

**index.html完成後のやり取りは、すべて `prototype/tickets/` に記録する。**

直接index.htmlを編集する前に、必ずチケットファイルを作成すること。
