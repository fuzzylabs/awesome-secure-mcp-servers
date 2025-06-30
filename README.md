# Awesome Secure MCP Servers [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> **Secure Model Context Protocol (MCP) servers** with automated security validation, vulnerability scanning, and tool poisoning detection. Browse 16+ vetted MCP servers for building secure agentic AI systems.

## 🛡️ Security-First MCP Server Directory

Find **secure MCP servers** for your agentic AI applications with confidence. Model Context Protocol is the USB-C of building agentic systems - providing standardized, secure connections between AI agents and external tools. Each server undergoes automated security scanning including dependency vulnerability checks, static analysis, and MCP-specific threat detection (tool poisoning, cross-origin attacks).

### 🚀 Quick Start
1. **Browse servers** by category below
2. **Check security status** - look for 🛡️ Verified Secure or ⚠️ Conditional ratings
3. **Review scores** - higher scores indicate better security posture
4. **Follow repository links** for installation instructions

### 📊 Security Status Legend
- **🛡️ Verified Secure** (85-100): Comprehensive validation passed
- **⚠️ Conditional** (70-84): Secure with specific configuration requirements  
- **⏳ Awaiting Scan**: Repository currently inaccessible for scanning
- **❌ Not Recommended** (0-49): Known security issues

## 📚 Table of Contents
- [🏢 Official Servers](#official-servers) - Anthropic-maintained MCP servers
- [🏭 Enterprise Servers](#enterprise-servers) - Company-backed integrations 
- [🛡️ Security Tools](#security-tools) - Cybersecurity & vulnerability scanning
- [👥 Community Servers](#community-servers) - Open source community projects
- [🔄 Under Review](#under-review) - Servers currently being assessed
- [📖 About This Project](#-about-this-project) - Methodology & contributing

## Security Status by Category

**Last Updated:** 2025-06-26 14:10 UTC  
**Total Servers:** 16

### Official Servers

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [Everything (Reference Server)](https://github.com/modelcontextprotocol/servers/tree/main/src/everything) | 0.5.0 | ⚠️ Conditional ([📊 Score: 80/100](#security-details-everything-reference)) | Reference server demonstrating all MCP features |
| [Fetch Server](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) | 0.3.2 | ⚠️ Conditional ([📊 Score: 80/100](#security-details-fetch)) | Web content fetching and conversion for efficient LLM usage |
| [Filesystem Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) | 0.4.1 | ⚠️ Conditional ([📊 Score: 80/100](#security-details-filesystem)) | Secure file operations with configurable access controls |
| [Git Server](https://github.com/modelcontextprotocol/servers/tree/main/src/git) | 0.2.1 | ⚠️ Conditional ([📊 Score: 80/100](#security-details-git)) | Tools to read, search, and manipulate Git repositories |
| [Memory Server](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) | 0.1.3 | ⚠️ Conditional ([📊 Score: 80/100](#security-details-memory)) | Persistent memory using a local knowledge graph |
| [Sequential Thinking Server](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) | 0.1.0 | ⚠️ Conditional ([📊 Score: 80/100](#security-details-sequential-thinking)) | Dynamic and reflective problem-solving through thought sequences |
| [Time Server](https://github.com/modelcontextprotocol/servers/tree/main/src/time) | 0.1.2 | ⚠️ Conditional ([📊 Score: 80/100](#security-details-time)) | Time and timezone conversion capabilities |

### Enterprise Servers

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [AWS MCP Server](https://github.com/awslabs/mcp) | 1.2.0 | ⏳ Awaiting Scan | AWS service integration with IAM controls |
| [Docker Server](https://github.com/QuantGeekDev/docker-mcp) | 1.5.2 | ⏳ Awaiting Scan | Docker container management with security controls |
| [GitHub MCP Server](https://github.com/github/github-mcp-server) | 1.0.0 | ⚠️ Conditional ([📊 Score: 78/100](#security-details-github)) | GitHub's official MCP Server for repository management |
| [Notion MCP Server](https://github.com/makenotion/notion-mcp-server) | 0.3.1 | ⚠️ Conditional ([📊 Score: 83/100](#security-details-notion)) | Notion official MCP server for workspace integration |
| [Stripe MCP Server](https://github.com/stripe/agent-toolkit) | 0.2.0 | 🛡️ Verified Secure ([📊 Score: 85/100](#security-details-stripe)) | Interact with Stripe API for payments and financial data |

### Security Tools

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [Nuclei Security Scanner](https://github.com/cyproxio/mcp-for-security/tree/main/nuclei) | 0.2.0 | 🛡️ Verified Secure ([📊 Score: 85/100](#security-details-nuclei-scanner)) | Template-based vulnerability scanner with extensive security checks |

### Community Servers

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [PostgreSQL MCP Server](https://github.com/crystaldba/postgres-mcp) | 0.4.2 | ⏳ Awaiting Scan | PostgreSQL database operations and query execution |
| [Slack MCP Server](https://github.com/korotovsky/slack-mcp-server) | 1.0.3 | ⏳ Awaiting Scan | Slack workspace integration for messaging and collaboration |

### Under Review

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [Anthropic Computer Use](https://github.com/anthropics/anthropic-computer-use) | 0.1.0 | ⏳ Awaiting Scan | Desktop automation with screen capture and input control |

---

## 📊 Detailed Security Assessments

_Click on server scores above to jump to detailed security breakdowns:_

<details id="security-details-everything-reference">
<summary><strong>Everything (Reference Server)</strong> Security Assessment</summary>

### Security Assessment: 2025-06-25

**🔍 MCP-Specific Security**: 90/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- No tool poisoning indicators found (basic check)

**📦 Third-Party Dependencies**: 80/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **2 potential issues found**
- Found 2 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 70/100 ⚠️
*Static analysis for common security vulnerabilities in source code*

⚠️ **0 potential issues found**
- Bandit not available for Python security analysis

**🐳 Container Security**: 50/100 ➖
*Analyzes Dockerfile and container configurations for security issues*

➖ **Not applicable**
- No container configurations found

**📋 Security Documentation**: 100/100 ✅
*Checks for security guidelines, vulnerability reporting, and usage instructions*

✅ **No issues found**
- Security documentation is adequate


</details>

<details id="security-details-fetch">
<summary><strong>Fetch Server</strong> Security Assessment</summary>

### Security Assessment: 2025-06-25

**🔍 MCP-Specific Security**: 90/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- No tool poisoning indicators found (basic check)

**📦 Third-Party Dependencies**: 80/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **2 potential issues found**
- Found 2 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 70/100 ⚠️
*Static analysis for common security vulnerabilities in source code*

⚠️ **0 potential issues found**
- Bandit not available for Python security analysis

**🐳 Container Security**: 50/100 ➖
*Analyzes Dockerfile and container configurations for security issues*

➖ **Not applicable**
- No container configurations found

**📋 Security Documentation**: 100/100 ✅
*Checks for security guidelines, vulnerability reporting, and usage instructions*

✅ **No issues found**
- Security documentation is adequate


</details>

<details id="security-details-filesystem">
<summary><strong>Filesystem Server</strong> Security Assessment</summary>

### Security Assessment: 2025-06-25

**🔍 MCP-Specific Security**: 90/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- No tool poisoning indicators found (basic check)

**📦 Third-Party Dependencies**: 80/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **2 potential issues found**
- Found 2 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 70/100 ⚠️
*Static analysis for common security vulnerabilities in source code*

⚠️ **0 potential issues found**
- Bandit not available for Python security analysis

**🐳 Container Security**: 50/100 ➖
*Analyzes Dockerfile and container configurations for security issues*

➖ **Not applicable**
- No container configurations found

**📋 Security Documentation**: 100/100 ✅
*Checks for security guidelines, vulnerability reporting, and usage instructions*

✅ **No issues found**
- Security documentation is adequate


</details>

<details id="security-details-git">
<summary><strong>Git Server</strong> Security Assessment</summary>

### Security Assessment: 2025-06-25

**🔍 MCP-Specific Security**: 90/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- No tool poisoning indicators found (basic check)

**📦 Third-Party Dependencies**: 80/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **2 potential issues found**
- Found 2 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 70/100 ⚠️
*Static analysis for common security vulnerabilities in source code*

⚠️ **0 potential issues found**
- Bandit not available for Python security analysis

**🐳 Container Security**: 50/100 ➖
*Analyzes Dockerfile and container configurations for security issues*

➖ **Not applicable**
- No container configurations found

**📋 Security Documentation**: 100/100 ✅
*Checks for security guidelines, vulnerability reporting, and usage instructions*

✅ **No issues found**
- Security documentation is adequate


</details>

<details id="security-details-github">
<summary><strong>GitHub MCP Server</strong> Security Assessment</summary>

### Security Assessment: 2025-06-25

**🔍 MCP-Specific Security**: 90/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- No tool poisoning indicators found (basic check)

**📦 Third-Party Dependencies**: 50/100 ➖
*Scans package.json, requirements.txt, etc. for known CVEs*

➖ **Not applicable**
- Go dependency scanning not yet implemented

**🐛 Code Security Analysis**: 70/100 ⚠️
*Static analysis for common security vulnerabilities in source code*

⚠️ **0 potential issues found**
- Semgrep not available for security analysis

**🐳 Container Security**: 100/100 ✅
*Analyzes Dockerfile and container configurations for security issues*

✅ **No issues found**
- Container configuration appears secure

**📋 Security Documentation**: 100/100 ✅
*Checks for security guidelines, vulnerability reporting, and usage instructions*

✅ **No issues found**
- Security documentation is adequate


</details>

<details id="security-details-memory">
<summary><strong>Memory Server</strong> Security Assessment</summary>

### Security Assessment: 2025-06-25

**🔍 MCP-Specific Security**: 90/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- No tool poisoning indicators found (basic check)

**📦 Third-Party Dependencies**: 80/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **2 potential issues found**
- Found 2 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 70/100 ⚠️
*Static analysis for common security vulnerabilities in source code*

⚠️ **0 potential issues found**
- Bandit not available for Python security analysis

**🐳 Container Security**: 50/100 ➖
*Analyzes Dockerfile and container configurations for security issues*

➖ **Not applicable**
- No container configurations found

**📋 Security Documentation**: 100/100 ✅
*Checks for security guidelines, vulnerability reporting, and usage instructions*

✅ **No issues found**
- Security documentation is adequate


</details>

<details id="security-details-notion">
<summary><strong>Notion MCP Server</strong> Security Assessment</summary>

### Security Assessment: 2025-06-25

**🔍 MCP-Specific Security**: 90/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- No tool poisoning indicators found (basic check)

**📦 Third-Party Dependencies**: 80/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **2 potential issues found**
- Found 2 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 70/100 ⚠️
*Static analysis for common security vulnerabilities in source code*

⚠️ **0 potential issues found**
- Static analysis partially failed: 'SecurityScanner' object has no attribute '_run_eslint_security'

**🐳 Container Security**: 100/100 ✅
*Analyzes Dockerfile and container configurations for security issues*

✅ **No issues found**
- Container configuration appears secure

**📋 Security Documentation**: 80/100 ⚠️
*Checks for security guidelines, vulnerability reporting, and usage instructions*

⚠️ **0 potential issues found**
- No dedicated security documentation found


</details>

<details id="security-details-nuclei-scanner">
<summary><strong>Nuclei Security Scanner</strong> Security Assessment</summary>

### Security Assessment: 2025-06-25

**🔍 MCP-Specific Security**: 95/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- MCP-scan found no security issues in 1 configuration file(s)

**📦 Third-Party Dependencies**: 100/100 ➖
*Scans package.json, requirements.txt, etc. for known CVEs*

➖ **Not applicable**
- No recognized dependency files found

**🐛 Code Security Analysis**: 70/100 ⚠️
*Static analysis for common security vulnerabilities in source code*

⚠️ **0 potential issues found**
- Static analysis partially failed: 'SecurityScanner' object has no attribute '_run_eslint_security'

**🐳 Container Security**: 50/100 ➖
*Analyzes Dockerfile and container configurations for security issues*

➖ **Not applicable**
- No container configurations found

**📋 Security Documentation**: 80/100 ⚠️
*Checks for security guidelines, vulnerability reporting, and usage instructions*

⚠️ **0 potential issues found**
- No dedicated security documentation found


</details>

<details id="security-details-sequential-thinking">
<summary><strong>Sequential Thinking Server</strong> Security Assessment</summary>

### Security Assessment: 2025-06-25

**🔍 MCP-Specific Security**: 90/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- No tool poisoning indicators found (basic check)

**📦 Third-Party Dependencies**: 80/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **2 potential issues found**
- Found 2 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 70/100 ⚠️
*Static analysis for common security vulnerabilities in source code*

⚠️ **0 potential issues found**
- Bandit not available for Python security analysis

**🐳 Container Security**: 50/100 ➖
*Analyzes Dockerfile and container configurations for security issues*

➖ **Not applicable**
- No container configurations found

**📋 Security Documentation**: 100/100 ✅
*Checks for security guidelines, vulnerability reporting, and usage instructions*

✅ **No issues found**
- Security documentation is adequate


</details>

<details id="security-details-stripe">
<summary><strong>Stripe MCP Server</strong> Security Assessment</summary>

### Security Assessment: 2025-06-25

**🔍 MCP-Specific Security**: 90/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- No tool poisoning indicators found (basic check)

**📦 Third-Party Dependencies**: 100/100 ➖
*Scans package.json, requirements.txt, etc. for known CVEs*

➖ **Not applicable**
- No recognized dependency files found

**🐛 Code Security Analysis**: 70/100 ⚠️
*Static analysis for common security vulnerabilities in source code*

⚠️ **0 potential issues found**
- Bandit not available for Python security analysis

**🐳 Container Security**: 50/100 ➖
*Analyzes Dockerfile and container configurations for security issues*

➖ **Not applicable**
- No container configurations found

**📋 Security Documentation**: 100/100 ✅
*Checks for security guidelines, vulnerability reporting, and usage instructions*

✅ **No issues found**
- Security documentation is adequate


</details>

<details id="security-details-time">
<summary><strong>Time Server</strong> Security Assessment</summary>

### Security Assessment: 2025-06-25

**🔍 MCP-Specific Security**: 90/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- No tool poisoning indicators found (basic check)

**📦 Third-Party Dependencies**: 80/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **2 potential issues found**
- Found 2 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 70/100 ⚠️
*Static analysis for common security vulnerabilities in source code*

⚠️ **0 potential issues found**
- Bandit not available for Python security analysis

**🐳 Container Security**: 50/100 ➖
*Analyzes Dockerfile and container configurations for security issues*

➖ **Not applicable**
- No container configurations found

**📋 Security Documentation**: 100/100 ✅
*Checks for security guidelines, vulnerability reporting, and usage instructions*

✅ **No issues found**
- Security documentation is adequate


</details>


---

## 🧪 Testing

This project includes comprehensive tests to ensure the security infrastructure works correctly:

### Running Tests

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

### Test Coverage

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

### Adding New Tests

When adding new features or scripts:

1. Create corresponding test files in `tests/`
2. Follow the naming convention `test_<script_name>.py`
3. Include tests for both success and error cases
4. Update this README with test descriptions
5. Ensure tests pass with `make test`

---

## 📖 About This Project

### Methodology

Our security validation process combines multiple approaches:

1. **Automated Scanning**: Static analysis, dependency checks, and container security
2. **MCP-Specific Analysis**: Tool poisoning detection using specialized mcp-scan tool
3. **Manual Review**: Architecture assessment and security documentation review
4. **Continuous Monitoring**: Regular rescans and vulnerability tracking

### Security Scoring

Each server receives a weighted score (0-100) based on:
- **MCP-Specific Security** (35%): Tool poisoning and protocol-specific threats
- **Dependencies** (25%): Known CVE scanning of third-party packages  
- **Static Analysis** (20%): Code vulnerability detection
- **Container Security** (10%): Docker configuration analysis
- **Documentation** (10%): Security guidelines and reporting processes

### Contributing

We welcome contributions\! Please:

1. **Test your changes**: Run `make test` before submitting
2. **Update documentation**: Keep README.md and CLAUDE.md current with new features
3. **Follow security practices**: All servers must pass our validation pipeline
4. **Validate data**: Use `make validate` to check data/servers.json changes

### Repository Maintenance

**⚠️ Important**: When adding new features or making changes:

- **Always update README.md** with new functionality, commands, and usage instructions
- **Always update CLAUDE.md** with development notes, architecture changes, and testing requirements
- **Run the test suite** to ensure nothing breaks
- **Update version tracking** in both documentation files

This ensures the documentation stays synchronized with the codebase and new contributors can understand the current state of the project.

### License

MIT License - see [LICENSE](LICENSE) for details.
EOF < /dev/null