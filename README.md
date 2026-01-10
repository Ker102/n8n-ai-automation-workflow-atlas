[![Star This Repo](https://img.shields.io/badge/⭐%20Star%20this%20repo-222?style=for-the-badge)](https://github.com/Ker102/n8n-workflows-36k)

# 🌌 n8n Automation Atlas

![Total](https://img.shields.io/badge/Total%20Workflows-131,648-blueviolet?style=for-the-badge)
![Importable](https://img.shields.io/badge/Importable-36,985-green?style=for-the-badge)
![ML Training](https://img.shields.io/badge/ML%20Training-97,000-orange?style=for-the-badge)
![Categories](https://img.shields.io/badge/Categories-26-9cf?style=for-the-badge)

### Built With
![n8n](https://img.shields.io/badge/n8n-EA4B71?style=flat-square&logo=n8n&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![ES Modules](https://img.shields.io/badge/ES%20Modules-.mjs-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

### AI & Embeddings
![Together AI](https://img.shields.io/badge/Together%20AI-FF6B6B?style=flat-square)
![M2-BERT-32k](https://img.shields.io/badge/M2--BERT--32k-Embeddings-blue?style=flat-square)
![Gemini Embedding](https://img.shields.io/badge/Gemini-Embedding--001-4285F4?style=flat-square&logo=google&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini%202.0-Flash-4285F4?style=flat-square&logo=google&logoColor=white)

> **131,648 n8n workflows** — the world's largest open-source n8n workflow dataset.  
> **36,985 importable** workflows ready for n8n + **97,000 ML training** variations.

---

## 🚀 Quick Access

### Option 1: Workflow Explorer (Recommended)
Browse, search, filter, and download the **36,985 importable** workflows:

👉 **[Open Workflow Explorer](https://n8n-workflows-36k.vercel.app)**

### Option 2: Training Dataset (HuggingFace)
For AI/ML training with instruction-tuning format (**131,648 examples**):

👉 **[Download from HuggingFace](https://huggingface.co/datasets/Ker102/n8n-mega-workflows)**

### Option 3: Clone Everything
```bash
git clone https://github.com/Ker102/n8n-workflows-36k.git
```

---

## 📂 Importable Workflows (36,985)

Ready to import into your n8n instance:

| Category | Workflows | Path | Description |
|----------|-----------|------|-------------|
| **Community Refined** | 24,696 | `workflows/external/` | Cleaned community dataset |
| **Synthetic v1** | 8,744 | `workflows/synthetic/` | AI-generated variations |
| **Initial Megapack** | 2,057 | `workflows/initial_megapack/` | General-purpose automations |
| **AI Automation Lab** | 1,464 | `workflows/ai-automation-lab/` | AI agents, copilots, RAG |
| **+ 4 more** | 24 | various | Box, Pinecone, Synapse demos |

---

## 🤖 ML Training Workflows (97,000)

Synthetic workflows for training AI models (in `workflows_ml/`):

| Category | Workflows | Description |
|----------|-----------|-------------|
| **Synthetic v2** | 97,000 | Node-swap generated variations from 100 archetypes |

> ⚠️ These are **synthetic node-swapped variations** optimized for ML training, not direct n8n import.

## 📥 How to Import a Workflow

1. **Find a workflow** using the [Explorer](https://n8n-workflows-36k.vercel.app) or [browse on GitHub](https://github.com/Ker102/n8n-workflows-36k/tree/main/workflows)
2. **Download the JSON file** (click "Download JSON" in Explorer, or "Raw" → Save As on GitHub)
3. **Open n8n** and click **Import → From File**
4. **Select the JSON file** and click Import
5. **Configure credentials** for any services (OpenAI, Slack, etc.)
6. **Activate and test** your workflow

---

## 🔍 Workflow Explorer Features

The web-based explorer at [n8n-workflows-36k.vercel.app](https://n8n-workflows-36k.vercel.app) offers:

- **Search** - Find workflows by name or keyword
- **Filter by Category** - Browse specific collections
- **Filter by Integration** - Find workflows using Slack, Google Sheets, OpenAI, etc.
- **Filter by Complexity** - Basic, Intermediate, or Advanced
- **One-click Download** - Download JSON files directly

---

## 📦 Bulk Download

For ML training or bulk import, download the complete dataset:

| File | Size | Format |
|------|------|--------|
| `n8n_workflows.jsonl` | ~280MB | JSONL (one workflow per line) |
| `n8n_full.parquet` | ~118MB | Parquet (for pandas/spark) |

**[→ Download from Releases](https://github.com/Ker102/n8n-workflows-36k/releases)**

---

## 🗂️ Directory Structure

```
workflows/
├── ai-automation-lab/        # 1,464 AI & automation workflows
├── initial_megapack/         # 2,057 general-purpose workflows
├── external/                 # 24,701 community refined workflows
├── synthetic/                # 8,744 synthetic variations
├── box-mcp-demos/            # 10 Box integration demos
├── pinecone-rag-kits/        # 6 RAG starters
├── synapse-pro-ops/          # 2 production workflows
└── self-hosted-ai-starter/   # 1 AI starter template
```

---

## 🔥 Companion: Kaelux Automate

Want an AI that writes n8n workflows from prompts? Check out **[Kaelux Automate](https://github.com/Ker102/Kaelux-Automate)**.

---

## 💖 Support

If this helps you, consider:
- ⭐ **[Star the repo](https://github.com/Ker102/n8n-workflows-36k)**
- 💰 **[Sponsor on GitHub](https://github.com/sponsors/Ker102)**
- 📢 Share with your team

---

## 🤝 Contributing

Have workflows to share? See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📄 License

- **Repository:** [Apache 2.0](./LICENSE)
- **Upstream sources:** See `licenses/` directory

---

Happy automating! 🚀
