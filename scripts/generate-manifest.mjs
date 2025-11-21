import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const WORKFLOWS_DIR = path.join(ROOT, 'workflows');
const OUTPUT_FILE = path.join(ROOT, 'web/public/workflows.json');

const COLLECTION_META = {
  'community-mega-pack': {
    label: 'Community Mega Pack',
    description: 'General-purpose automations covering marketing, ops, CRM, enrichment, and more.'
  },
  'ai-automation-lab': {
    label: 'AI Automation Lab',
    description: 'AI-first agents, copilots, enrichment flows, and RAG building blocks.'
  },
  'pinecone-rag-kits': {
    label: 'Pinecone RAG Kits',
    description: 'Retrieval-augmented generation starters powered by Pinecone indexes.'
  },
  'box-mcp-demos': {
    label: 'Box MCP Demos',
    description: 'Sample Box MCP workflows for DocGen, metadata, and insurance use cases.'
  },
  'synapse-pro-ops': {
    label: 'Synapse Pro Ops',
    description: 'Production-grade automations shared by ProfSynapse.'
  },
  'self-hosted-ai-starter': {
    label: 'Self-Hosted AI Starter',
    description: 'n8n self-hosted AI starter kit demo workflows.'
  }
};

async function walkDir(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...await walkDir(fullPath));
    } else if (entry.isFile() && entry.name.endsWith('.json')) {
      files.push(fullPath);
    }
  }
  return files;
}

async function main() {
  const dirEntries = await fs.readdir(WORKFLOWS_DIR, { withFileTypes: true });
  const categories = [];
  let total = 0;

  for (const entry of dirEntries) {
    if (!entry.isDirectory()) continue;
    const categoryId = entry.name;
    const meta = COLLECTION_META[categoryId] ?? {
      label: categoryId,
      description: 'Community-contributed workflows.'
    };

    const absoluteCategoryPath = path.join(WORKFLOWS_DIR, categoryId);
    const files = await walkDir(absoluteCategoryPath);
    const workflows = await Promise.all(files.map(async (filePath) => {
      const stats = await fs.stat(filePath);
      let metadata = {
        nodeCount: 0,
        complexity: 'basic',
        integrations: [],
        credentials: []
      };

      try {
        const content = await fs.readFile(filePath, 'utf8');
        const workflow = JSON.parse(content);
        const nodes = workflow.nodes || [];

        // Complexity
        metadata.nodeCount = nodes.length;
        if (metadata.nodeCount > 15) metadata.complexity = 'advanced';
        else if (metadata.nodeCount > 6) metadata.complexity = 'intermediate';

        // Integrations & Credentials
        const integrations = new Set();
        const credentials = new Set();

        const CORE_NODES = new Set([
          'n8n-nodes-base.manualTrigger', 'n8n-nodes-base.start', 'n8n-nodes-base.set',
          'n8n-nodes-base.splitInBatches', 'n8n-nodes-base.stickyNote', 'n8n-nodes-base.merge',
          'n8n-nodes-base.if', 'n8n-nodes-base.switch', 'n8n-nodes-base.noOp',
          'n8n-nodes-base.wait', 'n8n-nodes-base.executeWorkflow', 'n8n-nodes-base.code',
          'n8n-nodes-base.function', 'n8n-nodes-base.functionItem', 'n8n-nodes-base.itemLists',
          'n8n-nodes-base.moveBinaryData', 'n8n-nodes-base.writeBinaryFile',
          'n8n-nodes-base.readBinaryFile', 'n8n-nodes-base.spreadsheetFile',
          'n8n-nodes-base.dateTime', 'n8n-nodes-base.scheduleTrigger', 'n8n-nodes-base.webhook',
          'n8n-nodes-base.httpRequest', 'n8n-nodes-base.cron', 'n8n-nodes-base.interval'
        ]);

        nodes.forEach(node => {
          // Integrations
          if (node.type && !CORE_NODES.has(node.type) && node.type.startsWith('n8n-nodes-base.')) {
            const name = node.type.replace('n8n-nodes-base.', '');
            integrations.add(name);
          }
          // Credentials
          if (node.credentials) {
            Object.keys(node.credentials).forEach(cred => credentials.add(cred));
          }
        });

        metadata.integrations = Array.from(integrations).sort();
        metadata.credentials = Array.from(credentials).sort();

      } catch (e) {
        console.warn(`Failed to parse ${filePath}: ${e.message}`);
      }

      return {
        name: path.basename(filePath, '.json'),
        fileName: path.basename(filePath),
        relativePath: path.relative(ROOT, filePath).replace(/\\/g, '/'),
        categoryId,
        sizeBytes: stats.size,
        ...metadata
      };
    }));

    workflows.sort((a, b) => a.fileName.localeCompare(b.fileName));

    categories.push({
      id: categoryId,
      label: meta.label,
      description: meta.description,
      count: workflows.length,
      workflows
    });
    total += workflows.length;
  }

  categories.sort((a, b) => a.label.localeCompare(b.label));

  const manifest = {
    generatedAt: new Date().toISOString(),
    totalWorkflows: total,
    categoryCount: categories.length,
    categories
  };

  await fs.mkdir(path.dirname(OUTPUT_FILE), { recursive: true });
  await fs.writeFile(OUTPUT_FILE, JSON.stringify(manifest, null, 2));
  console.log(`Manifest created at ${OUTPUT_FILE}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
