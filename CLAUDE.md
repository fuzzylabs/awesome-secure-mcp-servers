# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a security-focused awesome list that curates Model Context Protocol (MCP) servers with comprehensive security validation. Unlike typical awesome lists, this repository performs active security scanning and maintains version-specific security assessments for each listed MCP server.

## Core Architecture

### Data-Driven Approach
The repository centers around `data/servers.json`, which contains structured security data for each MCP server. This file follows a strict JSON schema (`data/schema.json`) that tracks:
- Server metadata and categorization
- Version-specific security status and scores
- Detailed security scan results
- Vulnerability tracking
- Manual security review data

### Security Validation Pipeline
The security validation system consists of three main components:

1. **Automated Security Scanner** (`scripts/security-scanner.py`): Downloads and analyzes MCP server repositories, performing static analysis, dependency scanning, tool poisoning detection, and container security checks
2. **Manual Review Process**: Structured security assessments documented in the security scan data
3. **Continuous Monitoring**: GitHub Actions workflows that monitor for new versions and security vulnerabilities

### Security Status Scoring
Each server version receives a weighted security score (0-100) based on:
- Static Analysis (25%)
- Dependency Scan (25%) 
- Tool Poisoning Check (30%) - MCP-specific security concern
- Container Security (10%)
- Security Documentation (10%)

Scores map to security statuses: Verified Secure (🛡️ 85-100), Conditional (⚠️ 70-84), Under Review (🔄 50-69), Not Recommended (❌ 0-49).

## Common Commands

```bash
# Validate data integrity and schema compliance
npm run validate

# Run comprehensive security scanning
npm run security-scan

# Generate human-readable security reports
npm run generate-report

# Run all tests (currently just validation)
npm test

# Lint JavaScript code
npm run lint

# Set up development environment
./setup.sh
```

### Manual Security Scanning
```bash
# Scan specific server by slug
python scripts/security-scanner.py --input data/servers.json --output security/scan-results.json --server-slug filesystem

# Generate report from existing scan results
python scripts/generate-report.py --scan-results security/scan-results.json --output security/security-report.md
```

## Data Management

### Adding New Servers
When adding new MCP servers to `data/servers.json`:
1. Follow the JSON schema structure exactly
2. Set initial security_status to "under-review"
3. Include all required fields: name, slug, repository, category, description, versions
4. Use semantic versioning for version numbers
5. Include MCP protocol version compatibility

### Version Updates
New versions trigger the security validation pipeline:
1. Automated detection via GitHub Actions (`version-monitor.yml`)
2. Security scanning of the new version
3. Status updates based on scan results
4. README.md badge updates

### Security Categories
- **official**: Anthropic/MCP team maintained servers
- **enterprise**: Company-maintained with security attestations  
- **community**: Community servers passing validation
- **security-tools**: Defensive security MCP servers
- **under-review**: Servers currently being validated
- **deprecated**: Servers with unresolved security issues

## GitHub Actions Workflows

### Security Validation Pipeline (`security-scan.yml`)
- Triggers on data changes, PRs, and weekly schedule
- Runs automated security scans
- Updates security badges in README.md
- Creates issues for vulnerabilities
- Comments scan results on PRs

### Version Monitoring (`version-monitor.yml`)
- Daily checks for new MCP server versions
- Creates PRs for new versions requiring validation
- Manages stale version alerts
- Cleans up old branches

## Tool Poisoning Detection

This repository includes specialized detection for MCP-specific "tool poisoning" attacks where malicious instructions are embedded in tool descriptions. The scanner checks for patterns like:
- "ignore previous instructions"
- Hidden Unicode characters
- Malicious comments or metadata
- Social engineering patterns

## Security Validation Requirements

When reviewing or adding servers, ensure they meet the security criteria defined in `security/README.md`. Manual security reviews must cover:
- Architecture security design
- Authentication mechanisms
- Authorization controls
- Security documentation completeness

## Development Notes

- Always run `npm run validate` before committing changes to `data/servers.json`
- Security scanner requires Python 3.8+ and various security tools (bandit, safety, semgrep)
- Node.js 16+ required for validation scripts
- The repository is designed to be defensive-security focused only - never add servers with offensive capabilities