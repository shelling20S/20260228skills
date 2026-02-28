# うまくいかなかったコードサンプル

避けるべきパターンと、なぜうまくいかないか。

---

## 1. white-space: pre-line でボタンテキストが改行される

**問題のコード:**
```css
.button {
  white-space: pre-line; /* 改行を維持しようとした */
}
```

**症状:**
ボタンテキストが1文字ずつ改行されてしまう。

**原因:**
`pre-line` は改行を維持しつつ折り返すため、flexboxと組み合わせると意図しない改行が発生。

**解決策:**
```css
.button {
  white-space: nowrap; /* または pre */
  flex-shrink: 0;
}
```

---

## 2. position: fixed が phone-frame 内で効かない

**問題のコード:**
```css
.phone-frame {
  position: relative;
  overflow: hidden;
}

.toast {
  position: fixed;
  bottom: 20px;
}
```

**症状:**
トーストが画面全体の下部に表示される。

**原因:**
`position: fixed` は viewport 基準のため、phone-frame を無視する。

**解決策:**
```css
.phone-frame {
  position: relative;
}

.toast {
  position: absolute; /* fixed ではなく absolute */
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
}
```

---

## 3. touchstart/touchend の passive 未指定でスクロールがカクつく

**問題のコード:**
```javascript
el.addEventListener('touchstart', handler);
el.addEventListener('touchend', handler);
```

**症状:**
スクロール時にカクつき、警告が出る。

**原因:**
Chrome はタッチイベントをデフォルトでブロッキングとして扱う。

**解決策:**
```javascript
el.addEventListener('touchstart', handler, { passive: true });
el.addEventListener('touchend', handler, { passive: true });
```

---

## 4. innerHTML で XSS 脆弱性

**問題のコード:**
```javascript
container.innerHTML = `<div>${item.title}</div>`;
```

**症状:**
ユーザー入力に `<script>` が含まれると実行される。

**解決策:**
```javascript
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

container.innerHTML = `<div>${escapeHtml(item.title)}</div>`;
```

---

## 5. localStorage の JSON.parse でクラッシュ

**問題のコード:**
```javascript
const data = JSON.parse(localStorage.getItem('key'));
```

**症状:**
キーが存在しない場合、`null` を parse しようとしてエラー。

**解決策:**
```javascript
const raw = localStorage.getItem('key');
const data = raw ? JSON.parse(raw) : defaultData;
```

---

## 6. z-index の階層崩壊

**問題のコード:**
```css
.header { z-index: 100; }
.modal { z-index: 50; }
.toast { z-index: 9999; }
```

**症状:**
モーダルがヘッダーの下に隠れる。トーストだけ極端に高い。

**解決策:**
z-index を体系的に管理:
```css
:root {
  --z-header: 100;
  --z-modal-overlay: 200;
  --z-modal: 201;
  --z-toast: 300;
}

.header { z-index: var(--z-header); }
.modal-overlay { z-index: var(--z-modal-overlay); }
.modal { z-index: var(--z-modal); }
.toast { z-index: var(--z-toast); }
```

---

## 7. flex-direction: column で height: 100% が効かない

**問題のコード:**
```css
.container {
  display: flex;
  flex-direction: column;
}

.content {
  height: 100%; /* 効かない */
  overflow-y: auto;
}
```

**症状:**
コンテンツが親の高さを超えてスクロールできない。

**解決策:**
```css
.container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* 明示的に高さを指定 */
}

.content {
  flex: 1;
  overflow-y: auto;
  min-height: 0; /* これが重要 */
}
```

---

## 8. Date の月がずれる

**問題のコード:**
```javascript
const date = new Date();
const month = date.getMonth(); // 1月が 0
```

**症状:**
1月なのに `0` が返る。

**解決策:**
```javascript
const month = date.getMonth() + 1; // 1-12
```

---

## 9. アコーディオンの max-height アニメーションが途切れる

**問題のコード:**
```css
.accordion-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s;
}

.accordion.open .accordion-content {
  max-height: auto; /* auto は transition しない */
}
```

**症状:**
アニメーションなしで即座に開く。

**解決策:**
```css
.accordion.open .accordion-content {
  max-height: 500px; /* 十分大きい固定値 */
}
```

または JavaScript で動的に設定:
```javascript
content.style.maxHeight = content.scrollHeight + 'px';
```
