/**
 * Rename synthetic/external workflows from hash-based names to descriptive names
 * Based on archetype + integrations metadata
 * 
 * Usage: node scripts/rename-workflows.mjs
 */

import { promises as fs } from 'fs';
import fsSync from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const WORKFLOWS_DIR = path.join(ROOT, 'workflows');

// Folders to process (only synthetic and external have hash names)
const FOLDERS_TO_RENAME = ['synthetic', 'external'];

// Helper to create a safe filename
function sanitizeFilename(name) {
    return name
        .toLowerCase()
        .replace(/[^a-z0-9_-]/g, '_')
        .replace(/_+/g, '_')
        .replace(/^_|_$/g, '')
        .substring(0, 80);
}

// Generate descriptive name from workflow content
function generateName(workflow, originalName) {
    const parts = [];

    // Get archetype if available (from meta or folder structure)
    if (workflow.meta?.archetype) {
        parts.push(workflow.meta.archetype);
    }

    // Get nodes/integrations
    const nodes = workflow.nodes || [];
    const nodeTypes = new Set();

    // Skip these common/utility nodes
    const SKIP_NODES = new Set([
        'n8n-nodes-base.set', 'n8n-nodes-base.code', 'n8n-nodes-base.noOp',
        'n8n-nodes-base.stickyNote', 'n8n-nodes-base.merge', 'n8n-nodes-base.if',
        'n8n-nodes-base.switch', 'n8n-nodes-base.function', 'n8n-nodes-base.start'
    ]);

    nodes.forEach(node => {
        if (node.type && !SKIP_NODES.has(node.type)) {
            // Extract the node name (e.g., 'slack' from 'n8n-nodes-base.slack')
            const match = node.type.match(/n8n-nodes-base\.(\w+)/);
            if (match) {
                nodeTypes.add(match[1]);
            } else if (node.type.includes('.')) {
                nodeTypes.add(node.type.split('.').pop());
            }
        }
    });

    // Add up to 4 integrations to the name
    const integrations = Array.from(nodeTypes).slice(0, 4);
    if (integrations.length > 0) {
        parts.push(...integrations);
    }

    // If we still have no meaningful parts, use the workflow name or original
    if (parts.length === 0) {
        if (workflow.name && workflow.name !== originalName) {
            parts.push(workflow.name);
        } else {
            // Keep original hash but prefix with category
            return originalName;
        }
    }

    return sanitizeFilename(parts.join('_'));
}

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
    console.log('Renaming workflows with descriptive names...\n');

    const stats = {
        processed: 0,
        renamed: 0,
        skipped: 0,
        errors: 0,
        duplicates: 0
    };

    // Track used names to avoid duplicates
    const usedNames = new Map(); // name -> count

    for (const folder of FOLDERS_TO_RENAME) {
        const folderPath = path.join(WORKFLOWS_DIR, folder);
        if (!fsSync.existsSync(folderPath)) {
            console.log(`Folder ${folder} not found, skipping...`);
            continue;
        }

        console.log(`Processing ${folder}/...`);
        const files = await walkDir(folderPath);

        for (const filePath of files) {
            stats.processed++;

            try {
                const content = await fs.readFile(filePath, 'utf8');
                const workflow = JSON.parse(content);
                const originalName = path.basename(filePath, '.json');

                // Skip if already has a descriptive name (not just a hash)
                if (!/^[0-9a-f]{12,}$/i.test(originalName) && !/^\d{4}_/.test(originalName)) {
                    stats.skipped++;
                    continue;
                }

                // Generate new name
                let newName = generateName(workflow, originalName);

                // Handle duplicates by adding a counter
                const baseName = newName;
                let counter = usedNames.get(baseName) || 0;
                if (counter > 0) {
                    newName = `${baseName}_${counter}`;
                    stats.duplicates++;
                }
                usedNames.set(baseName, counter + 1);

                // Create new path
                const dir = path.dirname(filePath);
                const newPath = path.join(dir, `${newName}.json`);

                // Skip if same name
                if (filePath === newPath) {
                    stats.skipped++;
                    continue;
                }

                // Rename file
                await fs.rename(filePath, newPath);
                stats.renamed++;

                if (stats.renamed <= 10) {
                    console.log(`  ${originalName} → ${newName}`);
                } else if (stats.renamed === 11) {
                    console.log('  ... (showing first 10 renames)');
                }

            } catch (e) {
                stats.errors++;
                if (stats.errors <= 5) {
                    console.error(`  Error processing ${filePath}: ${e.message}`);
                }
            }
        }
    }

    console.log('\n=== RENAME COMPLETE ===');
    console.log(`Processed: ${stats.processed}`);
    console.log(`Renamed:   ${stats.renamed}`);
    console.log(`Skipped:   ${stats.skipped}`);
    console.log(`Duplicates handled: ${stats.duplicates}`);
    console.log(`Errors:    ${stats.errors}`);

    console.log('\nNext steps:');
    console.log('1. Regenerate manifest: node scripts/generate-manifest.mjs');
    console.log('2. Commit changes: git add -A && git commit -m "rename workflows with descriptive names"');
}

main().catch(console.error);
