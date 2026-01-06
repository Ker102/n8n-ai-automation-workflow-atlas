import { promises as fs } from 'fs';
import fsSync from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import readline from 'readline';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const WORKFLOWS_DIR = path.join(ROOT, 'workflows');
const EXTERNAL_CLEANED = path.join(ROOT, 'n8n_external_cleaned.jsonl');
const SYNTHETIC_JSONL = path.join(ROOT, 'workflows/synthetic_generated.jsonl');
const OUTPUT_FILE = path.join(ROOT, 'n8n_workflows.jsonl');

async function walkDir(dir) {
  if (!fsSync.existsSync(dir)) return [];
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

async function streamJsonl(filePath, outputStream) {
    if (!fsSync.existsSync(filePath)) return 0;
    const fileStream = fsSync.createReadStream(filePath);
    const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });
    let count = 0;
    for await (const line of rl) {
        if (line.trim()) {
            outputStream.write(line + '\n');
            count++;
        }
    }
    return count;
}

async function main() {
  console.log('Building consolidated dataset (Streaming)...');
  const outputStream = fsSync.createWriteStream(OUTPUT_FILE);
  
  let total = 0;

  // 1. Process Raw Repository Workflows
  const dirEntries = await fs.readdir(WORKFLOWS_DIR, { withFileTypes: true });
  for (const entry of dirEntries) {
    if (!entry.isDirectory()) continue;
    if (entry.name === 'synthetic_generated') continue; // Handled separately if it's a directory, but we moved to jsonl

    const absoluteCategoryPath = path.join(WORKFLOWS_DIR, entry.name);
    const files = await walkDir(absoluteCategoryPath);

    for (const filePath of files) {
      try {
        const contentStr = await fs.readFile(filePath, 'utf8');
        const workflow = JSON.parse(contentStr);
        const nodes = workflow.nodes || [];

        const integrations = new Set();
        nodes.forEach(node => {
          if (node.type && node.type.startsWith('n8n-nodes-base.')) {
            integrations.add(node.type.replace('n8n-nodes-base.', ''));
          }
        });

        const record = {
          id: workflow.id || path.basename(filePath, '.json'),
          name: workflow.name || path.basename(filePath, '.json'),
          node_count: nodes.length,
          integrations: Array.from(integrations).sort(),
          category: entry.name,
          content: workflow,
          meta: workflow.meta || { source: 'repository' }
        };

        outputStream.write(JSON.stringify(record) + '\n');
        total++;
      } catch (e) { }
    }
  }
  console.log(`Repository workflows: ${total}`);

  // 2. Stream Synthetic Workflows
  console.log('Streaming synthetic workflows...');
  const syntheticCount = await streamJsonl(SYNTHETIC_JSONL, outputStream);
  total += syntheticCount;
  console.log(`Synthetic workflows: ${syntheticCount}`);

  // 3. Stream External Cleaned Workflows
  console.log('Streaming external cleaned workflows...');
  const externalCount = await streamJsonl(EXTERNAL_CLEANED, outputStream);
  total += externalCount;
  console.log(`External workflows: ${externalCount}`);

  outputStream.end();
  console.log(`\nDONE! Final dataset contains ${total} workflows.`);
  console.log(`Output: ${OUTPUT_FILE}`);
}

main().catch(console.error);
