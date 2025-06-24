#!/usr/bin/env node
/**
 * JSON Schema Validation Script for servers.json
 * ==============================================
 * 
 * This script validates the servers.json file against the JSON schema
 * using AJV with format support.
 */

const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const fs = require('fs');
const path = require('path');

function main() {
    const schemaFile = path.join(process.cwd(), 'data', 'schema.json');
    const dataFile = path.join(process.cwd(), 'data', 'servers.json');
    
    // Check if files exist
    if (!fs.existsSync(schemaFile)) {
        console.error(`❌ Schema file not found: ${schemaFile}`);
        process.exit(1);
    }
    
    if (!fs.existsSync(dataFile)) {
        console.error(`❌ Data file not found: ${dataFile}`);
        process.exit(1);
    }
    
    let schema, data;
    
    try {
        schema = JSON.parse(fs.readFileSync(schemaFile, 'utf8'));
    } catch (error) {
        console.error(`❌ Failed to parse schema file: ${error.message}`);
        process.exit(1);
    }
    
    try {
        data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
    } catch (error) {
        console.error(`❌ Failed to parse data file: ${error.message}`);
        process.exit(1);
    }
    
    // Create AJV instance with formats
    const ajv = new Ajv({ allErrors: true });
    addFormats(ajv);
    
    // Compile and validate
    const validate = ajv.compile(schema);
    const valid = validate(data);
    
    if (!valid) {
        console.log('❌ Schema validation failed:');
        validate.errors.forEach((error, index) => {
            console.log(`${index + 1}. ${error.instancePath || 'root'}: ${error.message}`);
            if (error.data !== undefined) {
                console.log(`   Data: ${JSON.stringify(error.data)}`);
            }
        });
        process.exit(1);
    } else {
        console.log('✅ JSON schema validation passed');
    }
}

if (require.main === module) {
    main();
}

module.exports = { main };