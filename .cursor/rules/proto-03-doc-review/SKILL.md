---
name: proto-03-doc-review
description: |
  PROTOTYPE.mdの品質チェック（自動実行）。要件網羅・矛盾・機能欠落・バグ防止設計・古い情報を検査する。
  OK/MINOR/NGの3段階判定。OK/MINORなら proto-04-design-gallery へ進む。パイプライン: proto-02-design → **proto-03-doc-review** → proto-04-design-gallery。
  トリガー：proto-02-design完了後に自動実行、「ドキュメントレビュー」「仕様書チェック」「品質チェック」「proto-doc-review」
---

# Proto Doc Review

`prototype/PROTOTYPE.md` の品質をチェックする（自動実行）。

## ファイルパス規約

| ファイル | パス |
|---------|------|
| 仕様書（現在） | `prototype/PROTOTYPE.md` |
| 仕様書（過去） | `prototype/history/PROTOTYPE_v[N].md` |
| ステータス | `prototype/prototype_status.md` |

**バージョン履歴**: 新バージョン作成時、前バージョンを `prototype/history/` に `PROTOTYPE_v[N].md` として保存する。

## チェック項目

### 1. 要件網羅チェック
PROTOTYPE.mdの「概要」セクション（1.1〜1.4）の全項目が画面仕様に反映されているか確認。

**チェック方法:**
- 概要セクションの主要機能リストを抽出
- 画面仕様で対応する機能を確認
- 未対応の機能があれば指摘

### 2. 矛盾チェック
データモデルと画面仕様の整合性を確認。

**チェック方法:**
- データモデルのフィールドが画面で使用されているか
- 画面で表示するデータがモデルに定義されているか
- 状態遷移とデータ更新のタイミングが一致するか

### 3. 機能欠落チェック
前バージョンから消えた機能がないか確認（v2以降）。

**チェック方法:**
- `prototype/history/PROTOTYPE_v[N-1].md` と現在の `prototype/PROTOTYPE.md` を比較
- 削除された機能が意図的か確認
- 意図的でなければ復元を指示
- **履歴がない場合はスキップ**

### 4. バグ防止設計チェック（必須）
状態遷移セクションが実装時のバグを防ぐ設計になっているか確認。

**チェック方法:**
- 各画面遷移に「前提条件」が明記されているか（例: 「chatフェーズ完了済み、かつscenarioデータが存在するとき」）
- 異常時の動作が明記されているか（例: 「データがnullの場合はトップ画面に戻す」）
- ボタンの表示条件が明記されているか（例: 「投票アニメーション完了後に表示」）
- 「見えないが操作可能な要素」がないか（opacity:0のボタン等 → display:noneに変更すべき）
- 全`<button>`に`type="button"`が必要であることが技術仕様に記載されているか

### 5. 最新情報のみチェック
廃止済みの情報が残っていないか確認。

**チェック方法:**
- 「廃止」「削除」「旧」などのキーワード検索
- 該当箇所の削除を指示

## 判定

- **OK**: 問題なし → `proto-04-design-gallery` へ進む
- **MINOR**: 軽微な指摘のみ → 修正後に `proto-04-design-gallery` へ進む（再レビュー不要）
- **NG**: 重大な問題あり → 指摘事項を出力し、`proto-02-design` へ戻る

## 出力フォーマット

```markdown
## ドキュメントレビュー結果

### 判定: [OK / MINOR / NG]

### 指摘事項
1. [カテゴリ] [重大度: MINOR/NG] [内容]
2. ...

### 次のアクション
[proto-04-design-galleryへ進む / 軽微な修正後にproto-04へ進む / proto-02-designに戻る]
```

## ワークフロー

1. `prototype/PROTOTYPE.md` を読み込む
2. `prototype/history/` から前バージョンを探す（あれば）
3. 5つのチェックを実行
4. 結果を出力
5. `prototype/prototype_status.md` を更新

## 外部レビュー（任意）

スキル完了後、`dev-codex-review` で外部AIによるセカンドオピニオンを取得可能:

```bash
codex review --uncommitted
```
