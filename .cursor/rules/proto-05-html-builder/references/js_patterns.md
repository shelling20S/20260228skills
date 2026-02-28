# JSパターン集

## localStorage永続化

```javascript
const STORAGE_KEY = '[project]_v[version]';
const load = () => JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
const save = (data) => localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
```

---

## スワイプ検出

```javascript
let startX = 0;
el.addEventListener('touchstart', e => startX = e.touches[0].clientX, { passive: true });
el.addEventListener('touchend', e => {
  const diff = e.changedTouches[0].clientX - startX;
  if (Math.abs(diff) > 50) diff > 0 ? onSwipeRight() : onSwipeLeft();
}, { passive: true });
```

---

## 状態管理の基本パターン

```javascript
const state = {
  currentPhase: 'top',
  currentItem: null,
  isLoading: false,
  isSkipped: false
};

function switchPhase(phaseName) {
  document.querySelectorAll('.phase').forEach(el => {
    el.classList.remove('active');
  });

  const target = document.getElementById(`phase-${phaseName}`);
  if (target) {
    target.classList.add('active');
    state.currentPhase = phaseName;
  }
}
```

---

## ガード節パターン

```javascript
function showItemDetail(id) {
  const item = ITEMS.find(i => i.id === id);
  if (!item) {
    switchPhase('top');
    return;
  }

  state.currentItem = item;
  // ... 表示処理
}
```

---

## タイマーにフェーズガードを入れる

```javascript
function startAutoAdvance() {
  const expectedPhase = state.currentPhase;

  setTimeout(() => {
    if (state.currentPhase !== expectedPhase) return;
    if (state.isSkipped) return;

    advanceToNextPhase();
  }, 3000);
}
```

---

## トースト表示

```javascript
function showToast(message, duration = 2000) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.add('show');

  setTimeout(() => {
    toast.classList.remove('show');
  }, duration);
}
```

---

## モーダル制御

```javascript
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  const overlay = document.getElementById('overlay');

  overlay.style.display = 'block';
  modal.style.display = 'block';

  overlay.onclick = () => closeModal(modalId);
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  const overlay = document.getElementById('overlay');

  modal.style.display = 'none';
  overlay.style.display = 'none';
}
```

---

## データリセット機能

```javascript
const DEFAULT_DATA = {
  items: [
    { id: '1', name: 'サンプル1', description: '説明文です' },
    { id: '2', name: 'サンプル2', description: '長い説明文で\n改行も含みます' },
    { id: '3', name: 'Sample 3', description: 'English and 日本語 mixed' }
  ]
};

function resetToDefault() {
  if (confirm('サンプルデータに戻しますか？')) {
    save(DEFAULT_DATA);
    location.reload();
  }
}
```

---

## ローディング表示（モック用）

```javascript
function simulateApiCall(callback, minDelay = 300, maxDelay = 800) {
  const delay = Math.random() * (maxDelay - minDelay) + minDelay;

  showLoading();

  setTimeout(() => {
    hideLoading();
    callback();
  }, delay);
}

function showLoading() {
  document.getElementById('loading-overlay').style.display = 'flex';
}

function hideLoading() {
  document.getElementById('loading-overlay').style.display = 'none';
}
```
