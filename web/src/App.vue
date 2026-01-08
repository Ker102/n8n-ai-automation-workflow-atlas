<script setup>
import { ref, computed, onMounted } from 'vue';
import { uiConfig, repoConfig } from './config';
import { getRawDownloadUrl, getGitHubBlobUrl } from './utils/links';

const loading = ref(true);
const errorMessage = ref('');
const manifest = ref(null);
const searchTerm = ref('');
const selectedCategory = ref('all');
const selectedComplexity = ref('all');
const selectedIntegration = ref('all');
const selectedCredential = ref('all');

const manifestUrl = `${import.meta.env.BASE_URL}workflows.json`;

const numberFormatter = new Intl.NumberFormat('en-US');

const formatNumber = (value) => numberFormatter.format(value ?? 0);

const formatBytes = (bytes) => {
  if (!bytes && bytes !== 0) return '—';
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

const normalizedSearch = computed(() => searchTerm.value.trim().toLowerCase());

const categories = computed(() => manifest.value?.categories ?? []);

const categoryFilters = computed(() => {
  const list = categories.value.map((category) => ({
    id: category.id,
    label: `${category.label} (${formatNumber(category.count)})`,
  }));
  return [{ id: 'all', label: `All (${formatNumber(manifest.value?.totalWorkflows)})` }, ...list];
});

const uniqueComplexities = computed(() => {
  const set = new Set();
  categories.value.forEach((c) => c.workflows.forEach((w) => {
    if (w.complexity) set.add(w.complexity);
  }));
  return Array.from(set).sort();
});

const uniqueIntegrations = computed(() => {
  const set = new Set();
  categories.value.forEach((c) => c.workflows.forEach((w) => {
    w.integrations?.forEach((i) => set.add(i));
  }));
  return Array.from(set).sort();
});

const uniqueCredentials = computed(() => {
  const set = new Set();
  categories.value.forEach((c) => c.workflows.forEach((w) => {
    w.credentials?.forEach((c) => set.add(c));
  }));
  return Array.from(set).sort();
});

const filteredCategories = computed(() => {
  const query = normalizedSearch.value;
  return categories.value
    .filter((category) => selectedCategory.value === 'all' || category.id === selectedCategory.value)
    .map((category) => {
      const workflows = !query && selectedComplexity.value === 'all' && selectedIntegration.value === 'all' && selectedCredential.value === 'all'
        ? category.workflows
        : category.workflows.filter((workflow) => {
            // Search Term
            const nameMatch = workflow.name.toLowerCase().includes(query);
            const fileMatch = workflow.fileName.toLowerCase().includes(query);
            if (query && !nameMatch && !fileMatch) return false;

            // Complexity
            if (selectedComplexity.value !== 'all' && workflow.complexity !== selectedComplexity.value) return false;

            // Integration
            if (selectedIntegration.value !== 'all' && !workflow.integrations?.includes(selectedIntegration.value)) return false;

            // Credential
            if (selectedCredential.value !== 'all' && !workflow.credentials?.includes(selectedCredential.value)) return false;

            return true;
          });
      return { ...category, workflows };
    })
    .filter((category) => category.workflows.length > 0)
    .sort((a, b) => a.label.localeCompare(b.label));
});

const totalVisibleWorkflows = computed(() =>
  filteredCategories.value.reduce((sum, category) => sum + category.workflows.length, 0)
);

const generatedAt = computed(() => {
  if (!manifest.value?.generatedAt) return null;
  const date = new Date(manifest.value.generatedAt);
  return Number.isNaN(date.getTime()) ? null : date.toLocaleString();
});

const configWarning = computed(
  () => repoConfig.owner.includes('YOUR_') || repoConfig.repo.includes('YOUR_')
);

async function fetchManifest() {
  loading.value = true;
  errorMessage.value = '';
  try {
    const response = await fetch(manifestUrl);
    if (!response.ok) throw new Error(`HTTP ${response.status}: Unable to load workflows manifest.`);
    const text = await response.text();
    try {
      manifest.value = JSON.parse(text);
    } catch (parseError) {
      throw new Error(`Decoding failed: ${parseError.message}. Response size: ${text.length} bytes`);
    }
  } catch (error) {
    errorMessage.value = error.message ?? 'Unknown error while loading manifest.';
    console.error('Manifest load error:', error);
  } finally {
    loading.value = false;
  }
}

onMounted(fetchManifest);
</script>

<template>
  <main class="app-shell">
    <header class="hero">
      <p class="eyebrow">n8n Workflow Explorer</p>
      <h1>{{ uiConfig.pageTitle }}</h1>
      <p class="tagline">{{ uiConfig.heroTagline }}</p>

      <div class="repo-actions">
        <a href="https://github.com/Ker102/n8n-workflows-36k" target="_blank" rel="noopener" class="repo-btn">
          <svg height="16" viewBox="0 0 16 16" version="1.1" width="16" aria-hidden="true"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
          Repo
        </a>
        <a href="https://github.com/Ker102/n8n-workflows-36k" target="_blank" rel="noopener" class="repo-btn star-btn">
          <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-star"><path fill="currentColor" d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.75.75 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z"></path></svg>
          Star
        </a>
      </div>

      <section class="stats-grid" v-if="manifest">
        <div class="stat-card">
          <span>Total Workflows</span>
          <strong>{{ formatNumber(manifest.totalWorkflows) }}</strong>
        </div>
        <div class="stat-card">
          <span>Collections</span>
          <strong>{{ formatNumber(manifest.categoryCount) }}</strong>
        </div>
        <div class="stat-card">
          <span>Last Indexed</span>
          <strong>{{ generatedAt || 'Pending' }}</strong>
        </div>
      </section>
    </header>

    <section class="companion-card">
      <div>
        <p class="companion-kicker">Need an AI co-pilot?</p>
        <h2>Kaelux Automate</h2>
        <p>
          A custom n8n build with an integrated LLM that writes workflows from prompts.
          Use it alongside this atlas to brainstorm, scaffold, and refine automations faster.
        </p>
      </div>
      <a
        class="companion-link"
        href="https://github.com/Ker102/Kaelux-Automate"
        target="_blank"
        rel="noopener"
      >
        Explore Kaelux Automate →
      </a>
    </section>

    <section class="github-promo">
      <div class="promo-content">
        <svg height="32" viewBox="0 0 16 16" width="32" aria-hidden="true" class="github-icon">
          <path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
        </svg>
        <div>
          <h3>More from Ker102</h3>
          <p>
            Enjoying this collection? Check out my other automation tools and projects.
            If you find them useful, a ⭐ on GitHub goes a long way!
          </p>
        </div>
      </div>
      <a
        class="promo-link"
        href="https://github.com/Ker102?tab=repositories"
        target="_blank"
        rel="noopener"
      >
        View All Repositories →
      </a>
    </section>

    <section v-if="configWarning" class="config-alert">
      <p>
        Configure your GitHub owner/repo inside <code>web/src/config.js</code> so download links
        can point to the correct raw files.
      </p>
    </section>

    <section class="filters" v-if="manifest">
      <label class="search-field">
        <span>Search the library</span>
        <input
          type="search"
          v-model="searchTerm"
          :placeholder="`Search ${formatNumber(manifest.totalWorkflows)} workflows…`"
        />
      </label>

      <div class="filter-row">
        <select v-model="selectedComplexity" class="filter-select">
          <option value="all">Any Complexity</option>
          <option v-for="c in uniqueComplexities" :key="c" :value="c">{{ c }}</option>
        </select>

        <select v-model="selectedIntegration" class="filter-select">
          <option value="all">Any Integration</option>
          <option v-for="i in uniqueIntegrations" :key="i" :value="i">{{ i }}</option>
        </select>

        <select v-model="selectedCredential" class="filter-select">
          <option value="all">Any Credential</option>
          <option v-for="c in uniqueCredentials" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>

      <div class="chip-row">
        <button
          v-for="chip in categoryFilters"
          :key="chip.id"
          type="button"
          :class="['chip', { active: selectedCategory === chip.id }]"
          @click="selectedCategory = chip.id"
        >
          {{ chip.label }}
        </button>
      </div>
    </section>

    <section class="results">
      <p v-if="loading" class="muted">Loading manifest…</p>
      <p v-else-if="errorMessage" class="error">{{ errorMessage }}</p>

      <template v-else>
        <p class="result-meta">
          Showing <strong>{{ formatNumber(totalVisibleWorkflows) }}</strong>
          {{ totalVisibleWorkflows === 1 ? 'workflow' : 'workflows' }}
        </p>

        <p v-if="!filteredCategories.length" class="muted">
          No workflows match your search. Try another keyword or category.
        </p>

        <div class="category-list">
          <details
            v-for="(category, index) in filteredCategories"
            :key="category.id"
            :open="selectedCategory === 'all' ? index === 0 : selectedCategory === category.id"
          >
            <summary>
              <span>
                {{ category.label }}
                <small>{{ category.description }}</small>
              </span>
              <span class="count-pill">{{ formatNumber(category.workflows.length) }}</span>
            </summary>

            <ul class="workflow-list">
              <li v-for="workflow in category.workflows" :key="workflow.relativePath">
                <div class="workflow-meta">
                  <strong>{{ workflow.name }}</strong>
                  <span class="path">{{ workflow.relativePath }}</span>
                  <div class="tags">
                    <span v-if="workflow.complexity" :class="['badge', workflow.complexity]">{{ workflow.complexity }}</span>
                    <span v-for="int in workflow.integrations?.slice(0, 3)" :key="int" class="badge integration">{{ int }}</span>
                    <span v-if="workflow.integrations?.length > 3" class="badge more">+{{ workflow.integrations.length - 3 }}</span>
                  </div>
                </div>
                <div class="workflow-actions">
                  <span class="size">{{ formatBytes(workflow.sizeBytes) }}</span>
                  <a
                    :href="getGitHubBlobUrl(workflow.relativePath)"
                    target="_blank"
                    rel="noopener"
                    class="ghost"
                  >
                    View on GitHub
                  </a>
                  <a
                    :href="getRawDownloadUrl(workflow.relativePath)"
                    target="_blank"
                    rel="noopener"
                    download
                    class="primary"
                  >
                    Download JSON
                  </a>
                </div>
              </li>
            </ul>
          </details>
        </div>
      </template>
    </section>
  </main>
</template>
