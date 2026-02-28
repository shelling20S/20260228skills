# アイコンライブラリカタログ

**よく使われる絵文字（Unicode Emoji）は極力使用禁止。** 代わりに以下のアイコンライブラリをCDNで読み込んで使用する。デザインの方向性に合わせて最適なライブラリを1〜2個選定すること。

## A) クラス方式（`<i class="...">` で呼ぶ — Font Awesomeに最も近い）

| ライブラリ | CDN | クラス例 | 選定理由 |
|-----------|-----|---------|---------|
| **Font Awesome 6** | `<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">` | `<i class="fa-solid fa-heart"></i>` | solid/regular/brandsのスタイルが明確。情報量が最も多い |
| **Bootstrap Icons** | `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css">` | `<i class="bi bi-heart-fill"></i>` | 管理画面・業務UIに馴染む。癖が少ない |
| **Remix Icon** | `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/remixicon@4.9.0/fonts/remixicon.css">` | `<i class="ri-heart-fill"></i>` | 数が多く、line/fillのバリエーションが揃う |
| **Material Design Icons** | `<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/MaterialDesign-Webfont/7.4.47/css/materialdesignicons.min.css">` | `<i class="mdi mdi-heart"></i>` | Google系の安心感。7200+アイコン収録 |

## B) SVG方式（UIの品質が上がりやすい）

| ライブラリ | CDN | 使い方 | 選定理由 |
|-----------|-----|--------|---------|
| **Lucide** | `<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>` | `<i data-lucide="heart"></i>` + `lucide.createIcons()` | SVG置換タイプ。見た目が綺麗で軽い |
| **Tabler Icons** | `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">` | `<i class="ti ti-heart"></i>` | 線の統一感が強い。UIが締まる |
| **Phosphor Icons** | `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/regular/style.css">` | `<i class="ph ph-heart"></i>` | 太さ6段階（thin/light/regular/bold/fill/duotone）で"デザインを作れる" |

## C) リガチャ方式（テキストを書いたらアイコンになる）

| ライブラリ | CDN | 使い方 | 選定理由 |
|-----------|-----|--------|---------|
| **Material Symbols** | `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined">` | `<span class="material-symbols-outlined">favorite</span>` | 可変フォント（太さ/塗り/サイズ）調整が強い。Outlined/Rounded/Sharpの3スタイル |

## D) Web Components方式（タグで呼ぶ）

| ライブラリ | CDN | 使い方 | 選定理由 |
|-----------|-----|--------|---------|
| **Ionicons** | `<script type="module" src="https://cdn.jsdelivr.net/npm/ionicons@7.1.0/dist/ionicons/ionicons.esm.js"></script>` | `<ion-icon name="heart"></ion-icon>` | Web Componentとして部品的に扱える。モバイル寄り |

## アイコン選定の指針

- **1ファイルHTMLプロトタイプ** → クラス方式（A）が最も手軽。CDNのlinkタグ1行で済む
- **デザイン品質重視** → SVG方式（B）のLucide or Phosphorが綺麗
- **Google/Material系の世界観** → リガチャ方式（C）のMaterial Symbols
- **各デザイン案で異なるアイコンライブラリを使ってもよい**（差別化に有効）
- **同一案内では1つのライブラリに統一する**（混在はデザインの一貫性を損なう）
