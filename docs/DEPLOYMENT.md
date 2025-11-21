# Workflow Explorer Deployment Guide

This guide covers everything maintainers need to run, configure, and ship the `web/` Vue + Vite app (the n8n Workflow Explorer) to GitHub Pages.

## 1. Prerequisites
- Node.js 18+ (recommended v20)
- npm 9+
- Access to this repository with permission to push branches/Pages

## 2. Install & Develop Locally
```bash
cd web
npm install
npm run dev
```
- `npm run dev` auto-generates the `workflows.json` manifest, starts Vite, and hot-reloads changes.
- The app consumes `web/public/workflows.json`, so ensure your `workflows/` directory exists before running dev/build commands.

## 3. Configure Download Links
Edit `web/src/config.js`:
```js
export const repoConfig = {
  owner: 'YOUR_GITHUB_USERNAME',
  repo: 'YOUR_REPOSITORY_NAME',
  branch: 'main', // or gh-pages, etc.
};
```
- These values populate the GitHub and raw download links, so keep them in sync with the repo that hosts the workflow JSON files.
- Update `uiConfig` if you want to customize the hero title/tagline.

## 4. Build for Production
```bash
cd web
npm run build
```
- `npm run build` runs `npm run generate:manifest` first, ensuring the manifest is always fresh.
- Static files land in `web/dist/`.
- To serve the app from a sub-path (e.g., `https://<user>.github.io/<repo>/`), pass `VITE_BASE_PATH`:
  ```bash
  VITE_BASE_PATH=/your-repo-name/ npm run build
  ```

## 5. Deploy to GitHub Pages
### Option A: Manual Push
1. Build the site.
2. Create (or switch to) a `gh-pages` branch.
3. Copy `web/dist/` contents to the branch root and push.
4. Enable GitHub Pages → Deploy from branch `gh-pages` / root.

### Option B: GitHub Actions (recommended)
```yaml
name: Deploy Pages
on:
  push:
    branches: [main]
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: cd web && npm install
      - run: cd web && npm run build
        env:
          VITE_BASE_PATH: /<your-repo-name>/ # optional sub-path
      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: web/dist
```
- Update `VITE_BASE_PATH` if your Pages site is served under `/repo-name/` (standard for project Pages). Leave unset for user/organization root sites.
- After the first deployment, verify Pages settings point at the `gh-pages` branch.

## 6. Updating the Manifest
Any time new workflows land, rerun `npm run generate:manifest` (or simply `npm run build`) so the manifest reflects the latest files before deploying.

## 7. Troubleshooting
- **Blank download links**: Ensure `repoConfig` is set with real owner/repo values.
- **404s on GitHub Pages**: Double-check `VITE_BASE_PATH` matches the Pages sub-path and that the `base` option in `vite.config.js` uses `process.env.VITE_BASE_PATH`.
- **Manifest missing**: Confirm `workflows/` exists and contains JSON files; re-run the generator.

You're ready to share the explorer! 🎉
