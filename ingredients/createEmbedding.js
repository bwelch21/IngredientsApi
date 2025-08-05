const https = require('https');
const fs = require('fs');
const path = require('path');

// Replace with your OpenAI API key
const OPENAI_API_KEY = '***REMOVED***';

// Path to the input CSV file
const CSV_FILE_PATH = path.join(__dirname, 'data', 'ingredients.csv');

// Path to the output JSON file
const OUTPUT_FILE_PATH = path.join(__dirname, 'data', 'name_embeddings.json');

// Function to make an HTTPS POST request
function makePostRequest(url, data, headers) {
    return new Promise((resolve, reject) => {
        const urlObject = new URL(url);
        const options = {
            hostname: urlObject.hostname,
            path: urlObject.pathname,
            method: 'POST',
            headers: {
                ...headers,
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(data),
            },
        };

        const req = https.request(options, (res) => {
            let responseData = '';
            res.on('data', (chunk) => {
                responseData += chunk;
            });

            res.on('end', () => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    resolve(JSON.parse(responseData));
                } else {
                    reject(new Error(`HTTP Error: ${res.statusCode} - ${responseData}`));
                }
            });
        });

        req.on('error', (error) => {
            reject(error);
        });

        req.write(data);
        req.end();
    });
}

// Function to generate embeddings for a batch of strings
async function generateEmbeddingsBatch(inputStrings) {
    const url = 'https://api.openai.com/v1/embeddings';
    const data = JSON.stringify({
        model: 'text-embedding-ada-002',
        input: inputStrings,
    });
    const headers = {
        Authorization: `Bearer ${OPENAI_API_KEY}`,
    };

    try {
        const response = await makePostRequest(url, data, headers);
        return response.data.map((result, index) => ({
            Name: inputStrings[index],
            embedding: result.embedding,
        }));
    } catch (error) {
        console.error(`Error generating embeddings for batch:`, error.message);
        throw error;
    }
}

// Function to parse a CSV file into an array of objects
function parseCSV(filePath) {
    const fileContent = fs.readFileSync(filePath, 'utf8');
    const [headerLine, ...lines] = fileContent.trim().split('\n');
    const headers = headerLine.split(',').map((header) => header.trim());

    return lines.map((line) => {
        const values = line.split(',').map((value) => value.trim());
        return headers.reduce((obj, header, index) => {
            obj[header] = values[index];
            return obj;
        }, {});
    });
}

// Function to save embeddings in the required format
function saveEmbeddingsToFile(newEmbeddings) {
    try {
        let existingData = { rows: [] };
        if (fs.existsSync(OUTPUT_FILE_PATH)) {
            existingData = JSON.parse(fs.readFileSync(OUTPUT_FILE_PATH, 'utf8'));
        }

        existingData.rows.push(...newEmbeddings);

        fs.writeFileSync(OUTPUT_FILE_PATH, JSON.stringify(existingData, null, 2), 'utf8');
        console.log(`Embeddings saved to ${OUTPUT_FILE_PATH}`);
    } catch (error) {
        console.error('Error saving embeddings to file:', error.message);
    }
}

// Main function to process the CSV in parallel batches
async function processCSVInBatches(batchSize = 1000) {
    const ingredients = parseCSV(CSV_FILE_PATH);
    const allNames = ingredients.map((ingredient) => ingredient.Name).filter(Boolean); // Extract valid names

    for (let i = 0; i < allNames.length; i += batchSize) {
        const batch = allNames.slice(i, i + batchSize);
        console.log(`Processing batch ${Math.floor(i / batchSize) + 1}: ${batch.length} items`);
        try {
            const embeddings = await generateEmbeddingsBatch(batch);
            saveEmbeddingsToFile(embeddings);
        } catch (error) {
            console.error(`Error processing batch ${Math.floor(i / batchSize) + 1}`);
        }
    }

    console.log('All batches processed.');
}

// Run the script
processCSVInBatches().catch((error) => {
    console.error('An error occurred:', error.message);
});
