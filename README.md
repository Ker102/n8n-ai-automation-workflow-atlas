[![Star This Repo](https://img.shields.io/badge/⭐%20Star%20this%20repo-222?style=for-the-badge)](https://github.com/Ker102/n8n-ai-automation-workflow-atlas)

# 🌌 n8n Automation Atlas

![Workflows](https://img.shields.io/badge/Workflows-3831-blueviolet?style=for-the-badge)
![Collections](https://img.shields.io/badge/Collections-6-9cf?style=for-the-badge)
![Formats](https://img.shields.io/badge/Format-n8n%20JSON-0b5fff?style=for-the-badge&logo=json&logoColor=white)
![Future%20Stack](https://img.shields.io/badge/Future%20Builds-Vue%20%2B%20Vite-41b883?style=for-the-badge&logo=vue.js&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-000?style=for-the-badge)

> 3,831 battle-tested n8n workflows curated from top open-source libraries. Everything is trimmed down to ready-to-import JSON exports so you can remix, ship, and scale automations fast.

## 🤗 Welcome, Operators!
Whether you build full-stack AI agents, automate product ops, or just love tinkering with n8n, this atlas is for you. Clone it, remix it, and share your own packs—we would love to showcase community-built automations here.

## 💖 Support the Atlas
Keeping a living automation library online (and refreshing all upstream sources) takes time. If these workflows save you cycles, please consider:

- [**Sponsoring on GitHub**](https://github.com/sponsors/Ker102) to fund future packs and hosting.
- [**Starring the repository**](https://github.com/Ker102/n8n-ai-automation-workflow-atlas) so more builders discover it.
- Sharing the repo/link on socials or inside your team’s automation channel.

## 📚 What's Inside
- **6 themed packs** spanning community mega-collections, AI agents, Pinecone RAG starters, Box MCP demos, and more.
- **Only JSON exports**—no Dockerfiles, datasets, or scripts—making git pulls light and n8n imports instant.
- **Source licenses preserved** inside `licenses/` so you can honor every upstream project's terms when you redistribute.

## 🗺️ Collection Map
| Collection | Focus | Count | Folder | Source License |
| --- | --- | --- | --- | --- |
| Community Mega Pack | General-purpose automations from marketing, ops, CRM, and data tooling. | **2057** | `workflows/community-mega-pack/` | MIT (`licenses/zie619_LICENSE`)
| AI Automation Lab | AI/agent workflows (RAG, enrichment, assistants, chains) built around GPT/OpenAI. | **1764** | `workflows/ai-automation-lab/` | MIT + attribution (`licenses/ultimate-n8n-ai_LICENSE`)
| Box MCP Demos | Box Community demos for metadata, DocGen, and insurance scenarios. | **5** | `workflows/box-mcp-demos/` | MIT (`licenses/box-community_LICENSE`)
| Pinecone RAG Kits | Pinecone + n8n quickstarts for retrieval-augmented assistants. | **3** | `workflows/pinecone-rag-kits/` | MIT (`licenses/pinecone_LICENSE`)
| Synapse Pro Ops | Production-ready automations from ProfSynapse (transcripts, reporting). | **1** | `workflows/synapse-pro-ops/` | MIT (`licenses/prof-synapse_LICENSE`)
| Self-Hosted AI Starter | Demo workflow bundled with n8n's self-hosted AI starter kit. | **1** | `workflows/self-hosted-ai-starter/` | Apache-2.0 (`licenses/n8n-self-hosted_LICENSE`)

### 🔖 Category Rollup
- **AI + Agents:** `ai-automation-lab`, `pinecone-rag-kits`, `self-hosted-ai-starter`
- **Enterprise Integrations:** `box-mcp-demos`, `synapse-pro-ops`
- **Community Essentials:** `community-mega-pack`

## 🛠️ Import Any Workflow Into n8n
1. **Clone or download** this repo so you have the `workflows/` directory locally.
2. In your n8n instance, click **Import > From File** (or paste JSON on an open canvas).
3. **Select a workflow** from the folder that matches the capability you need.
4. n8n will load the nodes; **review credentials** placeholders (OpenAI, Pinecone, Box, HTTP auth, etc.).
5. **Create or link credentials** inside n8n to match the workflow's requirements.
6. Hit **Activate** on the workflow, test with sample data, then customize nodes to fit your stack.

> Tip: Many AI templates expect OpenAI API keys, Pinecone indexes, or vector DB credentials. Keep those handy for a seamless import.

## 🧭 How to Navigate
```text
workflows/
├── ai-automation-lab/         # AI-first agents, copilots, enrichment flows
├── box-mcp-demos/             # Box MCP demos for DocGen & metadata
├── community-mega-pack/       # Massive community collection covering most use cases
├── pinecone-rag-kits/         # Pinecone quickstarts for retrieval workflows
├── self-hosted-ai-starter/    # Template shipped with n8n's AI starter kit
└── synapse-pro-ops/           # ProfSynapse production automations
```

## 🔥 Companion Project: Kaelux Automate
Looking for an AI co-pilot that writes n8n workflows from prompts? Check out [**Kaelux Automate**](https://github.com/Ker102/Kaelux-Automate)—a custom n8n build with an LLM tuned specifically for workflow authoring, scaffolding, and iteration. Pair Kaelux with this atlas to brainstorm flows with AI and then import/extend the generated JSON templates here.

## 🚀 Getting Started (Even If You're New to GitHub)
Pick whichever flow feels easiest—each ends with a ready-to-import JSON file inside n8n.

### Option A · Quick Download from GitHub
1. Scroll to the [`workflows/`](workflows) folder in this repo and drill into the collection you need.
2. Click any `.json` file.
3. Hit the **Raw** button, then **Save As…** (or right-click → Save) to download the JSON locally.
4. In n8n, open the canvas → **Import from File** → choose the JSON you just saved.

### Option B · Fork or Clone the Entire Library
1. Click **Fork** to keep your own copy on GitHub (great if you plan to tweak workflows).
2. Or run `git clone https://github.com/Ker102/n8n-ai-automation-workflow-atlas.git`.
3. Browse workflows locally with your favorite editor/explorer.
4. Import any JSON into n8n via **Import from File** or copy/paste into the editor.

### Option C · Use the Hosted Workflow Explorer
1. Visit the [GitHub Pages explorer](https://ker102.github.io/n8n-ai-automation-workflow-atlas/).
2. Use the search bar and category chips to find a template.
3. Click **Download JSON** or **View on GitHub** right from the page.
4. Import the downloaded file into n8n just like in Options A/B.

> Need help importing? See **🛠️ Import Any Workflow Into n8n** below.

## ⭐ Keep It Handy
If this library saves you time, please:
- **Star** ⭐ the repo so it stays on your radar.
- **Fork** 🍴 it to stash a personal copy and track your tweaks.
- **Watch** 👀 for updates when new workflow drops land.

## 🧰 Future Development
Whenever we add tooling beyond JSON workflows (dashboards, viewers, etc.) we'll ship it with **Vue + Vite** to keep the DX fast. Contributions aligned with that stack are especially welcome.

## 🌐 Workflow Explorer UI
The `web/` directory contains a **Vue + Vite** single-page app that can be deployed to GitHub Pages and lets you search/filter/download every workflow. See `docs/DEPLOYMENT.md` for local dev steps and hosting instructions.

## 🤝 Contributing
We welcome new workflow packs, better documentation, and UX polish. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Workflow submission checklist
- Coding standards for the Vue explorer
- How to open discussions/issues/PRs that get merged fast

Need help or want to pitch an idea? Start a [GitHub Discussion](https://github.com/Ker102/n8n-ai-automation-workflow-atlas/discussions) and we’ll jam with you.

## 📄 License
- **Repository license:** [MIT](./LICENSE) — simple, permissive, and perfect for sharing/remixing these workflows.
- **Upstream licenses:** See `licenses/` for each source. Follow attribution/notice requirements when redistributing.

Happy automating! ⚡
