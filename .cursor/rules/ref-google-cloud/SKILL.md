---
name: ref-google-cloud
description: |
  Google Cloud セットアップのリファレンス手順集。OAuth同意画面・クライアントID作成・API有効化・
  スコープ設定のステップバイステップ手順を提供する。prod-impl-planスキルから参照して使う。
  トリガー：「Google Cloudセットアップ」「OAuth設定」「Google Cloud手順」「ref-google-cloud」
---

# Google Cloud セットアップ リファレンス

実装計画書に貼り付けて使うリファレンス手順集。
各手順は `{{プロジェクト名}}` 等のプレースホルダを含む。実装計画に組み込む際にプロジェクト固有の値に置換する。

## プレースホルダ一覧

| プレースホルダ | 説明 | 例 |
|---------------|------|-----|
| `{{プロジェクト名}}` | Google Cloudプロジェクト名 | `mitsdake` |
| `{{アプリ名}}` | OAuth同意画面のアプリ名 | `MITSDAKE` |
| `{{クライアント名}}` | OAuthクライアント名 | `mitsdake-web-client` |
| `{{本番URL}}` | 本番デプロイ先URL | `https://mitsdake.vercel.app` |
| `{{Supabase Callback URL}}` | SupabaseのOAuth callback | `https://xxxx.supabase.co/auth/v1/callback` |

---

## REF-GC-01: プロジェクト作成 (👤)

> Google Cloud Console で新規プロジェクトを作成する

1. https://console.cloud.google.com/ にアクセス（Googleログイン）
2. 画面上部のプロジェクト選択 → 「新しいプロジェクト」
3. プロジェクト名: `{{プロジェクト名}}`
4. 「作成」をクリック
5. ダッシュボードに遷移 → 作成したプロジェクトを選択

---

## REF-GC-02: OAuth同意画面の構成 (👤)

> OAuth認証に必要な同意画面を設定する

1. 検索バーで「api」と入力 →「APIとサービス」を選択
2. 「認証情報」→「認証情報を作成」→「OAuthクライアントID」
3. 「同意画面を構成」→「開始」をクリック
4. アプリ名: `{{アプリ名}}`
5. ユーザーサポートメール: 自分のメールアドレスを選択 → 「次へ」
6. 「外部」を選択 → 「次へ」
7. 連絡先メールアドレスを入力 → 「次へ」
8. ポリシーに同意 → 「続行」→「作成」

---

## REF-GC-03: OAuthクライアントID作成 (👤)

> ウェブアプリケーション用のOAuthクライアントIDを作成する

1. 「OAuthクライアントを作成」ボタンをクリック
2. アプリケーションの種類: 「ウェブアプリケーション」
3. 名前: `{{クライアント名}}`
4. **承認済みのJavaScript生成元**:
   - 「URIを追加」→ `{{本番URL}}`（本番URL）
   - 「URIを追加」→ `http://localhost:3000`（開発用）
5. **承認済みのリダイレクトURI**:
   - 「URIを追加」→ `{{Supabase Callback URL}}`
6. 「作成」をクリック
7. **クライアントID** と **クライアントシークレット** が表示される → メモ → 「OK」

**メモすべき情報**:
- 【G1】クライアントID: `xxxx.apps.googleusercontent.com`
- 【G2】クライアントシークレット: `GOCSPX-xxxx`

**トラブルシューティング**:
| 症状 | 原因 | 対処 |
|------|------|------|
| 「同意画面を構成」が表示されない | 既に構成済み | そのままクライアントID作成へ進む |
| リダイレクトURI エラー | URLの末尾スラッシュ | スラッシュの有無を統一する |

---

## REF-GC-04: API有効化 (👤)

> 必要なGoogle APIを有効化する

### Google Calendar API

1. 左メニュー「APIとサービス」→「ライブラリ」
2. 検索で「Google Calendar API」を検索
3. 「Google Calendar API」をクリック
4. 「有効にする」ボタンをクリック

### その他のAPI（必要に応じて）

同じ手順で以下のAPIも有効化可能:
- Google Drive API
- Google Sheets API
- Gmail API

---

## REF-GC-05: スコープ設定 (👤)

> OAuth同意画面で必要なスコープ（アクセス権限）を設定する

1. 左メニュー「OAuth同意画面」→「データアクセス」
2. 「スコープを追加または削除」をクリック
3. 以下にチェック:

**基本スコープ（認証用）**:
- `../auth/userinfo.email`
- `../auth/userinfo.profile`
- `openid`

**カレンダー連携用（必要な場合）**:
- `../auth/calendar.readonly`
- `../auth/calendar.events.readonly`

**カレンダー書き込み用（必要な場合）**:
- `../auth/calendar`
- `../auth/calendar.events`

4. 「更新」→「Save」

---

## REF-GC-06: テストユーザー追加 (👤)

> 公開前（テストモード）の場合、テストユーザーの登録が必要

1. 左メニュー「OAuth同意画面」→「対象」をクリック
2. 「+ Add users」をクリック
3. 自分のGoogleアカウントのメールアドレスを入力
4. 「追加」→「保存」

> **注意**: テストモード（公開前）では、登録したテストユーザーのみがOAuth認証を使用可能。本番公開後はこの制限は解除される。

**トラブルシューティング**:
| 症状 | 原因 | 対処 |
|------|------|------|
| 「このアプリはテスト中」エラー | テストユーザー未追加 | 本手順を実施 |
| ユーザー追加できない | 上限到達（100名） | 不要なユーザーを削除 |

---

## 全体フロー

```
REF-GC-01: プロジェクト作成
    ↓
REF-GC-02: OAuth同意画面
    ↓
REF-GC-03: OAuthクライアントID作成 → 【G1】【G2】取得
    ↓
REF-GC-04: API有効化（Calendar等）
    ↓
REF-GC-05: スコープ設定
    ↓
REF-GC-06: テストユーザー追加
```

---

## 実装計画への組み込み例

```markdown
### X.X Google Cloud OAuth設定 ⏳

> 参照: ref-google-cloud REF-GC-01〜06

| # | タスク | 実施者 | 完了条件 | 状態 |
|---|--------|--------|---------|------|
| X.X.1 | Google Cloudプロジェクト作成 | 👤 | プロジェクト作成完了 | ⏳ |
| X.X.2 | OAuth同意画面の構成 | 👤 | 同意画面設定完了 | ⏳ |
| X.X.3 | OAuthクライアントID作成 | 👤 | 【G1】【G2】メモ | ⏳ |
| X.X.4 | Google Calendar API有効化 | 👤 | API有効化完了 | ⏳ |
| X.X.5 | スコープ設定 | 👤 | カレンダースコープ追加 | ⏳ |
| X.X.6 | テストユーザー追加 | 👤 | 自分のアカウント追加 | ⏳ |
```
