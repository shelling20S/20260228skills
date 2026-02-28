# 差別化デザインパターン集

「普通」を脱して記憶に残るプロトタイプを作るためのパターン集。

## 目次
1. [共感ファーストパターン](#共感ファーストパターン)
2. [メタファー活用パターン](#メタファー活用パターン)
3. [Before/Afterパターン](#beforeafterパターン)
4. [カラー差別化パターン](#カラー差別化パターン)
5. [具体的約束パターン](#具体的約束パターン)
6. [アンチパターン集](#アンチパターン集)

---

## 共感ファーストパターン

### 原則
- ファーストビューで機能を説明しない
- ユーザーの悩み・不安・期待を言葉にする
- 「わかってくれている」と感じさせる

### パターン1: 内なる声の表出

```html
<div class="empathy-section">
  <p class="empathy-quote">"今の仕事、このままでいいのかな..."</p>
  <p class="empathy-quote">"転職したいけど、何から始めれば..."</p>
  <p class="empathy-quote">"自分の強み、うまく言葉にできない..."</p>
</div>
<p class="empathy-response">その迷い、一緒に解決しましょう。</p>
```

```css
.empathy-quote {
  font-size: 18px;
  color: var(--text-secondary);
  font-style: italic;
  opacity: 0;
  animation: fadeIn 0.8s ease forwards;
}
.empathy-quote:nth-child(1) { animation-delay: 0.5s; }
.empathy-quote:nth-child(2) { animation-delay: 1.2s; }
.empathy-quote:nth-child(3) { animation-delay: 1.9s; }
.empathy-response {
  font-size: 24px;
  font-weight: 700;
  color: var(--accent);
  margin-top: 24px;
}
```

### パターン2: ペルソナの問いかけ

```html
<div class="persona-question">
  <img src="avatar.png" class="persona-avatar" alt="">
  <div class="speech-bubble">
    <p>"副業を始めたいけど、何をアピールすればいいんだろう..."</p>
  </div>
</div>
```

### パターン3: 状況の描写

```html
<div class="situation">
  <p class="time">深夜2時</p>
  <p class="scene">転職サイトを開いては閉じる。</p>
  <p class="scene">「まだ準備ができていない」と自分に言い聞かせる。</p>
  <p class="question">...いつまで待つ？</p>
</div>
```

---

## メタファー活用パターン

### 原則
- サービス名/コンセプトをデザインに落とし込む
- アニメーションで意味を伝える
- 単なる飾りではなく、体験の一部にする

### パターン1: コンパス（方向を見つける）

```css
@keyframes compass-settle {
  0% { transform: rotate(-30deg); }
  20% { transform: rotate(20deg); }
  40% { transform: rotate(-10deg); }
  60% { transform: rotate(5deg); }
  80% { transform: rotate(-2deg); }
  100% { transform: rotate(0deg); }
}

.compass-needle {
  animation: compass-settle 2s ease-out forwards;
}
```

```html
<div class="compass">
  <div class="compass-body">🧭</div>
  <div class="compass-needle" style="font-size: 48px;">↑</div>
</div>
<p class="compass-message">あなたの進むべき方向が見つかる</p>
```

### パターン2: 種が芽吹く（成長）

```css
@keyframes sprout {
  0% {
    transform: scaleY(0);
    transform-origin: bottom;
    opacity: 0.5;
  }
  50% { opacity: 1; }
  100% {
    transform: scaleY(1);
    opacity: 1;
  }
}

.plant-icon {
  animation: sprout 1.5s ease-out forwards;
}
```

### パターン3: 扉が開く（可能性）

```css
@keyframes door-open {
  0% {
    transform: perspective(800px) rotateY(0);
  }
  100% {
    transform: perspective(800px) rotateY(-80deg);
  }
}

.door {
  transform-origin: left;
  animation: door-open 1s ease-out forwards;
}
```

### パターン4: 霧が晴れる（明確化）

```css
@keyframes fog-clear {
  0% { filter: blur(8px); opacity: 0.3; }
  100% { filter: blur(0); opacity: 1; }
}

.clarity-text {
  animation: fog-clear 2s ease-out forwards;
}
```

### パターン5: パズルが揃う（整理）

```css
@keyframes puzzle-fit {
  0% {
    transform: translate(20px, -20px) rotate(15deg);
    opacity: 0;
  }
  100% {
    transform: translate(0, 0) rotate(0);
    opacity: 1;
  }
}

.puzzle-piece:nth-child(1) { animation-delay: 0s; }
.puzzle-piece:nth-child(2) { animation-delay: 0.3s; }
.puzzle-piece:nth-child(3) { animation-delay: 0.6s; }
```

---

## Before/Afterパターン

### 原則
- 抽象的な価値を具体的な変化で見せる
- 感情の変化も表現する
- 対比を視覚的に明確にする

### パターン1: カード対比

```html
<div class="transformation">
  <div class="before-card">
    <span class="label">Before</span>
    <div class="content">
      <span class="emoji">😔</span>
      <p>"自分の強みがわからない..."</p>
    </div>
    <div class="visual muted">
      <div class="skill-bar empty"></div>
      <div class="skill-bar empty"></div>
      <div class="skill-bar empty"></div>
    </div>
  </div>

  <div class="arrow-container">
    <span class="arrow">→</span>
    <span class="duration">5分で</span>
  </div>

  <div class="after-card highlight">
    <span class="label">After</span>
    <div class="content">
      <span class="emoji">😊</span>
      <p>"3つの強みを言語化できた！"</p>
    </div>
    <div class="visual">
      <div class="skill-bar filled">プロジェクト管理</div>
      <div class="skill-bar filled">データ分析</div>
      <div class="skill-bar filled">チーム育成</div>
    </div>
  </div>
</div>
```

```css
.before-card {
  background: var(--bg-muted);
  border: 1px dashed var(--border-light);
  filter: grayscale(0.5);
}

.after-card {
  background: linear-gradient(135deg, var(--accent-light) 0%, #FFF 100%);
  border: 2px solid var(--accent);
  box-shadow: 0 8px 24px var(--accent-glow);
}

.arrow-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.arrow {
  font-size: 32px;
  color: var(--accent);
}

.duration {
  font-size: 12px;
  color: var(--text-secondary);
}
```

### パターン2: タイムライン

```html
<div class="timeline">
  <div class="timeline-item past">
    <span class="time">1週間前</span>
    <p>職務経歴書が書けない...</p>
  </div>
  <div class="timeline-item present">
    <span class="time">今日</span>
    <p>Your Compassに情報を入力</p>
  </div>
  <div class="timeline-item future glow">
    <span class="time">5分後</span>
    <p>ポートフォリオサイト完成！</p>
  </div>
</div>
```

### パターン3: スプリット画面

```css
.split-screen {
  display: flex;
}

.before-side {
  flex: 1;
  background: #E5E5E5;
  filter: grayscale(1);
}

.after-side {
  flex: 1;
  background: var(--accent-light);
}

.divider {
  width: 4px;
  background: var(--accent);
}
```

---

## カラー差別化パターン

### 避けるべき「SaaSテンプレ」カラー

```css
/* ❌ これらは「普通」に見える */
--primary: #3B82F6;  /* 青 */
--primary: #6366F1;  /* インディゴ */
--primary: #8B5CF6;  /* バイオレット */
--bg: #F9FAFB;       /* グレー背景 */
```

### 差別化カラーパレット

#### アンバー系（温かみ・信頼）
```css
:root {
  --accent: #F59E0B;
  --accent-light: #FEF3C7;
  --accent-dark: #92400E;
  --accent-glow: rgba(245, 158, 11, 0.25);
  --bg-primary: #FFFBF5;
}
```
適したサービス: キャリア支援、コーチング、教育

#### コーラル系（親しみ・活力）
```css
:root {
  --accent: #F97316;
  --accent-light: #FFF7ED;
  --accent-dark: #C2410C;
  --accent-glow: rgba(249, 115, 22, 0.25);
  --bg-primary: #FFFAF5;
}
```
適したサービス: クリエイター向け、SNS系、コミュニティ

#### ティール系（成長・バランス）
```css
:root {
  --accent: #14B8A6;
  --accent-light: #CCFBF1;
  --accent-dark: #0F766E;
  --accent-glow: rgba(20, 184, 166, 0.25);
  --bg-primary: #F7FFFE;
}
```
適したサービス: ウェルネス、自己成長、ライフハック

#### ローズ系（やさしさ・ケア）
```css
:root {
  --accent: #F472B6;
  --accent-light: #FCE7F3;
  --accent-dark: #BE185D;
  --accent-glow: rgba(244, 114, 182, 0.25);
  --bg-primary: #FFFBFC;
}
```
適したサービス: 女性向け、育児・家族、ケア系

#### スレート系（プロ・信頼性）
```css
:root {
  --accent: #475569;
  --accent-light: #F1F5F9;
  --accent-dark: #1E293B;
  --accent-glow: rgba(71, 85, 105, 0.15);
  --bg-primary: #FAFBFC;
  --highlight: #F59E0B;  /* アクセントとして暖色を追加 */
}
```
適したサービス: B2B、コンサル、金融

---

## 具体的約束パターン

### 原則
- 抽象的な価値より具体的な数字
- 達成可能な小さな約束
- ユーザーが想像しやすい単位

### パターン1: 時間の約束

```html
<div class="promise-badge">
  <span class="number">5</span>
  <span class="unit">分</span>
  <span class="action">で始める</span>
</div>
```

例:
- 「5分で始める」
- 「15分で完成」
- 「1日5分からOK」

### パターン2: アクション数の約束

```html
<div class="steps-promise">
  <span class="number">3</span>
  <span class="text">つのアクションで</span>
  <span class="result">キャリアが動き出す</span>
</div>
```

例:
- 「3つのステップで完了」
- 「質問は5つだけ」
- 「たった2クリックで」

### パターン3: 実績・信頼の約束

```html
<div class="social-proof">
  <span class="number">1,000</span>
  <span class="unit">人以上</span>
  <span class="action">が利用中</span>
</div>
```

例:
- 「1,000人以上が利用」
- 「満足度98%」
- 「平均評価4.8」

### パターン4: 成果の約束

```html
<div class="outcome-promise">
  <span class="intro">あなたの</span>
  <span class="what">強み</span>
  <span class="verb">が見つかる</span>
</div>
```

例:
- 「3つの強みが見つかる」
- 「次のアクションが明確になる」
- 「迷いがなくなる」

---

## アンチパターン集

### ❌ 避けるべきパターン

#### 1. 機能列挙ファースト
```html
<!-- ❌ これは普通 -->
<h1>キャリア分析ツール</h1>
<ul>
  <li>スキル可視化</li>
  <li>ポートフォリオ生成</li>
  <li>AIアドバイス</li>
</ul>
```

#### 2. 無個性なカード配置
```html
<!-- ❌ これは普通 -->
<div class="features">
  <div class="card">
    <div class="icon">📊</div>
    <h3>分析機能</h3>
    <p>AIがあなたを分析します</p>
  </div>
  <div class="card">...</div>
  <div class="card">...</div>
</div>
```

#### 3. 意味のないグラデーション
```css
/* ❌ グラデーションのためのグラデーション */
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

#### 4. 抽象的なキャッチコピー
```html
<!-- ❌ 何も伝わらない -->
<h1>あなたの可能性を最大化</h1>
<h1>新しいキャリアの形</h1>
<h1>未来を切り開く</h1>
```

### ✅ 改善例

```html
<!-- ✅ 共感から始める -->
<div class="empathy-hero">
  <p>"このままでいいのかな..."</p>
  <p>"強みがわからない..."</p>
  <h1>5分で、あなたの強みが見つかる</h1>
</div>
```

---

## チェックリスト

実装前に確認:

- [ ] ファーストビューで機能説明をしていないか
- [ ] ユーザーの悩みに共感しているか
- [ ] サービス名/コンセプトがデザインに活きているか
- [ ] Before/Afterが視覚化されているか
- [ ] 「青+カード+アイコン」パターンを避けているか
- [ ] 具体的な数字（時間、ステップ数）があるか
- [ ] 意味のあるアニメーションがあるか
