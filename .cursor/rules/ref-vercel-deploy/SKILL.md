---
name: ref-vercel-deploy
description: |
  Vercelダッシュボードでのデプロイ手順リファレンス。プロジェクト作成・環境変数設定・デプロイ実行の
  ステップバイステップ手順を提供する。prod-impl-planスキルから参照して使う。
  トリガー：「Vercelデプロイ手順」「Vercelセットアップ」「ref-vercel-deploy」
---

# Vercel デプロイ リファレンス

実装計画書に貼り付けて使うリファレンス手順集。
各手順は `{{プロジェクト名}}` 等のプレースホルダを含む。実装計画に組み込む際にプロジェクト固有の値に置換する。

> **注意**: Vercel CLIでの新規プロジェクト作成は禁止。必ずダッシュボードから作成すること。
> CLI操作は `dev-vercel-cli` スキルを参照。

## プレースホルダ一覧

| プレースホルダ | 説明 | 例 |
|---------------|------|-----|
| `{{プロジェクト名}}` | Vercelプロジェクト名 | `mitsdake` |
| `{{GitHubリポジトリ}}` | GitHubリポジトリパス | `kiyogon/20251206mitsdake` |
| `{{フレームワーク}}` | フレームワーク名 | `Next.js` |

---

## REF-VC-01: プロジェクト作成・初回デプロイ (👤)

> Vercelダッシュボードで新規プロジェクトを作成し、GitHubリポジトリを連携してデプロイする

**Step 1: Vercelにログイン**
1. https://vercel.com にアクセス
2. 「Log In」→「Continue with GitHub」でGitHubアカウントでログイン
3. 初回の場合は認可を許可

**Step 2: 新規プロジェクト作成**
1. ダッシュボードで「Add New...」→「Project」をクリック
2. 「Import Git Repository」セクションで「Continue with GitHub」
3. リポジトリ一覧から `{{GitHubリポジトリ}}` を探す
   - 表示されない場合: 「Adjust GitHub App Permissions」でアクセス許可を追加
4. 該当リポジトリの「Import」ボタンをクリック

**Step 3: プロジェクト設定**
1. **Project Name**: `{{プロジェクト名}}`（URLに使われる）
2. **Framework Preset**: `{{フレームワーク}}`（自動検出されるはず）
3. **Root Directory**: `./`（デフォルトのまま）
4. **Build and Output Settings**: デフォルトのまま

**Step 4: 環境変数設定**
1. 「Environment Variables」セクションを展開
2. `.env.local` の内容をコピーして、Keyの入力欄に貼り付け
   → 自動で Key/Value に分割される
3. 必要な環境変数がすべて追加されていることを確認

**Step 5: デプロイ実行**
1. 「Deploy」ボタンをクリック
2. ビルドが開始される（2〜3分程度）
3. 「Congratulations!」が表示されたら成功
4. 「Continue to Dashboard」をクリック

**Step 6: 本番URLを確認・メモ**
1. ダッシュボードの「Domains」セクションで本番URLを確認
2. 例: `https://{{プロジェクト名}}.vercel.app`

**メモすべき情報**:
- 【E1】プロジェクト名: `{{プロジェクト名}}`
- 【E2】デプロイ先URL: `https://{{プロジェクト名}}.vercel.app`
- 【E3】Callback URL: `https://{{プロジェクト名}}.vercel.app/auth/callback`

**トラブルシューティング**:
| 症状 | 原因 | 対処 |
|------|------|------|
| ビルドエラー | 依存関係 or コードエラー | Vercelのビルドログを確認 |
| リポジトリが見つからない | 権限不足 | GitHub App Permissionsでアクセス許可を追加 |
| 環境変数エラー | 余分な空白や改行 | 値をトリムして再入力 |
| Framework Presetが検出されない | package.json不足 | 手動で選択 |

---

## REF-VC-02: 環境変数の追加・変更 (👤)

> デプロイ済みプロジェクトに環境変数を追加・変更する

1. https://vercel.com/ にアクセス
2. プロジェクト「{{プロジェクト名}}」を選択
3. 「Settings」タブ → 「Environment Variables」
4. 新規追加の場合:
   - **Key**: 環境変数名
   - **Value**: 値
   - **Environment**: `Production`, `Preview`, `Development` から選択（通常はすべてチェック）
5. 「Save」をクリック

> **重要**: 環境変数の追加・変更後は再デプロイが必要（REF-VC-03参照）

---

## REF-VC-03: 再デプロイ (👤)

> 環境変数変更後や手動で再デプロイしたい場合

1. https://vercel.com/ にアクセス
2. プロジェクト「{{プロジェクト名}}」を選択
3. 「Deployments」タブを開く
4. 最新のデプロイの「...」メニュー → 「Redeploy」
5. 「Redeploy」ボタンをクリック
6. デプロイ完了を待つ（約1〜2分）

> **補足**: git push でも自動デプロイされる（GitHub連携済みの場合）

---

## REF-VC-04: カスタムドメイン設定 (👤)（オプション）

> 独自ドメインを Vercel プロジェクトに紐付ける

1. https://vercel.com/ にアクセス
2. プロジェクト「{{プロジェクト名}}」を選択
3. 「Settings」タブ → 「Domains」
4. ドメイン名を入力 → 「Add」
5. 表示されたDNSレコードをドメイン管理サービスに設定:
   - **CNAME**: `cname.vercel-dns.com`
   - または **A**: `76.76.21.21`
6. DNS反映を待つ（数分〜最大48時間）
7. Vercelダッシュボードで「Valid Configuration」と表示されれば完了

---

## 全体フロー

```
REF-VC-01: プロジェクト作成・初回デプロイ → 【E1】【E2】【E3】取得
    ↓
（外部サービス設定：Google Cloud、Supabase Auth等）
    ↓
REF-VC-02: 追加の環境変数設定（必要に応じて）
    ↓
REF-VC-03: 再デプロイ
    ↓
REF-VC-04: カスタムドメイン設定（オプション）
```

---

## 実装計画への組み込み例

```markdown
### X.X Vercel プロジェクト作成・デプロイ ⏳ ⭐最初に実行

> 参照: ref-vercel-deploy REF-VC-01

| # | タスク | 実施者 | 完了条件 | 状態 |
|---|--------|--------|---------|------|
| X.X.1 | Vercelプロジェクト作成 + 初回デプロイ | 👤 | 【E1】【E2】メモ | ⏳ |
| X.X.2 | 本番URL確認 | 👤 | 【E3】メモ | ⏳ |
```
