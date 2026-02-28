# うまくいったコードサンプル

実際のプロトタイプ開発でうまくいったパターン集。

---

## 1. 集中モードのレイアウト（MITSUDAKE）

タスクの「次の一手」を大きく表示し、詳細はアコーディオンで隠す。

```html
<div class="focus-mode">
  <div class="focus-content">
    <div class="focus-koredake">これだけやれ</div>
    <div class="focus-next-step" id="focus-next-step">
      企画書の構成を考える
    </div>
    <div class="focus-info-list">
      <div class="focus-info-row">予想時間: <span>30分</span></div>
      <div class="focus-info-row">〆切: <span>今日</span></div>
      <div class="focus-info-row">完了条件: <span>構成案を3つ出す</span></div>
    </div>
    <div class="focus-task-accordion" onclick="toggleFocusDetail()">
      <span class="focus-task-title">企画書を作成する</span>
      <span class="focus-accordion-arrow">▼</span>
    </div>
    <div class="focus-accordion" id="focus-accordion">
      <div class="focus-subtasks">
        <div class="subtask">□ 構成を考える</div>
        <div class="subtask">□ 資料を集める</div>
      </div>
    </div>
  </div>
</div>
```

```css
.focus-koredake {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.focus-next-step {
  font-size: 24px;
  font-weight: 600;
  line-height: 1.4;
  margin-bottom: 24px;
}

.focus-info-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 24px;
  font-size: 14px;
}

.focus-task-accordion {
  display: flex;
  justify-content: space-between;
  padding: 12px;
  background: var(--surface);
  border-radius: 8px;
  cursor: pointer;
}
```

**ポイント:**
- 「次の一手」を24pxで最も目立たせる
- メタ情報（時間、〆切、条件）はコンパクトに
- タスク詳細はアコーディオンで必要時のみ表示

---

## 2. スワイプ可能なタブ切り替え

タブクリックとスワイプの両方に対応。

```javascript
// タブとコンテンツの状態管理
let currentTab = 0;
const tabCount = 3;

function switchTab(newIndex) {
  if (newIndex < 0 || newIndex >= tabCount) return;

  // タブのスタイル更新
  document.querySelectorAll('.tab-item').forEach((tab, i) => {
    tab.classList.toggle('active', i === newIndex);
  });

  // コンテンツの表示切り替え
  document.querySelectorAll('.tab-content').forEach((content, i) => {
    content.classList.toggle('active', i === newIndex);
  });

  currentTab = newIndex;
}

// スワイプ対応
let touchStartX = 0;
document.addEventListener('touchstart', e => {
  touchStartX = e.touches[0].clientX;
}, { passive: true });

document.addEventListener('touchend', e => {
  const diff = e.changedTouches[0].clientX - touchStartX;
  if (Math.abs(diff) > 80) {
    switchTab(currentTab + (diff > 0 ? -1 : 1));
  }
}, { passive: true });
```

**ポイント:**
- `passive: true` でスクロールパフォーマンス維持
- 閾値を80pxに設定し、誤操作を防止
- 範囲外のタブへの移動を防止

---

## 3. フィルタチップの排他制御

「すべて」選択時に他のフィルタを解除。

```javascript
function toggleFilter(filterEl) {
  const filterValue = filterEl.dataset.filter;

  if (filterValue === 'all') {
    // 「すべて」を選択したら他を解除
    document.querySelectorAll('.filter-chip').forEach(chip => {
      chip.classList.remove('selected');
    });
    filterEl.classList.add('selected');
  } else {
    // 「すべて」を解除
    document.querySelector('[data-filter="all"]').classList.remove('selected');
    filterEl.classList.toggle('selected');

    // 何も選択されていなければ「すべて」を選択
    const selectedCount = document.querySelectorAll('.filter-chip.selected').length;
    if (selectedCount === 0) {
      document.querySelector('[data-filter="all"]').classList.add('selected');
    }
  }

  applyFilters();
}
```

**ポイント:**
- 「すべて」と個別フィルタを排他制御
- フィルタが0個になったら「すべて」に戻す
- 直感的なUXを維持

---

## 4. ボトムシートのオーバーレイ制御

```javascript
function openBottomSheet(id) {
  const overlay = document.getElementById(id + '-overlay');
  const sheet = document.getElementById(id);

  overlay.classList.add('open');
  sheet.classList.add('open');

  // スクロール無効化
  document.body.style.overflow = 'hidden';
}

function closeBottomSheet(id) {
  const overlay = document.getElementById(id + '-overlay');
  const sheet = document.getElementById(id);

  overlay.classList.remove('open');
  sheet.classList.remove('open');

  // スクロール復活
  document.body.style.overflow = '';
}

// オーバーレイクリックで閉じる
document.querySelectorAll('.bottom-sheet-overlay').forEach(overlay => {
  overlay.addEventListener('click', e => {
    if (e.target === overlay) {
      const id = overlay.id.replace('-overlay', '');
      closeBottomSheet(id);
    }
  });
});
```

**ポイント:**
- オーバーレイとシートを別要素で管理
- `e.target === overlay` でシート内クリックを除外
- `body.overflow` で背景スクロールを制御
