---
name: ref-gemini-api
description: |
  Gemini APIセットアップのリファレンス手順集。Google AI StudioでのAPIキー取得・
  環境変数設定・動作確認のステップバイステップ手順を提供する。prod-impl-planスキルから参照して使う。
  トリガー：「Gemini API設定」「Gemini APIキー」「AI API設定」「ref-gemini-api」
---

# Gemini API セットアップ リファレンス

実装計画書に貼り付けて使うリファレンス手順集。
各手順は `{{プロジェクト名}}` 等のプレースホルダを含む。実装計画に組み込む際にプロジェクト固有の値に置換する。

## プレースホルダ一覧

| プレースホルダ | 説明 | 例 |
|---------------|------|-----|
| `{{プロジェクト名}}` | Vercelプロジェクト名 | `mitsdake` |
| `{{本番URL}}` | 本番デプロイ先URL | `https://mitsdake.vercel.app` |
| `{{環境変数名}}` | APIキーの環境変数名 | `GEMINI_API_KEY` |

---

## REF-GM-01: APIキー取得 (👤)

> Google AI Studio で Gemini API キーを取得する

1. https://aistudio.google.com/ にアクセス
2. Googleアカウントでログイン
3. 左メニュー「Get API key」をクリック
4. 「Create API key」→「Create API key in new project」をクリック
   - または既存のGoogle Cloudプロジェクトを選択
5. 生成されたAPIキーをコピー（`AIza...`で始まる文字列）

> **注意**: APIキーは他人に共有しないこと。

**メモすべき情報**:
- 【GM1】APIキー: `AIza...`

---

## REF-GM-02: ローカル環境変数設定 (👤)

> 開発環境（ローカル）でAPIキーを使えるようにする

1. プロジェクトルートの `.env.local` を開く
2. 以下を追加:
   ```
   {{環境変数名}}=AIza...（【GM1】の値）
   ```
3. ファイルを保存
4. 開発サーバーを再起動（`npm run dev`）

---

## REF-GM-03: 本番環境変数設定 (👤)

> Vercel の環境変数にAPIキーを追加する

1. https://vercel.com/ にアクセス
2. プロジェクト「{{プロジェクト名}}」を選択
3. 「Settings」タブ → 「Environment Variables」
4. 以下を追加:
   - **Key**: `{{環境変数名}}`
   - **Value**: 【GM1】のAPIキー
   - **Environment**: `Production`, `Preview`, `Development` すべてにチェック
5. 「Save」をクリック

> **重要**: 環境変数の追加後は再デプロイが必要（ref-vercel-deploy REF-VC-03参照）

---

## REF-GM-04: 再デプロイと動作確認 (👤)

> 環境変数追加後の再デプロイと動作確認

**Step 1: 再デプロイ**
1. Vercelダッシュボード →「Deployments」タブ
2. 最新のデプロイの「...」メニュー → 「Redeploy」
3. 「Redeploy」ボタンをクリック
4. デプロイ完了を待つ（約1〜2分）

**Step 2: 動作確認**
1. `{{本番URL}}` にアクセス
2. AI機能を使用する操作を実行（例: 「AIで再提案」「AIで整理」等）
3. モックではなく実際のAI応答が返ることを確認
4. ブラウザのDevTools（F12）→ Consoleでエラーがないことを確認

**トラブルシューティング**:
| 症状 | 原因 | 対処 |
|------|------|------|
| AI機能がモックデータを返す | 環境変数未設定 or 再デプロイ未実施 | REF-GM-03を再確認、再デプロイ |
| 「API key not valid」エラー | APIキーが無効 | Google AI Studioで新しいキーを生成 |
| 「Quota exceeded」エラー | 無料枠の上限到達 | 翌日まで待つか、課金プランに変更 |
| 500エラー | APIキーの環境変数名が違う | コード内の参照名と一致しているか確認 |

---

## 料金について

- **無料枠**: 1分あたり60リクエスト、1日あたり1500リクエスト（目安）
- 個人利用であれば無料枠で十分
- 詳細: https://ai.google.dev/pricing

---

## 全体フロー

```
REF-GM-01: APIキー取得 → 【GM1】取得
    ↓
REF-GM-02: .env.local に追加（ローカル開発用）
    ↓
REF-GM-03: Vercel環境変数に追加（本番用）
    ↓
REF-GM-04: 再デプロイ + 動作確認
```

---

## 実装計画への組み込み例

```markdown
### X.X Gemini API設定 ⏳

> 参照: ref-gemini-api REF-GM-01〜04

| # | タスク | 実施者 | 完了条件 | 状態 |
|---|--------|--------|---------|------|
| X.X.1 | Google AI StudioでAPIキー取得 | 👤 | 【GM1】メモ | ⏳ |
| X.X.2 | .env.local に追加 | 👤 | ローカルでAI機能動作 | ⏳ |
| X.X.3 | Vercel環境変数に追加 | 👤 | 環境変数追加完了 | ⏳ |
| X.X.4 | 再デプロイ + 動作確認 | 👤 | 本番でAI機能動作 | ⏳ |
```
