[![Star This Repo](https://img.shields.io/badge/⭐%20Star%20this%20repo-222?style=for-the-badge)](https://github.com/Ker102/n8n-workflows-36k)

# 🌌 n8n Automation Atlas

![Total](https://img.shields.io/badge/Total%20Workflows-131,648-blueviolet?style=for-the-badge)
![Importable](https://img.shields.io/badge/Importable-36,985-green?style=for-the-badge)
![Vectors](https://img.shields.io/badge/RAG%20Vectors-36,166-FF4F64?style=for-the-badge)
![Fine-Tuning](https://img.shields.io/badge/Fine--Tuning-In%20Progress-orange?style=for-the-badge)

### 🔧 Core Tech Stack
![n8n](https://img.shields.io/badge/n8n%201.x-EA4B71?style=flat-square&logo=n8n&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js%203-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white)
![Vite](https://img.shields.io/badge/Vite%205-646CFF?style=flat-square&logo=vite&logoColor=white)
![Python](https://img.shields.io/badge/Python%203.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js%2022-339933?style=flat-square&logo=nodedotjs&logoColor=white)

### 🧠 AI & RAG Infrastructure
![Qdrant](https://img.shields.io/badge/Qdrant%20Cloud-FF4F64?style=flat-square&logo=qdrant&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini%203-Pro%20Preview-4285F4?style=flat-square&logo=google&logoColor=white)
![Together AI](https://img.shields.io/badge/Together%20AI-M2--BERT-FF6B6B?style=flat-square)
![Qwen](https://img.shields.io/badge/Qwen%203-Coder%2014B-7C3AED?style=flat-square)
![Unsloth](https://img.shields.io/badge/Unsloth-Training-orange?style=flat-square)

### 🚀 Hosting
![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=flat-square&logo=huggingface&logoColor=black)

> **131,648 n8n workflows** — the world's largest open-source n8n workflow dataset.  
> **36,166 vectors** in Qdrant Cloud for RAG-powered workflow retrieval.  
> **🔥 Custom Qwen 3 Coder 14B** fine-tuning in progress with 21,925 cleaned examples.

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

## 🧠 RAG Infrastructure

This dataset powers a production RAG system for AI-assisted workflow generation:

| Component | Details |
|-----------|---------|
| **Vector Database** | Qdrant Cloud (1GB free tier) |
| **Embeddings** | Together AI M2-BERT (768-dim) |
| **Vectors Indexed** | 36,166 workflows |
| **Query Latency** | ~50ms semantic search |

### Fine-Tuning Dataset

| File | Examples | Purpose |
|------|----------|---------|
| `training_data_clean.jsonl` | 21,925 | Cleaned instruction-output pairs |
| `finetune_train.jsonl` | 19,732 | Unsloth/HuggingFace format |
| `finetune_vertex_train.jsonl` | 19,732 | Vertex AI Gemini format |

```bash
# Query similar workflows
python scripts/query-qdrant.py "create a slack notification workflow"
```

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
