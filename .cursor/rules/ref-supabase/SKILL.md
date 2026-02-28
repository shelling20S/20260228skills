---
name: ref-supabase
description: |
  Supabaseセットアップのリファレンス手順集。プロジェクト作成・API Keys取得・MCP接続・Auth設定の
  ステップバイステップ手順を提供する。prod-impl-planスキルから参照して使う。
  トリガー：「Supabaseセットアップ」「Supabase手順」「ref-supabase」
---

# Supabase セットアップ リファレンス

実装計画書に貼り付けて使うリファレンス手順集。
各手順は `{{プロジェクト名}}` 等のプレースホルダを含む。実装計画に組み込む際にプロジェクト固有の値に置換する。

## プレースホルダ一覧

| プレースホルダ | 説明 | 例 |
|---------------|------|-----|
| `{{プロジェクト名}}` | Supabaseプロジェクト名 | `mitsdake` |
| `{{リージョン}}` | プロジェクトリージョン | `Tokyo` |
| `{{トークン名}}` | Personal Access Tokenの名前 | `mitsdake-mcp` |
| `{{本番URL}}` | Vercel等の本番URL | `https://mitsdake.vercel.app` |
| `{{Supabase URL}}` | SupabaseプロジェクトURL | `https://xxxx.supabase.co` |
| `{{Callback URL}}` | Supabase Callback URL | `https://xxxx.supabase.co/auth/v1/callback` |
| `{{Google Client ID}}` | Google OAuthクライアントID | `xxxx.apps.googleusercontent.com` |
| `{{Google Client Secret}}` | Google OAuthクライアントシークレット | `GOCSPX-xxxx` |

---

## REF-SB-01: プロジェクト作成 (👤)

> Supabaseダッシュボードで新規プロジェクトを作成し、API Keysを取得する

**Step 1: プロジェクト作成**
1. https://supabase.com/dashboard にアクセス（GitHubでログイン）
2. 「New project」をクリック
3. Organization: 自分のOrganizationを選択
4. プロジェクト名: `{{プロジェクト名}}`
5. Database Password: 安全なパスワードを設定 → メモ
6. Region: `{{リージョン}}`
7. 「Create new project」をクリック
8. プロジェクトの初期化を待つ（1〜2分）

**Step 2: API Keys 取得**
1. ダッシュボード左メニュー「Project Settings」→「API」
2. 以下をメモ:
   - **Project URL**: `https://xxxx.supabase.co`
   - **anon public key**: `eyJhbGciOiJIUzI1NiIs...`
   - **service_role secret key**: `eyJhbGciOiJIUzI1NiIs...`

**Step 3: .env.local 作成**
1. プロジェクトルートに `.env.local` ファイルを作成
2. 以下の内容を記載:

```bash
NEXT_PUBLIC_SUPABASE_URL=https://xxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIs...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIs...
```

**メモすべき情報**:
- 【SB1】Project URL: `https://xxxx.supabase.co`
- 【SB2】anon key: `eyJhbGciOiJIUzI1NiIs...`
- 【SB3】service_role key: `eyJhbGciOiJIUzI1NiIs...`
- 【SB4】Database Password: `（設定したパスワード）`

**トラブルシューティング**:
| 症状 | 原因 | 対処 |
|------|------|------|
| プロジェクト作成が止まる | リージョン負荷 | 別リージョンで再試行 |
| API Keysが表示されない | 初期化未完了 | 数分待ってリロード |

---

## REF-SB-02: Personal Access Token 取得 (👤)

> Claude Code の Supabase MCP 接続に必要なトークンを取得する

1. https://supabase.com/dashboard/account/tokens にアクセス
2. 「Generate new token」をクリック
3. トークン名: `{{トークン名}}`
4. 発行されたトークンをメモ

> **注意**: トークンは一度しか表示されない。必ずメモすること。

**メモすべき情報**:
- 【SB5】Personal Access Token: `sbp_xxxx...`

---

## REF-SB-03: Supabase MCP セットアップ（Codex CLI OAuth） (👤+🤖)

> Codex CLI のグローバルMCP設定で Supabase MCP を有効化する。
> **推奨URLは `https://mcp.supabase.com/mcp`**（`project_ref` 付きURLは使わない）。

**Step 1: MCPサーバー登録** (🤖)
```bash
codex mcp add supabase --url "https://mcp.supabase.com/mcp"
```

**Step 2: OAuth認証** (👤)
```bash
codex mcp login supabase
```
1. ターミナルに表示されたURLをブラウザで開く
2. Supabaseで認可する
3. **ターミナルに成功メッセージが出るまで閉じない**

**Step 3: セッション再読み込み** (👤)
1. IDEで `Developer: Reload Window` を実行、またはCodexセッションを再起動

**Step 4: 接続状態確認** (🤖)
```bash
codex mcp list
```
→ `supabase` が `enabled` / `Auth: OAuth` ならOK

**Step 5: ツール疎通テスト** (🤖)
```text
mcp__supabase__list_projects()
```
→ プロジェクト一覧が返ればOK

**トラブルシューティング**:
| 症状 | 原因 | 対処 |
|------|------|------|
| `Auth required` が出る | OAuth認証が保存されていない、または古いセッション | `codex mcp login supabase` を再実行し、成功表示まで待つ。完了後にIDE再読み込み |
| `unknown MCP server "supabase"` | セッションが古く設定を未反映 | `codex mcp list` で存在確認後、IDE再読み込み/新規セッション開始 |
| `resources/list ... Method not found` | Supabase MCPはresources API未対応 | 想定動作。`mcp__supabase__*` ツールを直接使う |
| 接続が不安定・URL設定が怪しい | 旧設定や誤URLが残っている | `codex mcp remove supabase` → `codex mcp add supabase --url "https://mcp.supabase.com/mcp"` → `codex mcp login supabase` |

---

## REF-SB-04: DBスキーマ適用 (🤖)

> マイグレーションファイルを作成し、Supabase MCP 経由でスキーマを適用する

**Step 1: マイグレーションSQL作成** (🤖)
- `supabase/migrations/` ディレクトリにSQLファイルを作成

**Step 2: スキーマ適用** (🤖)
```
mcp__supabase__apply_migration(project_id, name, query)
```

**Step 3: テーブル確認** (🤖)
```
mcp__supabase__list_tables(project_id, schemas: ["public"])
```
→ 作成したテーブルが一覧に表示されればOK

---

## REF-SB-05: Auth設定（Google OAuth連携） (👤)

> Supabase AuthenticationでGoogle OAuth Providerを有効化する。
> 前提: Vercelデプロイ済み（【E2】本番URL）、Google Cloud OAuth設定済み（【G1】【G2】）

**Step 1: Site URLの変更**
1. https://supabase.com/dashboard にアクセス（GitHubログイン）
2. プロジェクト `{{プロジェクト名}}` を選択
3. 左メニュー「Authentication」→「URL Configuration」
4. **Site URL** を `{{本番URL}}` に変更
5. 「Save changes」

**Step 2: Redirect URLsの設定**
1. 同じ画面で「Add URL」をクリック
2. **1つ目**: `{{本番URL}}/auth/callback`（本番用）
3. **2つ目**: `http://localhost:3000/auth/callback`（開発用）
4. 「Save changes」

**Step 3: Google Provider有効化**
1. 左メニュー「Authentication」→「Sign In / Providers」
2. 「Google」を探してクリック
3. 「Enable sign in with Google」を **ON**
4. **Client ID**: `{{Google Client ID}}`（【G1】の値）
5. **Client Secret**: `{{Google Client Secret}}`（【G2】の値）
6. 「Save」をクリック

**Step 4: OAuth Scopes設定（カレンダー連携が必要な場合）**
1. 同じ「Google」Providerの設定画面で **「OAuth Scopes」フィールド** を確認
2. 以下のスコープを追加（スペース区切りで入力）:
   ```
   https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/calendar.events.readonly
   ```
3. 「Save」をクリック

> **注意**: このスコープ設定がないと、Googleログインは成功しても `provider_token` が取得できず、カレンダーデータを取得できません。

**メモすべき情報**:
- 【SB6】Supabase Callback URL: `{{Supabase URL}}/auth/v1/callback`

**トラブルシューティング**:
| 症状 | 原因 | 対処 |
|------|------|------|
| Redirect URI mismatch | URLの設定不一致 | Google Cloud側とSupabase側のURLを再確認 |
| provider_token が null | OAuth Scopes未設定 | Step 4を実施 |
| 「テストユーザーのみ」エラー | Google Cloud側の制限 | テストユーザーに自分を追加 |

---

## REF-SB-06: Auth動作確認 (👤)

> OAuth設定完了後の認証フローテスト

**開発環境テスト**:

以下のURLにアクセスして、Googleログイン後にリダイレクトされることを確認:
```
{{Supabase URL}}/auth/v1/authorize?provider=google&redirect_to=http://localhost:3000/auth/callback
```
→ Googleログイン後、`localhost:3000` にリダイレクトされればOK

**本番環境テスト**:
```
{{Supabase URL}}/auth/v1/authorize?provider=google&redirect_to={{本番URL}}/auth/callback
```
→ Googleログイン後、本番URLにリダイレクトされればOK

**トラブルシューティング**:
- Redirect URI エラー → Google Cloud / Supabase の設定を再確認
- 「テストユーザーのみ」エラー → Google Cloud でテストユーザーに自分を追加
- ブラウザのDevTools（F12）でエラー内容を確認

---

## 実装計画への組み込み例

```markdown
### X.X Supabase プロジェクト作成 ⏳

> 参照: ref-supabase REF-SB-01

| # | タスク | 実施者 | 完了条件 | 状態 |
|---|--------|--------|---------|------|
| X.X.1 | プロジェクト作成 + API Keys取得 | 👤 | 【SB1】〜【SB3】メモ | ⏳ |
| X.X.2 | .env.local 作成 | 👤 | 環境変数設定完了 | ⏳ |
| X.X.3 | Personal Access Token 取得 | 👤 | 【SB5】メモ | ⏳ |
| X.X.4 | MCPサーバー登録 | 🤖 | `codex mcp add` 成功 | ⏳ |
| X.X.5 | OAuth認証 | 👤 | `codex mcp login` 認可完了 | ⏳ |
| X.X.6 | IDE再読み込み | 👤 | 新セッションへ反映 | ⏳ |
| X.X.7 | 接続テスト | 🤖 | `list_projects` 成功 | ⏳ |
| X.X.8 | DBスキーマ適用 | 🤖 | テーブル作成完了 | ⏳ |
```
