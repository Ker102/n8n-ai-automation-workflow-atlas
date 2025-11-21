import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

/**
 * Use VITE_BASE_PATH env so the same build can run locally (/) and on GitHub Pages (/repo-name/).
 * Example: VITE_BASE_PATH=/n8n-automation-atlas/ npm run build
 */
export default defineConfig({
  plugins: [vue()],
  base: process.env.VITE_BASE_PATH || '/',
});
