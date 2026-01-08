/**
 * Apply semantic labels to workflows using internal workflow name matching
 * Reads each workflow's 'name' field and matches against cluster assignments
 * 
 * Usage: node scripts/apply-semantic-labels-v2.mjs
 */

import { promises as fs } from 'fs';
import fsSync from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const CLUSTERS_FILE = path.join(ROOT, 'workflow_clusters.json');
const WORKFLOWS_DIR = path.join(ROOT, 'workflows');

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
    console.log('Applying semantic labels (v2 - name matching)...\n');

    // Load cluster assignments
    const clustersData = JSON.parse(await fs.readFile(CLUSTERS_FILE, 'utf8'));
    const assignments = clustersData.assignments;
    const clusterInfo = clustersData.cluster_info;

    // Build lookup by name (lowercase for case-insensitive matching)
    const nameLookup = new Map();
    for (const [key, value] of Object.entries(assignments)) {
        nameLookup.set(key.toLowerCase(), value);
        // Also add without special chars
        const simplified = key.toLowerCase().replace(/[^a-z0-9]/g, '');
        nameLookup.set(simplified, value);
    }

    console.log(`Loaded ${Object.keys(assignments).length} cluster assignments\n`);

    const stats = {
        processed: 0,
        labeled: 0,
        notFound: 0,
        errors: 0
    };

    const allFiles = await walkDir(WORKFLOWS_DIR);
    console.log(`Found ${allFiles.length} workflow files\n`);

    for (const filePath of allFiles) {
        stats.processed++;

        try {
            const content = await fs.readFile(filePath, 'utf8');
            const workflow = JSON.parse(content);

            // Try multiple matching strategies
            const workflowName = workflow.name || '';
            const workflowId = workflow.id || '';
            const fileName = path.basename(filePath, '.json');

            // Try to find assignment
            let assignment =
                nameLookup.get(workflowName.toLowerCase()) ||
                nameLookup.get(workflowId.toLowerCase()) ||
                nameLookup.get(workflowName.toLowerCase().replace(/[^a-z0-9]/g, '')) ||
                nameLookup.get(fileName.toLowerCase()) ||
                assignments[workflowName] ||
                assignments[workflowId];

            if (!assignment) {
                stats.notFound++;
                continue;
            }

            // Apply semantic label
            if (!workflow.meta) workflow.meta = {};
            workflow.meta.semanticLabel = assignment.label;
            workflow.meta.clusterId = assignment.cluster;

            // Write back
            await fs.writeFile(filePath, JSON.stringify(workflow, null, 2));
            stats.labeled++;

            if (stats.processed % 5000 === 0) {
                console.log(`Processed ${stats.processed}/${allFiles.length}... (${stats.labeled} labeled)`);
            }

        } catch (e) {
            stats.errors++;
            if (stats.errors <= 5) {
                console.error(`Error: ${filePath} - ${e.message}`);
            }
        }
    }

    console.log('\n=== SEMANTIC LABELS APPLIED ===');
    console.log(`Processed: ${stats.processed}`);
    console.log(`Labeled:   ${stats.labeled}`);
    console.log(`Not found: ${stats.notFound}`);
    console.log(`Errors:    ${stats.errors}`);

    console.log('\nNext steps:');
    console.log('1. Regenerate manifest: node scripts/generate-manifest.mjs');
    console.log('2. Commit changes');
}

main().catch(console.error);
