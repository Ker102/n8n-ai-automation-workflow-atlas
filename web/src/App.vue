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
    if (!response.ok) throw new Error('Unable to load workflows manifest.');
    manifest.value = await response.json();
  } catch (error) {
    errorMessage.value = error.message ?? 'Unknown error while loading manifest.';
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
