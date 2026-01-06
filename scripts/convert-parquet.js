const parquet = require('parquetjs');
const fs = require('fs');

async function convertParquetToJsonl() {
    console.log('Opening parquet file...');
    let reader;
    try {
        reader = await parquet.ParquetReader.openFile('n8n_workflows_dataset.parquet');
    } catch (e) {
        console.error('Failed to open parquet file:', e);
        return;
    }

    console.log('Reading rows...');
    const cursor = reader.getCursor();
    let record = null;
    let count = 0;
    
    const outputStream = fs.createWriteStream('converted_external.jsonl', { flags: 'a' });

    while (record = await cursor.next()) {
        // The record structure depends on the parquet schema.
        // We assume it has a column with the JSON content or similar.
        // Let\'s log the first record to see the structure.
        if (count === 0) {
            console.log('First record structure:', Object.keys(record));
        }

        // Based on the user\'s previous context, it\'s likely a list of workflows.
        // We need to map it to our format.
        // If the record has 'workflow_json' or similar, we use that.
        // For now, let\'s just dump the record to see what we have, 
        // but since we want to append to our dataset, we need to be careful.
        // Let\'s first just dump raw JSONL to a temp file and inspect it.
        
        outputStream.write(JSON.stringify(record) + '\n');
        count++;
        if (count % 1000 === 0) console.log(`Processed ${count} rows`);
    }

    await reader.close();
    outputStream.end();
    console.log(`Finished converting ${count} rows.`);
}

convertParquetToJsonl().catch(console.error);
