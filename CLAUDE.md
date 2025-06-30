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
- MCP-Specific Security (35%) - Tool poisoning detection using mcp-scan from Invariant Labs
- Dependencies (25%) - Known CVE scanning of package.json, requirements.txt, etc.
- Static Analysis (20%) - Code vulnerability scanning (Bandit, ESLint, Semgrep)
- Container Security (10%) - Dockerfile and container configuration analysis
- Security Documentation (10%) - Presence of SECURITY.md and vulnerability reporting

Scores map to security statuses: Verified Secure (🛡️ 85-100), Conditional (⚠️ 70-84), Under Review (🔄 50-69), Not Recommended (❌ 0-49).

## Common Commands

### Testing Commands
```bash
# Run all basic functionality tests
make test
npm test

# Run validation-specific tests  
make test-validation
npm run test-validation

# Run complete test suite (requires proper imports)
npm run test-full
```

### Using Makefile (Recommended)
```bash
# Validate data integrity and schema compliance
make validate

# Run all pipeline steps
make all

# Update artifacts (data and README) with scan results
make update

# Generate security report
make report

# Clean generated files
make clean
```

### Legacy npm commands
```bash
# Validate data integrity and schema compliance
npm run validate

# Run comprehensive security scanning
npm run security-scan

# Generate human-readable security reports
npm run generate-report

# Lint JavaScript code
npm run lint

# Set up development environment
./setup.sh
```

### Manual Security Scanning
```bash
# Scan specific server by slug
python scripts/security-scanner.py --input data/servers.json --output security/scan-results.json --server-slug filesystem

# Update artifacts with scan results (replaces separate update scripts)
python scripts/update-artifacts.py --servers data/servers.json --scan-results security/scan-results.json --readme README.md

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

This repository includes specialized detection for MCP-specific "tool poisoning" attacks where malicious instructions are embedded in tool descriptions. The security pipeline uses:

1. **mcp-scan tool** (Invariant Labs): Specialized MCP security scanner that validates configuration files and detects protocol-specific vulnerabilities
2. **Pattern-based detection**: Checks for common attack patterns like:
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

## Testing Infrastructure

### Test Coverage

This project includes comprehensive tests to ensure the security infrastructure works correctly:

- **Data Validation Tests** (`tests/test_validate.py`)
  - Schema validation with actual project files
  - Duplicate detection (slugs, names)
  - Version format validation
  - Error handling for invalid data

- **Update Artifacts Tests** (`tests/test_update_artifacts.py`)
  - README generation without duplication
  - Security score calculations and mappings
  - Section boundary detection
  - Dry-run mode functionality
  - Security assessment formatting

- **Security Scanner Tests** (`tests/test_security_scanner.py`)
  - Score calculation and weighting
  - Tool integration (Bandit, Safety, mcp-scan)
  - Error handling for unavailable repositories
  - Docker security scanning
  - Tool poisoning detection

- **Basic Functionality Tests** (`test_runner.py`)
  - Core component functionality verification
  - Project data validation
  - Makefile command testing

### Testing Requirements

When adding new features or making changes:

1. **Create corresponding tests** for new scripts in `tests/` directory
2. **Follow naming conventions**: `test_<script_name>.py`
3. **Include both success and error cases** in test coverage
4. **Run test suite before committing**: `make test`
5. **Update test documentation** in both README.md and CLAUDE.md

### Test Execution

Tests use Python's unittest framework and can be run via:
- `make test` - Basic functionality tests
- `make test-validation` - Data validation tests specifically
- `npm run test-full` - Complete test suite (requires imports)

## Development Notes

- **Always run `make test`** before committing any changes
- Always run `make validate` (or `npm run validate`) before committing changes to `data/servers.json`
- Security scanner requires Python 3.8+ and various security tools (bandit, safety, semgrep, mcp-scan)
- Node.js 16+ required for validation scripts  
- Use `make all` to run the complete pipeline: validate → discover → process → scan → update → report
- The consolidated `scripts/update-artifacts.py` replaces separate update-security-data.py and update-readme.py scripts
- Security assessments include actionable recommendations and links to security details
- The repository is designed to be defensive-security focused only - never add servers with offensive capabilities

## Documentation Maintenance

**⚠️ Critical Requirement**: When adding new features or making changes to the codebase:

### Required Documentation Updates

1. **Always update README.md** with:
   - New functionality and commands
   - Usage instructions and examples
   - Test coverage information
   - Contributing guidelines

2. **Always update CLAUDE.md** with:
   - Development notes and architecture changes
   - Testing requirements and procedures
   - New script descriptions and usage
   - Infrastructure status updates

3. **Version tracking** in both documentation files:
   - Update Current Infrastructure Status section
   - Document script changes and consolidations
   - Note any breaking changes or deprecations

### Documentation Standards

- **Keep examples current**: Update command examples when scripts change
- **Maintain accuracy**: Ensure documentation reflects actual implementation
- **Include context**: Explain why changes were made, not just what changed
- **Test instructions**: Verify all documented commands actually work

This ensures the documentation stays synchronized with the codebase and new contributors can understand the current state of the project.

## Current Infrastructure Status

- **16 MCP servers** currently tracked with real security scan results
- **Automated scanning pipeline** running weekly via GitHub Actions
- **Script consolidation** completed with Makefile orchestration (PR #5)
- **Enhanced README** with clickable security scores and detailed assessments
- **"Awaiting Scan" status** for repositories that are currently inaccessible
- **mcp-scan integration** for MCP-specific threat detection
- **Comprehensive testing infrastructure** with unit tests for all major scripts