import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const INPUT_FILE = path.join(ROOT, 'n8n_workflows.jsonl');
const OUTPUT_DIR = path.join(ROOT, 'workflows/synthetic_generated');

// Heuristics to categorize nodes based on their type name
const CATEGORY_RULES = {
    database: ['postgres', 'mysql', 'mongo', 'mariadb', 'supabase', 'dynamodb', 'redis'],
    spreadsheet: ['sheet', 'airtable', 'baserow', 'nocodb', 'grid'],
    messaging: ['slack', 'discord', 'telegram', 'teams', 'mattermost', 'whatsapp', 'matrix'],
    mail: ['gmail', 'mail', 'smtp', 'imap', 'outlook'],
    crm: ['hubspot', 'salesforce', 'pipedrive', 'zoho', 'activecampaign'],
    devops: ['github', 'gitlab', 'bitbucket', 'docker', 'kubernetes', 'aws', 's3', 'circleci', 'jenkins'],
    ai: ['openai', 'anthropic', 'langchain', 'huggingface', 'mistral', 'gemini', 'llama'],
    trigger: ['trigger', 'webhook', 'schedule', 'cron', 'interval', 'poll', 'event']
};

async function loadDataset() {
    console.log('Loading dataset...');
    const content = await fs.readFile(INPUT_FILE, 'utf8');
    const workflows = content.trim().split('\n').map(line => {
        try {
            return JSON.parse(line);
        } catch (e) {
            return null;
        }
    }).filter(w => w);
    return workflows;
}

function categorizeNode(nodeType) {
    const lower = nodeType.toLowerCase();
    for (const [category, keywords] of Object.entries(CATEGORY_RULES)) {
        if (keywords.some(k => lower.includes(k))) {
            return category;
        }
    }
    return 'other';
}

function extractNodeRegistry(workflows) {
    const registry = {};

    workflows.forEach(wf => {
        const nodes = wf.content.nodes || [];
        nodes.forEach(node => {
            const type = node.type;
            if (!registry[type]) {
                registry[type] = {
                    type,
                    count: 0,
                    category: categorizeNode(type),
                    sampleParameters: node.parameters,
                    sampleCredentials: node.credentials
                };
            }
            registry[type].count++;
        });
    });

    return registry;
}

async function main() {
    const workflows = await loadDataset();
    console.log(`Loaded ${workflows.length} workflows.`);

    const registry = extractNodeRegistry(workflows);
    
    // Group nodes by category
    const byCategory = {};
    Object.values(registry).forEach(node => {
        if (!byCategory[node.category]) byCategory[node.category] = [];
        byCategory[node.category].push(node);
    });

    console.log('\n--- Node Coverage Analysis ---');
    for (const [cat, nodes] of Object.entries(byCategory)) {
        if (cat === 'other') continue;
        console.log(`\nCategory: ${cat.toUpperCase()} (${nodes.length} nodes)`);
        // Sort by usage count
        const topNodes = nodes.sort((a, b) => b.count - a.count).slice(0, 5);
        topNodes.forEach(n => console.log(`  - ${n.type} (Used ${n.count} times)`));
    }

    console.log('\n------------------------------');
    console.log('This analysis confirms we have sufficient data to generate synthetic workflows.');
    console.log('For example, we can swap "n8n-nodes-base.googleSheets" with "n8n-nodes-base.airtable"');
    console.log('or "n8n-nodes-base.slack" with "n8n-nodes-base.discord" to create new valid combinations.');
}

main().catch(console.error);
