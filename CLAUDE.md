# CLAUDE.md

このファイルは、このリポジトリで作業するClaude Code (claude.ai/code) に向けたガイダンスです。

## プロジェクト概要

カジログ (kajilog) — NFCタップ1つで家事実績を記録する、夫婦・同棲カップル向けの家事みえる化アプリ。背景・課題・ユーザーストーリーは `docs/PRD_家事みえる化アプリ.md` を参照。

## 現状

- `frontend/`: Vite + React (PWA、`vite-plugin-pwa`使用)。スキャフォールディング済みだが、Viteテンプレート以上のアプリロジックはまだ無い。
- `backend/`: FastAPI。データモデル（`models.py`、SQLAlchemy）とローカルSQLite接続（`database.py`）は実装済み。`/api/health`と`/api/chores`のみで、NFCタグ経由の記録エンドポイント（`/t/{tagId}`）はまだ無い。
- `prototype/index.html` は初期の設計レビュー用に作った、ビルド不要の静的HTML/CSS/JSモックアップ。本番のフロントエンドではないため、これを拡張する形で開発を進めないこと。

## コマンド

フロントエンド（`frontend/`で実行）:
- `npm install` — 依存関係のインストール
- `npm run dev` — 開発サーバー（デフォルトポート5173）
- `npm run build` — 本番ビルド（`frontend/dist`に出力）
- `npm run lint` — oxlint

バックエンド（`backend/`で実行。素のvenv/pipではなく[uv](https://docs.astral.sh/uv/)で管理）:
- `uv sync` — 初回セットアップ／依存関係インストール（`.venv`を作成し`uv.lock`を読む）
- `uv add <package>` — 依存関係の追加（`pyproject.toml`と`uv.lock`を更新）
- `uv run uvicorn main:app --port 8000 --reload` — 開発サーバー
- `uv run python seed.py` — テーブル作成＋サンプルデータ投入（ローカルSQLite `backend/kajilog.db`。git管理外）
- テストスイートはまだ無い。

## アーキテクチャ決定

詳細と理由は `docs/DesignDoc_家事みえる化アプリ.md` を参照。要約:

- **フロントエンド**: Vite + React、PWAとしてビルド（`vite-plugin-pwa`）
- **バックエンド**: Python(FastAPI)。Vercelの単一Pythonサーバーレス関数としてデプロイ
- **ホスティング**: Vercelに統一（フロント・バックエンドとも同一プロジェクト）
- **DB**: Supabase(Postgres)
- **家事記録方式（方法B）**: 各NFCタグに固定URL(`https://{domain}/t/{tagId}`)をNDEF URIレコードとして直接書き込む（NFC Tools等のアプリで実施）。iOSショートカットの自動化もネイティブアプリも不要で、タグにタッチするとSafariでそのURLが開くだけ。`tagId`は家事名そのものではなく間接参照で、サーバー側で解決するため、家事名や重みを変えても物理タグの書き直しは不要。「どの家事か」はタグに、「誰がタップしたか」は端末側（初回選択後にクライアント側で記憶）にそれぞれ持たせる。

## ドキュメントの運用

`docs/DesignDoc_家事みえる化アプリ.md` は決定ログ（決定ログ表）とオープンクエスチョン（未決事項）を持つ生きたドキュメント。新しいアーキテクチャ・ツール選定の決定をしたら、決定ログに一言添えて追記し、オープンクエスチョンも更新すること。決定事項を会話履歴だけに残さないこと。

## リポジトリ固有の注意点

- `docs/動画/` は参考資料のみ（競合アプリCAJICOのスクリーンショットと操作録画）で、`.gitignore`で意図的にgit管理から除外している。スクリーンショットには実際の家庭の家事記録データが写っており、録画ファイルも約100MB(GitHubの単一ファイル上限に近い)のため。`git add -f`で戻さないこと。
- GitHubリポジトリ(`froggyy351/kajilog`)は**Public**。PRDに既に含まれる内容以外の、実際の個人・家庭のデータをコミットしないよう注意すること。

## ドキュメント言語

このリポジトリのドキュメント（`*.md`）は日本語で統一する。コード中のコメント・識別子は通常の英語命名で問題ない。
