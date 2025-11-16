# Repository Guidelines

## Project Structure & Module Organization
Workflow assets live under `workflows/<collection>/`, grouped by category (AI lab, Pinecone kits, Box demos, etc.). Source licenses mirror each collection inside `licenses/`, and new folders require a matching notice there. The Vue workflow explorer sits in `web/` (`src/` for components, `public/` for the generated manifest) and deploys as a static site. Automation scripts stay in `scripts/`, while longer-form references live in `docs/`.

## Build, Test, and Development Commands
- `node scripts/generate-manifest.mjs` — resyncs `web/public/workflows.json` after workflow edits.
- `cd web && npm install` — install Vue/Vite dependencies before hacking on the explorer.
- `cd web && npm run dev` — Vite dev server with hot reload.
- `cd web && npm run build` — runs the manifest prebuild and emits production assets to `web/dist/`; treat this as CI.
- `cd web && npm run preview` — serve the built dist folder locally for the final smoke test.

## Coding Style & Naming Conventions
Keep workflow filenames ASCII, descriptive, and zero-padded where helpful (e.g., `ai-automation-lab/003_sales_assistant.json`). Vue single-file components use `<script setup>`, camelCase composables, kebab-case component names, and 2-space indentation like `src/App.vue`. Keep CSS in `web/src/style.css` scoped via utility classes; avoid inline styles. There is no repo-wide linter, so stick with Prettier-style formatting and stay consistent.

## Testing Guidelines
There is no standalone test runner. Treat `npm run build` as the acceptance gate: it regenerates the manifest in `public/` and ensures Vite compiles. After the build, review the explorer with `npm run preview` and import at least one touched workflow into n8n to confirm credential placeholders and metadata survive.

## Commit & Pull Request Guidelines
Recent history favors short, imperative commit titles with optional prefixes (`chore: rebuild repository without secrets`, `Create FUNDING.yml`). Keep each commit focused (workflows vs. UI code vs. docs). Pull requests must use `.github/pull_request_template.md`: fill the summary, tick the `npm run build` and manifest boxes, cite related issues/discussions, and call out any updated licenses. Attach screenshots or gifs for UI tweaks.

## Security & Configuration Tips
Do not commit credentials into workflow JSON—leave placeholders and document requirements inside README entries. Update `web/src/config.js` when forking so download links point to your repo, and verify manifest paths before publishing. License mirrors in `licenses/` must stay current to keep redistribution compliant.\n*** End Patch"}assistant to=functions.apply_patch能买吗
