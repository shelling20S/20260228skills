# バグ防止実装ルール

**プロトタイプはスピードが命。デバッグに時間をかけないためのルール。**

## 過去のバグ事例サマリ

| バグ | 原因 | 教訓 |
|------|------|------|
| 見えないボタンがキーボードで押せてクラッシュ | `opacity:0`+`pointer-events:none`で非表示にしていた | `display:none`を使う |
| `state.currentScenario`がnullでクラッシュ | 状態リセット後もUIは前の画面のまま | 各関数冒頭でnullガード |
| スキップ後に次のフェーズに遷移しない | スキップ処理が「表示を終える」だけで「進む」処理がなかった | スキップ=次へ進むを実装 |
| タイマー発火後にスキップされ重複表示 | タイマーコールバックにガードなし | コールバック冒頭でフェーズ・フラグチェック |
| ボタンのtype未指定でページリロード | `<button>`のデフォルトはtype="submit" | 全buttonにtype="button" |
| className上書きでクラスが消える | `el.className = 'btn'`で他のクラスが消える | classListで操作する |

---

## HTML実装ルール

| ルール | 詳細 |
|--------|------|
| **全`<button>`に`type="button"`** | ページリロード防止 |
| **画面切り替えは`display:none`/`display:block`** | `opacity`+`pointer-events`は使わない。隠れたボタン問題を根本防止 |
| **段階表示ボタンも`display:none`→`display:block`** | 「結論を見る」等のボタンは表示タイミングまで`display:none` |

---

## JS実装ルール

| ルール | 詳細 |
|--------|------|
| **各遷移関数の冒頭にガード節** | `if (!state.currentXxx) { switchPhase('top'); return; }` |
| **タイマーコールバックにフェーズガード** | `if (state.currentPhase !== '期待フェーズ') return;` |
| **タイマーコールバックにフラグガード** | `if (state.isSkipped) return;` |
| **スキップ=次フェーズへ自動遷移** | スキップ後にユーザーが操作不能にならないこと |
| **データ参照前にnullチェック** | `CHARACTERS[id]`、`SCENARIOS.find()`等の戻り値をチェック |
| **classNameは使わない。classListを使う** | `el.classList.add('visible')` / `el.classList.remove('visible')` |

---

## CSS実装ルール

| ルール | 詳細 |
|--------|------|
| **非アクティブ画面は`display:none`** | `.phase { display:none } .phase.active { display:block }` |
| **フェーズ固有のdisplayは`.active`に付ける** | `#phase-chat { display:flex }` のようにIDに直接displayを書くと、`.phase`の`display:none`がIDの詳細度に負けて常に表示される。`#phase-chat.active { display:flex }` とすること |
| **`inert`属性は不要** | `display:none`で十分。余計な複雑性を入れない |
| **`opacity`で表示制御しない** | ボタン・画面の表示/非表示には`display`プロパティを使う |
