# Contributing Guide

Thanks for helping expand the n8n Automation Atlas! This document explains how to submit workflows, report bugs, and ship UI improvements responsibly.

## 🧭 Ground Rules
- Be kind and assume positive intent; our Discussions board is the preferred place for brainstorming.
- Respect upstream licenses. If you import workflows from another repo, include their license text under `licenses/`.
- Keep file names ASCII and descriptive (e.g., `ai-agents/001_newsletter_coordinator.json`).

## 📁 Workflow Contributions
1. Fork the repo and create a feature branch.
2. Drop your `.json` exports inside the most appropriate folder in `workflows/`. Create a new folder if needed.
3. Update or add the upstream license file inside `licenses/`.
4. Run `node scripts/generate-manifest.mjs` (or `cd web && npm run build`) so the explorer sees your workflows.
5. Update `README.md` if you added a new collection category.
6. Open a pull request using the template so reviewers understand provenance, credentials, and testing.

## 💻 Explorer (Vue) Contributions
- Stack: Vue 3 + Vite + vanilla CSS (utility libraries like PrimeVue are welcome).
- Install deps: `cd web && npm install`.
- Start dev server: `npm run dev`.
- Please run `npm run build` before opening a PR to ensure the static assets compile.

## 🐛 Issues & Discussions
- **Questions / showcases / ideas** → use the Discussions templates.
- **Bug reports** → `New Issue > Bug report` template with reproduction steps.
- **Feature requests** → `New Issue > Feature request` template outlining value + scope.

## 🔁 Pull Requests
- Use the provided PR template.
- Keep PRs focused; large multi-topic changes are difficult to review.
- Mention any related issue or discussion.

## 🔐 Security
Found a security/privacy issue? Please open a private discussion or email the maintainer instead of filing a public issue.

Thanks for helping keep the atlas evergreen! ⚡
