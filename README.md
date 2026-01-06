[![Star This Repo](https://img.shields.io/badge/⭐%20Star%20this%20repo-222?style=for-the-badge)](https://github.com/Ker102/n8n-ai-automation-workflow-atlas)

# 🌌 n8n Automation Atlas

![Workflows](https://img.shields.io/badge/Workflows-36,405-blueviolet?style=for-the-badge)
![Collections](https://img.shields.io/badge/Collections-6-9cf?style=for-the-badge)
![Synthetic](https://img.shields.io/badge/Synthetic-12,500+-ff6b6b?style=for-the-badge)
![Formats](https://img.shields.io/badge/Format-n8n%20JSON-0b5fff?style=for-the-badge&logo=json&logoColor=white)
![ML Ready](https://img.shields.io/badge/ML%20Ready-Semantic%20Labels-41b883?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-000?style=for-the-badge)

> **36,405 unique n8n workflows** — curated community templates + AI-generated synthetic workflows, all deduplicated and labeled for semantic search and ML training.

---

## 🆕 What's New: Synthetic Dataset Generation

We've scaled this repository from 3,800 to **36,405 unique workflows** using a **Combinatorial Archetype Engine**:

| Source | Count | Description |
|--------|-------|-------------|
| **Repository Curated** | 3,831 | Hand-picked community templates |
| **Synthetic Generated** | 12,500+ | Archetype-based combinatorial expansion |
| **External Community** | 23,900+ | Cleaned HuggingFace dataset |
| **Final (Deduplicated)** | **36,405** | Unique, ML-ready workflows |

### How It Works

Instead of random generation (which produces broken JSON), we use **5 proven archetype blueprints**:

| Archetype | Flow |
|-----------|------|
| **AI Pipeline** | Trigger → AI Analysis → Database → Notification |
| **Cross-PM Sync** | Schedule → Source PM → Destination PM (Jira↔Asana↔Trello) |
| **Redundant Backup** | Trigger → SQL Database → NoSQL Backup |
| **Support Triage** | Form → AI Classification → Ticket → Team Notification |
| **E-commerce** | Order Trigger → CRM Update → Email Receipt |

Each archetype uses **equivalency groups** (Postgres = MySQL = Supabase) and generates every valid combination:

```
27 triggers × 4 AI models × 13 databases × 5 messaging = 7,020 workflows
```

**→ Read full details:** [docs/SYNTHETIC_GENERATION.md](docs/SYNTHETIC_GENERATION.md)

---

## 🤗 Welcome, Operators!

Whether you build full-stack AI agents, automate product ops, or just love tinkering with n8n, this atlas is for you. Clone it, remix it, and share your own packs—we'd love to showcase community-built automations here.

---

## 📦 Dataset Downloads

Large data files are available as **GitHub Release assets**:

| File | Size | Description |
|------|------|-------------|
| `n8n_workflows.jsonl` | ~280MB | Final consolidated dataset (36,405 workflows) |
| `n8n_full.parquet` | ~118MB | Same data in Parquet format |

**[→ Download from Releases](https://github.com/Ker102/n8n-ai-automation-workflow-atlas/releases)**

---

## 💖 Support the Atlas

Keeping a living automation library online (and refreshing all upstream sources) takes time. If these workflows save you cycles, please consider:

- [**Sponsoring on GitHub**](https://github.com/sponsors/Ker102) to fund future packs and hosting.
- [**Starring the repository**](https://github.com/Ker102/n8n-ai-automation-workflow-atlas) so more builders discover it.
- Sharing the repo/link on socials or inside your team's automation channel.

---

## 📚 What's Inside

### Curated Collections (3,831 workflows)

| Collection | Focus | Count | Folder | License |
|------------|-------|-------|--------|---------|
| Community Mega Pack | General-purpose automations | **2057** | `workflows/community-mega-pack/` | MIT |
| AI Automation Lab | AI agents, RAG, chains | **1764** | `workflows/ai-automation-lab/` | MIT |
| Box MCP Demos | Box metadata & DocGen | **5** | `workflows/box-mcp-demos/` | MIT |
| Pinecone RAG Kits | Retrieval-augmented workflows | **3** | `workflows/pinecone-rag-kits/` | MIT |
| Synapse Pro Ops | Production automations | **1** | `workflows/synapse-pro-ops/` | MIT |
| Self-Hosted AI Starter | n8n AI starter kit | **1** | `workflows/self-hosted-ai-starter/` | Apache-2.0 |

### Synthetic + External Dataset (32,500+ workflows)

| Source | Description |
|--------|-------------|
| `workflows/synthetic_generated.jsonl` | 12,500+ archetype-generated workflows |
| External Community | 23,900+ cleaned HuggingFace workflows |

---

## 🧰 Dataset Generation Scripts

Generate your own synthetic workflows or process external datasets:

```bash
# Generate synthetic workflows (12,500+)
node scripts/generate-synthetic-workflows.mjs

# Convert external parquet dataset
node scripts/convert-parquet.js

# Clean and validate external data
node scripts/clean-external-data.mjs

# Consolidate all sources with deduplication
node scripts/prepare-dataset.mjs

# Add semantic labels for ML
node scripts/final-labeling.mjs
```

| Script | Purpose |
|--------|---------|
| `generate-synthetic-workflows.mjs` | Combinatorial archetype engine |
| `convert-parquet.js` | Convert HuggingFace parquet to JSONL |
| `clean-external-data.mjs` | Filter invalid workflows, extract metadata |
| `prepare-dataset.mjs` | Merge sources, deduplicate |
| `final-labeling.mjs` | Add semantic labels for vector search |
| `analyze-node-coverage.mjs` | Audit node type usage |

---

## 🛠️ Import Any Workflow Into n8n

1. **Clone or download** this repo so you have the `workflows/` directory locally.
2. In your n8n instance, click **Import > From File** (or paste JSON on an open canvas).
3. **Select a workflow** from the folder that matches the capability you need.
4. n8n will load the nodes; **review credentials** placeholders (OpenAI, Pinecone, Box, etc.).
5. **Create or link credentials** inside n8n to match the workflow's requirements.
6. Hit **Activate** on the workflow, test with sample data, then customize nodes to fit your stack.

---

## 🧭 How to Navigate

```text
workflows/
├── ai-automation-lab/           # AI-first agents, copilots, enrichment flows
├── box-mcp-demos/               # Box MCP demos for DocGen & metadata
├── community-mega-pack/         # Massive community collection
├── pinecone-rag-kits/           # Pinecone quickstarts
├── self-hosted-ai-starter/      # n8n AI starter kit template
├── synapse-pro-ops/             # ProfSynapse production automations
└── synthetic_generated.jsonl    # 12,500+ synthetic workflows

scripts/
├── generate-synthetic-workflows.mjs  # Archetype engine
├── convert-parquet.js                # Dataset converter
├── clean-external-data.mjs           # Quality filter
├── prepare-dataset.mjs               # Consolidation
├── final-labeling.mjs                # Semantic labeling
└── analyze-node-coverage.mjs         # Coverage audit

docs/
└── SYNTHETIC_GENERATION.md      # Full generation documentation
```

---

## 🔥 Companion Project: Kaelux Automate

Looking for an AI co-pilot that writes n8n workflows from prompts? Check out [**Kaelux Automate**](https://github.com/Ker102/Kaelux-Automate)—a custom n8n build with an LLM tuned specifically for workflow authoring. Pair Kaelux with this atlas to brainstorm flows with AI and then import/extend the generated templates here.

---

## 🚀 Getting Started

### Option A · Quick Download from GitHub
1. Browse [`workflows/`](workflows) and find the collection you need.
2. Click any `.json` file → **Raw** button → **Save As…**
3. In n8n: **Import from File** → choose the saved JSON.

### Option B · Clone the Entire Library
```bash
git clone https://github.com/Ker102/n8n-ai-automation-workflow-atlas.git
```

### Option C · Use the Hosted Explorer
Visit the [GitHub Pages explorer](https://ker102.github.io/n8n-ai-automation-workflow-atlas/) to search, filter, and download workflows.

---

## 🌐 Workflow Explorer UI

The `web/` directory contains a **Vue + Vite** single-page app deployed to GitHub Pages. Features:
- **Search & filter** by integrations, complexity, credentials
- **Download JSON** directly from the browser
- **Preview** workflow structure before importing

---

## 🤝 Contributing

We welcome new workflow packs, better documentation, and UX polish. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

- **Repository:** [MIT](./LICENSE)
- **Upstream sources:** See `licenses/` for each collection's terms.

---

Happy automating! ⚡
