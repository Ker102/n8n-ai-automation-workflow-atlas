# GEMINI.md - Project Context & Instructions

## Project Overview
**Name:** n8n Automation Atlas
**Description:** A curated collection of 3,800+ n8n automation workflows, organized into themed packs. It includes a Vue + Vite web application (`web/`) to browse and explore these workflows.
**Goal:** To provide a centralized, easy-to-navigate repository of n8n workflows for the community.

## Directory Structure
- **`workflows/`**: The core content. Contains subdirectories for each collection (e.g., `ai-automation-lab`, `community-mega-pack`). Each file is a `.json` export of an n8n workflow.
- **`web/`**: A Vue.js + Vite application serving as a "Workflow Explorer" UI.
    - `src/`: Source code for the Vue app.
    - `public/`: Static assets.
    - `package.json`: Dependencies (Vue 3, Vite).
- **`scripts/`**: Utility scripts. Notably `generate-manifest.mjs` which likely indexes the workflows for the web app.
- **`docs/`**: Documentation files.
- **`licenses/`**: License files for the upstream sources of the workflows.

## Tech Stack
- **Workflows:** n8n (JSON exports)
- **Web UI:** Vue.js 3, Vite, JavaScript (ES Modules).

## Key Guidelines for AI Assistants
1.  **Workflow Handling:**
    - Workflows are stored as JSON files.
    - When analyzing workflows, look for the `nodes` and `connections` arrays in the JSON.
    - Do not modify the `workflows/` directory structure unless explicitly asked to reorganize.
2.  **Web UI Development (`web/`):**
    - Use `npm run dev` to start the local development server.
    - The build process (`npm run build`) triggers `generate:manifest` to update the workflow index.
    - Follow Vue.js 3 best practices (Composition API).
3.  **Documentation:**
    - Keep `README.md` and `GEMINI.md` updated if the project structure changes.
    - Respect upstream licenses when adding new workflows.

## Common Tasks
- **Adding a new workflow:** Place the `.json` file in the appropriate subdirectory within `workflows/`.
- **Updating the Web UI:** Modify files in `web/src/` and test with `npm run dev`.
- **Re-indexing Workflows:** Run `npm run generate:manifest` (from the `web/` directory) to update the list of available workflows for the UI.

## Contextual Notes
- This project is a "monorepo" of sorts, combining data (workflows) and a viewer (web app).
- The `workflows` directory is very large; avoid listing all files recursively unless necessary.
