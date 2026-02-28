# 差別化デザインパターン

**「普通」に見えるデザインを避け、記憶に残るプロトタイプを作るための必須パターン集。**

## なぜ「普通」になるのか？

| 原因 | 症状 | 解決策 |
|-----|------|-------|
| 機能説明ファースト | ヘッダーに「〜できるサービス」と書いてしまう | 共感ファースト：ユーザーの悩みから始める |
| 感情への訴えがない | 論理的な説明ばかり | 不安・焦り・期待に寄り添うコピー |
| よくあるSaaSカラー | 青一辺倒、グレー基調 | アンバー、コーラル、グリーン等で差別化 |
| Before/Afterがない | 価値が抽象的 | 具体的な変化を視覚化する |
| メタファー未活用 | サービス名が飾り | 名前の意味をデザイン・アニメーションに |

---

## 差別化チェックリスト（実装前に確認）

- [ ] **共感ファースト**: ファーストビューで「あなたの気持ち、わかります」と伝えているか
- [ ] **メタファーの視覚化**: サービス名/コンセプトがアニメーションや図で表現されているか
- [ ] **Before/After**: ユーザーの変化が一目でわかるセクションがあるか
- [ ] **色の差別化**: 「青+カード+アイコン」のSaaSテンプレ回避しているか
- [ ] **具体的な数字**: 「5分で完成」「3つのアクション」「1,000人以上」等の約束があるか

---

## 共感ファーストの実装例

```html
<!-- ❌ 機能ファースト（普通） -->
<h1>あなたのキャリアを可視化するサービス</h1>
<p>AIがあなたのスキルを分析し、最適なキャリアパスを提案します。</p>

<!-- ✅ 共感ファースト（差別化） -->
<div class="empathy-section">
  <p class="empathy-quote fade-in">"今の仕事、このままでいいのかな..."</p>
  <p class="empathy-quote fade-in">"転職したいけど、何から始めれば..."</p>
  <p class="empathy-quote fade-in">"自分の強み、うまく言葉にできない..."</p>
</div>
<p class="empathy-response">その迷い、一緒に解決しましょう。</p>
```

---

## メタファーアニメーション例

```css
/* コンパス（方向を見つける） */
@keyframes compass-settle {
  0% { transform: rotate(-30deg); }
  20% { transform: rotate(20deg); }
  40% { transform: rotate(-10deg); }
  60% { transform: rotate(5deg); }
  80% { transform: rotate(-2deg); }
  100% { transform: rotate(0deg); }
}

/* 種が芽吹く（成長） */
@keyframes sprout {
  0% { transform: scaleY(0); transform-origin: bottom; }
  100% { transform: scaleY(1); }
}

/* 扉が開く（新しい可能性） */
@keyframes door-open {
  0% { transform: perspective(800px) rotateY(0); }
  100% { transform: perspective(800px) rotateY(-80deg); }
}
```

---

## Before/After パターン

```html
<div class="transformation">
  <div class="before-card">
    <span class="label">Before</span>
    <p>"自分の強みがわからない..."</p>
    <span class="mood sad">😔</span>
  </div>
  <div class="arrow">→</div>
  <div class="after-card">
    <span class="label">After</span>
    <p>"3つの強みを言語化できた！"</p>
    <span class="mood happy">😊</span>
  </div>
</div>
```

---

## 差別化カラーパレット例

```css
/* アンバー系（温かみ・信頼） */
--accent: #F59E0B;
--accent-light: #FEF3C7;
--accent-dark: #92400E;

/* コーラル系（親しみ・活力） */
--accent: #F97316;
--accent-light: #FFF7ED;
--accent-dark: #C2410C;

/* ティール系（成長・バランス） */
--accent: #14B8A6;
--accent-light: #CCFBF1;
--accent-dark: #0F766E;
```

---

## frontend-design ガイドライン

### タイポグラフィ
- **Google Fonts使用**: 日本語: `Zen Maru Gothic`（あたたかい）、`Noto Sans JP`（モダン）、`M PLUS Rounded 1c`（やわらかい）

### カラー & テーマ
- **グラデーション活用**: 背景、ボタン、バッジにlinear-gradientを使用
- **CSS変数で一元管理**: `--accent`, `--accent-dark`, `--accent-light`, `--accent-glow` など

### モーション
- **ロード時アニメーション**: カードは `fadeInUp` で順番に登場（animation-delay使用）
- **インタラクション**: タップ時 `scale(0.98)`、ホバー時シャドウ変化

### 空間構成
- **大きめの角丸**: カード 20px、ボタン 14px、モーダル 28px
- **十分な余白**: padding は spacing変数で管理

### ビジュアルディテール
- **背景テクスチャ**: 微細なグラデーション（radial-gradient overlay）
- **タブバー**: `backdrop-filter: blur(20px)` で半透明効果
- **アバター**: グラデーション背景 + グロー効果（box-shadow with accent-glow）
