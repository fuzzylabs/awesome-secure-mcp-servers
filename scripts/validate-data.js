#!/usr/bin/env node
/**
 * Data Validation Script for MCP Server Data
 * ==========================================
 * 
 * This script validates the servers.json file for:
 * - Required fields presence
 * - Data consistency
 * - Version format validation
 * - URL format validation
 */

const fs = require('fs');
const path = require('path');

class DataValidator {
    constructor() {
        this.errors = [];
        this.warnings = [];
    }

    validateServersData(data) {
        console.log('🔍 Starting data validation...');
        
        // Validate root structure
        this.validateRootStructure(data);
        
        // Validate each server
        if (data.servers && Array.isArray(data.servers)) {
            data.servers.forEach((server, index) => {
                this.validateServer(server, index);
            });
        }
        
        // Check for duplicates
        this.checkForDuplicates(data.servers || []);
        
        // Print results
        this.printResults();
        
        return this.errors.length === 0;
    }

    validateRootStructure(data) {
        const requiredFields = ['servers', 'last_updated', 'schema_version'];
        
        requiredFields.forEach(field => {
            if (!data.hasOwnProperty(field)) {
                this.errors.push(`Missing required root field: ${field}`);
            }
        });

        // Validate schema version format
        if (data.schema_version && !/^\d+\.\d+\.\d+$/.test(data.schema_version)) {
            this.errors.push(`Invalid schema_version format: ${data.schema_version}`);
        }

        // Validate last_updated format
        if (data.last_updated && !this.isValidISODate(data.last_updated)) {
            this.errors.push(`Invalid last_updated format: ${data.last_updated}`);
        }
    }

    validateServer(server, index) {
        const serverPrefix = `Server ${index} (${server.name || 'unnamed'})`;
        
        // Required fields
        const requiredFields = ['name', 'slug', 'repository', 'category', 'description', 'versions'];
        
        requiredFields.forEach(field => {
            if (!server.hasOwnProperty(field)) {
                this.errors.push(`${serverPrefix}: Missing required field '${field}'`);
            }
        });

        // Validate slug format
        if (server.slug && !/^[a-z0-9-]+$/.test(server.slug)) {
            this.errors.push(`${serverPrefix}: Invalid slug format '${server.slug}' (must be lowercase alphanumeric with hyphens)`);
        }

        // Validate repository URL
        if (server.repository && !this.isValidURL(server.repository)) {
            this.errors.push(`${serverPrefix}: Invalid repository URL '${server.repository}'`);
        }

        // Validate category
        const validCategories = ['official', 'enterprise', 'community', 'security-tools', 'under-review', 'deprecated'];
        if (server.category && !validCategories.includes(server.category)) {
            this.errors.push(`${serverPrefix}: Invalid category '${server.category}' (must be one of: ${validCategories.join(', ')})`);
        }

        // Validate versions array
        if (server.versions) {
            if (!Array.isArray(server.versions)) {
                this.errors.push(`${serverPrefix}: 'versions' must be an array`);
            } else if (server.versions.length === 0) {
                this.warnings.push(`${serverPrefix}: No versions defined`);
            } else {
                server.versions.forEach((version, vIndex) => {
                    this.validateVersion(version, `${serverPrefix} version ${vIndex}`);
                });
            }
        }

        // Validate MCP protocol versions
        if (server.mcp_protocol_versions) {
            if (!Array.isArray(server.mcp_protocol_versions)) {
                this.errors.push(`${serverPrefix}: 'mcp_protocol_versions' must be an array`);
            } else {
                server.mcp_protocol_versions.forEach(version => {
                    if (!/^\d{4}-\d{2}-\d{2}$/.test(version)) {
                        this.errors.push(`${serverPrefix}: Invalid MCP protocol version format '${version}' (must be YYYY-MM-DD)`);
                    }
                });
            }
        }

        // Validate maintainer
        if (server.maintainer) {
            this.validateMaintainer(server.maintainer, serverPrefix);
        }

        // Validate tags
        if (server.tags && !Array.isArray(server.tags)) {
            this.errors.push(`${serverPrefix}: 'tags' must be an array`);
        }
    }

    validateVersion(version, versionPrefix) {
        // Required fields for version
        const requiredFields = ['version', 'security_status', 'is_recommended'];
        
        requiredFields.forEach(field => {
            if (!version.hasOwnProperty(field)) {
                this.errors.push(`${versionPrefix}: Missing required field '${field}'`);
            }
        });

        // Validate version format (semantic versioning)
        if (version.version && !/^\d+\.\d+\.\d+(-[\w\.-]+)?(\+[\w\.-]+)?$/.test(version.version)) {
            this.warnings.push(`${versionPrefix}: Version '${version.version}' doesn't follow semantic versioning`);
        }

        // Validate security status
        const validStatuses = ['verified-secure', 'conditional', 'under-review', 'not-recommended', 'deprecated'];
        if (version.security_status && !validStatuses.includes(version.security_status)) {
            this.errors.push(`${versionPrefix}: Invalid security_status '${version.security_status}' (must be one of: ${validStatuses.join(', ')})`);
        }

        // Validate boolean fields
        if (version.is_recommended !== undefined && typeof version.is_recommended !== 'boolean') {
            this.errors.push(`${versionPrefix}: 'is_recommended' must be a boolean`);
        }

        // Validate dates
        if (version.release_date && !this.isValidDate(version.release_date)) {
            this.errors.push(`${versionPrefix}: Invalid release_date format '${version.release_date}'`);
        }

        if (version.deprecation_date && !this.isValidDate(version.deprecation_date)) {
            this.errors.push(`${versionPrefix}: Invalid deprecation_date format '${version.deprecation_date}'`);
        }

        // Validate security scan
        if (version.security_scan) {
            this.validateSecurityScan(version.security_scan, versionPrefix);
        }

        // Validate vulnerabilities
        if (version.vulnerabilities) {
            if (!Array.isArray(version.vulnerabilities)) {
                this.errors.push(`${versionPrefix}: 'vulnerabilities' must be an array`);
            } else {
                version.vulnerabilities.forEach((vuln, vIndex) => {
                    this.validateVulnerability(vuln, `${versionPrefix} vulnerability ${vIndex}`);
                });
            }
        }
    }

    validateMaintainer(maintainer, serverPrefix) {
        const requiredFields = ['name', 'type'];
        
        requiredFields.forEach(field => {
            if (!maintainer.hasOwnProperty(field)) {
                this.errors.push(`${serverPrefix} maintainer: Missing required field '${field}'`);
            }
        });

        const validTypes = ['individual', 'organization', 'official'];
        if (maintainer.type && !validTypes.includes(maintainer.type)) {
            this.errors.push(`${serverPrefix} maintainer: Invalid type '${maintainer.type}' (must be one of: ${validTypes.join(', ')})`);
        }

        if (maintainer.contact && !this.isValidURL(maintainer.contact) && !this.isValidEmail(maintainer.contact)) {
            this.warnings.push(`${serverPrefix} maintainer: Contact '${maintainer.contact}' should be a valid URL or email`);
        }
    }

    validateSecurityScan(scan, versionPrefix) {
        const requiredFields = ['scan_date', 'overall_score'];
        
        requiredFields.forEach(field => {
            if (!scan.hasOwnProperty(field)) {
                this.errors.push(`${versionPrefix} security_scan: Missing required field '${field}'`);
            }
        });

        if (scan.scan_date && !this.isValidISODate(scan.scan_date)) {
            this.errors.push(`${versionPrefix} security_scan: Invalid scan_date format '${scan.scan_date}'`);
        }

        if (scan.overall_score !== undefined) {
            if (typeof scan.overall_score !== 'number' || scan.overall_score < 0 || scan.overall_score > 100) {
                this.errors.push(`${versionPrefix} security_scan: overall_score must be a number between 0 and 100`);
            }
        }

        // Validate scan results
        const scanTypes = ['static_analysis', 'dependency_scan', 'container_scan', 'tool_poisoning_check'];
        scanTypes.forEach(scanType => {
            if (scan[scanType]) {
                this.validateScanResult(scan[scanType], `${versionPrefix} security_scan.${scanType}`);
            }
        });

        // Validate manual review
        if (scan.manual_review) {
            this.validateManualReview(scan.manual_review, `${versionPrefix} security_scan.manual_review`);
        }
    }

    validateScanResult(result, resultPrefix) {
        const validStatuses = ['pass', 'fail', 'warning', 'not-applicable'];
        if (result.status && !validStatuses.includes(result.status)) {
            this.errors.push(`${resultPrefix}: Invalid status '${result.status}' (must be one of: ${validStatuses.join(', ')})`);
        }

        if (result.score !== undefined) {
            if (typeof result.score !== 'number' || result.score < 0 || result.score > 100) {
                this.errors.push(`${resultPrefix}: score must be a number between 0 and 100`);
            }
        }

        if (result.issues_found !== undefined) {
            if (typeof result.issues_found !== 'number' || result.issues_found < 0 || !Number.isInteger(result.issues_found)) {
                this.errors.push(`${resultPrefix}: issues_found must be a non-negative integer`);
            }
        }
    }

    validateManualReview(review, reviewPrefix) {
        const requiredFields = ['reviewer', 'review_date'];
        
        requiredFields.forEach(field => {
            if (!review.hasOwnProperty(field)) {
                this.errors.push(`${reviewPrefix}: Missing required field '${field}'`);
            }
        });

        if (review.review_date && !this.isValidDate(review.review_date)) {
            this.errors.push(`${reviewPrefix}: Invalid review_date format '${review.review_date}'`);
        }

        // Validate review results
        const reviewTypes = ['architecture_review', 'authentication_review', 'authorization_review', 'documentation_review'];
        reviewTypes.forEach(reviewType => {
            if (review[reviewType]) {
                this.validateScanResult(review[reviewType], `${reviewPrefix}.${reviewType}`);
            }
        });
    }

    validateVulnerability(vuln, vulnPrefix) {
        const requiredFields = ['id', 'severity', 'description', 'discovery_date', 'patch_available'];
        
        requiredFields.forEach(field => {
            if (!vuln.hasOwnProperty(field)) {
                this.errors.push(`${vulnPrefix}: Missing required field '${field}'`);
            }
        });

        const validSeverities = ['critical', 'high', 'medium', 'low'];
        if (vuln.severity && !validSeverities.includes(vuln.severity)) {
            this.errors.push(`${vulnPrefix}: Invalid severity '${vuln.severity}' (must be one of: ${validSeverities.join(', ')})`);
        }

        if (vuln.discovery_date && !this.isValidDate(vuln.discovery_date)) {
            this.errors.push(`${vulnPrefix}: Invalid discovery_date format '${vuln.discovery_date}'`);
        }

        if (vuln.patch_available !== undefined && typeof vuln.patch_available !== 'boolean') {
            this.errors.push(`${vulnPrefix}: 'patch_available' must be a boolean`);
        }

        if (vuln.references && !Array.isArray(vuln.references)) {
            this.errors.push(`${vulnPrefix}: 'references' must be an array`);
        } else if (vuln.references) {
            vuln.references.forEach((ref, refIndex) => {
                if (!this.isValidURL(ref)) {
                    this.errors.push(`${vulnPrefix} reference ${refIndex}: Invalid URL '${ref}'`);
                }
            });
        }
    }

    checkForDuplicates(servers) {
        const slugs = new Set();
        const names = new Set();

        servers.forEach((server, index) => {
            if (server.slug) {
                if (slugs.has(server.slug)) {
                    this.errors.push(`Duplicate slug '${server.slug}' found in server ${index}`);
                } else {
                    slugs.add(server.slug);
                }
            }

            if (server.name) {
                if (names.has(server.name.toLowerCase())) {
                    this.warnings.push(`Potential duplicate name '${server.name}' found in server ${index}`);
                } else {
                    names.add(server.name.toLowerCase());
                }
            }
        });
    }

    isValidURL(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }

    isValidEmail(string) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(string);
    }

    isValidDate(dateString) {
        // Check YYYY-MM-DD format
        const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
        if (!dateRegex.test(dateString)) {
            return false;
        }
        
        const date = new Date(dateString);
        return date instanceof Date && !isNaN(date) && dateString === date.toISOString().split('T')[0];
    }

    isValidISODate(dateString) {
        try {
            const date = new Date(dateString);
            if (!(date instanceof Date) || isNaN(date)) {
                return false;
            }
            
            // Check if it's a valid ISO format (allowing both Z and timezone offsets)
            const isoRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?([+-]\d{2}:\d{2}|Z)$/;
            return isoRegex.test(dateString);
        } catch (_) {
            return false;
        }
    }

    printResults() {
        console.log('\n📊 Validation Results:');
        console.log('======================');
        
        if (this.errors.length === 0 && this.warnings.length === 0) {
            console.log('✅ All validation checks passed!');
            return;
        }

        if (this.errors.length > 0) {
            console.log(`\n❌ Errors (${this.errors.length}):`);
            this.errors.forEach((error, index) => {
                console.log(`${index + 1}. ${error}`);
            });
        }

        if (this.warnings.length > 0) {
            console.log(`\n⚠️  Warnings (${this.warnings.length}):`);
            this.warnings.forEach((warning, index) => {
                console.log(`${index + 1}. ${warning}`);
            });
        }

        console.log(`\nSummary: ${this.errors.length} errors, ${this.warnings.length} warnings`);
    }
}

function main() {
    const serversFile = path.join(process.cwd(), 'data', 'servers.json');
    
    if (!fs.existsSync(serversFile)) {
        console.error(`❌ File not found: ${serversFile}`);
        process.exit(1);
    }

    let data;
    try {
        const fileContent = fs.readFileSync(serversFile, 'utf8');
        data = JSON.parse(fileContent);
    } catch (error) {
        console.error(`❌ Failed to parse JSON file: ${error.message}`);
        process.exit(1);
    }

    const validator = new DataValidator();
    const isValid = validator.validateServersData(data);

    if (!isValid) {
        console.log('\n❌ Validation failed. Please fix the errors above.');
        process.exit(1);
    } else {
        console.log('\n✅ Validation completed successfully!');
        process.exit(0);
    }
}

if (require.main === module) {
    main();
}

module.exports = { DataValidator };