import fsSync from 'fs';
import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import readline from 'readline';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const INPUT_FILE = path.join(ROOT, 'n8n_workflows.jsonl');
const OUTPUT_DIR = path.join(ROOT, 'workflows');

// Source categories based on meta.source or meta.archetype
const CATEGORY_MAP = {
    'synthetic': 'synthetic',      // meta.generated === true
    'external_community': 'external', // meta.source === 'external_community'
    'repository': null             // Keep in original category folder
};

async function ensureDir(dir) {
    if (!fsSync.existsSync(dir)) {
        await fs.mkdir(dir, { recursive: true });
    }
}

async function main() {
    console.log('Splitting n8n_workflows.jsonl into individual files...\n');

    const fileStream = fsSync.createReadStream(INPUT_FILE);
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    const stats = {
        total: 0,
        synthetic: 0,
        external: 0,
        repository: 0,
        errors: 0
    };

    // Ensure output directories exist
    await ensureDir(path.join(OUTPUT_DIR, 'synthetic'));
    await ensureDir(path.join(OUTPUT_DIR, 'external'));

    for await (const line of rl) {
        if (!line.trim()) continue;

        try {
            const record = JSON.parse(line);
            stats.total++;

            // Determine category based on meta
            let category;
            let subFolder = '';

            if (record.meta?.generated === true || record.meta?.archetype) {
                category = 'synthetic';
                // Use archetype as subfolder if available
                if (record.meta?.archetype) {
                    subFolder = record.meta.archetype;
                }
                stats.synthetic++;
            } else if (record.meta?.source === 'external_community') {
                category = 'external';
                stats.external++;
            } else if (record.category) {
                // Repository workflow - use existing category
                category = record.category;
                stats.repository++;
            } else {
                category = 'uncategorized';
                stats.repository++;
            }

            // Create safe filename from id or name
            const rawId = record.id || record.name || `workflow_${stats.total}`;
            const safeId = String(rawId)
                .replace(/[^a-zA-Z0-9_-]/g, '_')
                .substring(0, 100);

            const fileName = `${safeId}.json`;

            // Build output path
            let outputPath;
            if (subFolder) {
                await ensureDir(path.join(OUTPUT_DIR, category, subFolder));
                outputPath = path.join(OUTPUT_DIR, category, subFolder, fileName);
            } else {
                await ensureDir(path.join(OUTPUT_DIR, category));
                outputPath = path.join(OUTPUT_DIR, category, fileName);
            }

            // Write individual workflow file (only the content, not the wrapper)
            const workflowContent = record.content || record;
            await fs.writeFile(outputPath, JSON.stringify(workflowContent, null, 2));

            if (stats.total % 5000 === 0) {
                console.log(`Processed ${stats.total} workflows...`);
            }
        } catch (e) {
            stats.errors++;
            if (stats.errors <= 5) {
                console.error(`Error processing line ${stats.total + 1}:`, e.message);
            }
        }
    }

    console.log('\n=== SPLIT COMPLETE ===');
    console.log(`Total workflows:    ${stats.total}`);
    console.log(`  Synthetic:        ${stats.synthetic}`);
    console.log(`  External:         ${stats.external}`);
    console.log(`  Repository:       ${stats.repository}`);
    console.log(`Errors:             ${stats.errors}`);
    console.log(`\nOutput directory: ${OUTPUT_DIR}`);
}

main().catch(console.error);
