# Repository Guidelines

## Project Structure & Module Organization

This repository teaches agent harness mechanisms through paired Python examples, docs, and a Next.js learning UI.

- `agents/`: Python reference implementations from `s01_agent_loop.py` through `s12_worktree_task_isolation.py`, plus `s_full.py`.
- `docs/{en,zh,ja}/`: session documentation in three languages. Keep session IDs aligned across locales.
- `web/`: interactive learning platform, source viewer, visualizations, and generated content.
- `web/src/data/scenarios/` and `web/src/data/annotations/`: per-session UI data such as `s03.json`.
- `skills/`: teaching examples for the skill-loading session.
- `tests/`: Python smoke and behavior tests.
- `note/`: learner-facing Markdown notes produced after each completed session.

## Build, Test, and Development Commands

Run Python examples from the repository root:

```sh
pip install -r requirements.txt
python agents/s03_todo_write.py
pytest
```

Run the interactive platform from `web/`:

```sh
npm install
npm run dev      # extracts content, then serves http://localhost:3000
npm run build    # extracts content, type-checks/builds Next.js
npx tsc --noEmit # CI type check
```

`npm run extract` regenerates `web/src/data/generated/` from `agents/` and `docs/`.

## Coding Style & Naming Conventions

Use concise, readable Python with 4-space indentation and standard library types where practical. Session files follow `sNN_topic_name.py`; docs and UI data follow matching `sNN-*` or `sNN.json` names.

For the web app, use TypeScript, React components, and existing path conventions under `web/src/components/`, `web/src/app/`, and `web/src/data/`. Keep generated files generated; change their sources instead.

## Testing Guidelines

Python tests use `pytest` and `unittest` patterns. Name files `test_*.py` and keep tests deterministic; avoid real API calls by faking external modules or clients as existing tests do. For web changes, run `npx tsc --noEmit` and `npm run build`.

## Commit & Pull Request Guidelines

Git history was unavailable in this environment due repository ownership protection, so use a simple conventional style: short imperative subject lines such as `Add s03 annotation data` or `Fix source viewer routing`.

Pull requests should include a brief summary, commands run, affected sessions, and screenshots or screen recordings for UI changes. Link related issues when available and call out generated-file updates.

## Security & Configuration Tips

Copy `.env.example` to `.env` for local agent runs and set `ANTHROPIC_API_KEY`. Do not commit secrets, local caches, `node_modules/`, or ad hoc run logs.

## Learning Note Workflow

After each session is studied, create or update a Markdown note under `note/` named `sNN-topic.md`. Capture what the learner understood, mistakes or unclear points, runtime issues encountered, corrected explanations, and follow-up review questions. Keep notes practical and specific to the session rather than duplicating the full course docs.
