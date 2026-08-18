# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

カジログ (kajilog) — NFCタップ1つで家事実績を記録する、夫婦・同棲カップル向けの家事みえる化アプリ。背景・課題・ユーザーストーリーは `docs/PRD_家事みえる化アプリ.md` を参照。

## Current state

- `frontend/`: Vite + React (PWA via `vite-plugin-pwa`), scaffolded but no app logic yet beyond the Vite template.
- `backend/`: FastAPI, scaffolded with a single `/api/health` endpoint — no real routes/data model yet.
- `prototype/index.html` is a static, no-build HTML/CSS/JS mockup used for early design review only. It is not the production frontend and should not be extended as if it were.

## Commands

Frontend (run from `frontend/`):
- `npm install` — install dependencies
- `npm run dev` — dev server (default port 5173)
- `npm run build` — production build (outputs to `frontend/dist`)
- `npm run lint` — oxlint

Backend (run from `backend/`, managed with [uv](https://docs.astral.sh/uv/), not plain venv/pip):
- `uv sync` — first-time setup / install dependencies (creates `.venv`, reads `uv.lock`)
- `uv add <package>` — add a new dependency (updates `pyproject.toml` and `uv.lock`)
- `uv run uvicorn main:app --port 8000 --reload` — dev server
- No test suite yet.

## Architecture decisions

Full detail and rationale live in `docs/DesignDoc_家事みえる化アプリ.md`. Summary:

- **Frontend**: Vite + React, built as a PWA (`vite-plugin-pwa`).
- **Backend**: Python (FastAPI), deployed as a single Vercel Python serverless function.
- **Hosting**: Vercel for both frontend and backend, in one project.
- **Database**: Supabase (Postgres).
- **Chore recording ("Method B")**: each NFC tag has a static URL (`https://{domain}/t/{tagId}`) written directly onto it as an NDEF URI record (via an app like NFC Tools) — no iOS Shortcuts automation and no native app required. Tapping the tag just opens the URL in Safari. `tagId` is an indirect reference, not the chore name itself, and is resolved server-side, so chore names/weights can change later without rewriting physical tags. "Which chore" is encoded in the tag; "who tapped" is inferred from the device (remembered client-side after the first selection), not from the tag.

## Working with the docs

`docs/DesignDoc_家事みえる化アプリ.md` is a living document with a 決定ログ (decision log) table and an オープンクエスチョン (open questions) section. When a new architecture or tooling decision is made, add it to the decision log with a one-line rationale and update the open questions — don't let decisions live only in chat history.

## Repo-specific gotchas

- `docs/動画/` holds reference material only (screenshots of the competing app CAJICO, plus a screen recording) and is intentionally excluded from git via `.gitignore`: the screenshots capture real household chore-tracking data, and the recording is ~100MB (near GitHub's per-file limit). Don't `git add -f` these back in.
- The GitHub repo (`froggyy351/kajilog`) is **public**. Be careful before committing anything that contains real personal/family data beyond what's already in the PRD.
