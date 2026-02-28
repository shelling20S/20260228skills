# CSSパターン集

## HTML基本構造

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>[プロジェクト名]</title>
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[フォント名]&display=swap" rel="stylesheet">
  <style>
    :root {
      /* Colors */
      --bg-primary: #FFFBF7;
      --bg-card: #FFFFFF;
      --text-primary: #3D3D3D;
      --text-secondary: #7A7A7A;
      --accent: #E8A5A5;
      --accent-dark: #D48888;
      --accent-light: #FDF0F0;
      --accent-glow: rgba(232, 165, 165, 0.3);

      /* Shadows */
      --shadow-sm: 0 2px 8px rgba(180, 140, 120, 0.08);
      --shadow-md: 0 4px 16px rgba(180, 140, 120, 0.08);
      --shadow-card: 0 2px 12px rgba(180, 140, 120, 0.08);

      /* Transitions */
      --transition-fast: 0.15s ease;
      --transition-normal: 0.25s ease;
    }
  </style>
</head>
<body>
  <div class="phone-frame">
    <!-- 画面コンテンツ -->
  </div>
  <script>/* JS here */</script>
</body>
</html>
```

---

## phone-frame

```css
.phone-frame {
  width: 375px; height: 812px;
  margin: 0 auto;
  overflow: hidden;
  position: relative;
}
```

---

## ボトムシート

```css
/* phone-frame内では absolute を使用（fixed は viewport 基準になるため） */
.bottom-sheet {
  position: absolute; bottom: 0; left: 0; right: 0;
  background: var(--surface);
  border-radius: 16px 16px 0 0;
  transform: translateY(100%);
  transition: transform 0.3s ease;
}
.bottom-sheet.open { transform: translateY(0); }
```

---

## トースト

```css
/* phone-frame内では absolute を使用 */
.toast {
  position: absolute; bottom: 80px; left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  border-radius: 8px;
  opacity: 0; transition: opacity 0.3s;
}
.toast.show { opacity: 1; }
```

---

## アニメーション（必須）

```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

/* カードに適用（順番に登場） */
.card {
  animation: fadeInUp 0.5s ease backwards;
}
.card:nth-child(1) { animation-delay: 0.05s; }
.card:nth-child(2) { animation-delay: 0.1s; }
.card:nth-child(3) { animation-delay: 0.15s; }

/* インタラクション */
.card:active { transform: scale(0.98); }
.card:hover { box-shadow: var(--shadow-card-hover); }
```

---

## グラデーション・グロー（必須）

```css
/* ボタン */
.btn-primary {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%);
  box-shadow: 0 4px 16px var(--accent-glow);
}

/* アバター */
.avatar {
  background: linear-gradient(135deg, var(--accent-light) 0%, #FFE4E4 100%);
  box-shadow: 0 2px 8px var(--accent-glow);
}

/* タブバー（blur効果） */
.tab-bar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}
```

---

## タイポグラフィ（最低フォントサイズ）

| 用途 | 最低サイズ | 推奨ウェイト | 備考 |
|------|-----------|-------------|------|
| 見出し1 | 24px | 700 | ヘッダー、詳細画面名 |
| 見出し2 | 20px | 600 | 月表示、モーダルタイトル |
| 本文 | 17px | 400 | カード名、コメント |
| 本文（補助） | 16px | 400 | 説明文、トグルラベル |
| キャプション | 15px | 400 | フォームラベル、ボタン |
| 月・日付 | 14px | 500 | カード内サブ情報 |
| タブラベル | 12px | 400 | タブバー（これ以上小さくしない） |
| バッジ | 14px | 500 | ステータスバッジ |

### 重要なルール
- **12px未満は使用禁止**（タブラベルが最小）
- line-height は本文で 1.6〜1.8 を確保

---

## フォールバックテンプレート（DESIGN_DECISION.mdがない場合）

| テンプレート | 適したプロジェクト | 主なカラー |
|-------------|-------------------|-----------|
| retro | 温かみ・落ち着き、30-50代向け | クリーム + テラコッタ |
| minimal | 洗練・プロ向け、ビジネス系 | 白 + 黒 |
| dark | エンジニア向け、長時間利用 | ダーク + ブルー |
| nature | 癒し・ウェルネス系 | アイボリー + グリーン |
| pop | 若者向け・カジュアル | 白 + パープル |
