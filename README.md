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

**Last Updated:** 2026-03-09 06:17 UTC  
**Total Servers:** 16

### Official Servers

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [Everything (Reference Server)](https://github.com/modelcontextprotocol/servers/tree/main/src/everything) | 0.5.0 | 🛡️ Verified Secure ([📊 Score: 87/100](#security-details-everything-reference)) | Reference server demonstrating all MCP features |
| [Fetch Server](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) | 0.3.2 | 🛡️ Verified Secure ([📊 Score: 87/100](#security-details-fetch)) | Web content fetching and conversion for efficient LLM usage |
| [Filesystem Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) | 0.4.1 | 🛡️ Verified Secure ([📊 Score: 87/100](#security-details-filesystem)) | Secure file operations with configurable access controls |
| [Git Server](https://github.com/modelcontextprotocol/servers/tree/main/src/git) | 0.2.1 | 🛡️ Verified Secure ([📊 Score: 87/100](#security-details-git)) | Tools to read, search, and manipulate Git repositories |
| [Memory Server](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) | 0.1.3 | 🛡️ Verified Secure ([📊 Score: 87/100](#security-details-memory)) | Persistent memory using a local knowledge graph |
| [Sequential Thinking Server](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) | 0.1.0 | 🛡️ Verified Secure ([📊 Score: 87/100](#security-details-sequential-thinking)) | Dynamic and reflective problem-solving through thought sequences |
| [Time Server](https://github.com/modelcontextprotocol/servers/tree/main/src/time) | 0.1.2 | 🛡️ Verified Secure ([📊 Score: 87/100](#security-details-time)) | Time and timezone conversion capabilities |

### Enterprise Servers

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [AWS MCP Server](https://github.com/awslabs/mcp) | 1.2.0 | 🛡️ Verified Secure ([📊 Score: 92/100](#security-details-aws)) | AWS service integration with IAM controls |
| [Docker Server](https://github.com/QuantGeekDev/docker-mcp) | 1.5.2 | 🛡️ Verified Secure ([📊 Score: 91/100](#security-details-docker-server)) | Docker container management with security controls |
| [GitHub MCP Server](https://github.com/github/github-mcp-server) | 1.0.0 | ⚠️ Conditional ([📊 Score: 80/100](#security-details-github)) | GitHub's official MCP Server for repository management |
| [Notion MCP Server](https://github.com/makenotion/notion-mcp-server) | 0.3.1 | ⚠️ Conditional ([📊 Score: 79/100](#security-details-notion)) | Notion official MCP server for workspace integration |
| [Stripe MCP Server](https://github.com/stripe/agent-toolkit) | 0.2.0 | 🛡️ Verified Secure ([📊 Score: 89/100](#security-details-stripe)) | Interact with Stripe API for payments and financial data |

### Security Tools

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [Nuclei Security Scanner](https://github.com/cyproxio/mcp-for-security/tree/main/nuclei) | 0.2.0 | 🛡️ Verified Secure ([📊 Score: 92/100](#security-details-nuclei-scanner)) | Template-based vulnerability scanner with extensive security checks |

### Community Servers

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [PostgreSQL MCP Server](https://github.com/crystaldba/postgres-mcp) | 0.4.2 | 🛡️ Verified Secure ([📊 Score: 86/100](#security-details-postgresql)) | PostgreSQL database operations and query execution |
| [Slack MCP Server](https://github.com/korotovsky/slack-mcp-server) | 1.0.3 | ⚠️ Conditional ([📊 Score: 77/100](#security-details-slack)) | Slack workspace integration for messaging and collaboration |

### Under Review

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [Anthropic Computer Use](https://github.com/anthropics/anthropic-computer-use) | 0.1.0 | ⏳ Awaiting Scan | Desktop automation with screen capture and input control |

---

## 📊 Detailed Security Assessments

_Click on server scores above to jump to detailed security breakdowns:_

<details id="security-details-aws">
<summary><strong>AWS MCP Server</strong> Security Assessment</summary>

### Security Assessment: 2026-03-09

**🔍 MCP-Specific Security**: 95/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- MCP-scan found no security issues in 5 configuration file(s)

**📦 Third-Party Dependencies**: 100/100 ➖
*Scans package.json, requirements.txt, etc. for known CVEs*

➖ **Not applicable**
- No recognized dependency files found

**🐛 Code Security Analysis**: 70/100 ⚠️
*Static analysis for common security vulnerabilities in source code*

⚠️ **0 potential issues found**
- Bandit completed but output could not be parsed


</details>

<details id="security-details-docker-server">
<summary><strong>Docker Server</strong> Security Assessment</summary>

### Security Assessment: 2026-03-09

**🔍 MCP-Specific Security**: 90/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- No tool poisoning indicators found (basic check)

**📦 Third-Party Dependencies**: 100/100 ➖
*Scans package.json, requirements.txt, etc. for known CVEs*

➖ **Not applicable**
- No recognized dependency files found

**🐛 Code Security Analysis**: 85/100 ⚠️
*Static analysis for common security vulnerabilities in source code*

⚠️ **1 potential issues found**
- Found 1 critical security issue(s)


</details>

<details id="security-details-everything-reference">
<summary><strong>Everything (Reference Server)</strong> Security Assessment</summary>

### Security Assessment: 2026-03-09

**🔍 MCP-Specific Security**: 95/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- MCP-scan found no security issues in 1 configuration file(s)

**📦 Third-Party Dependencies**: 60/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **26 potential issues found**
- Found 26 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 100/100 ✅
*Static analysis for common security vulnerabilities in source code*

✅ **No issues found**
- No critical security vulnerabilities found


</details>

<details id="security-details-fetch">
<summary><strong>Fetch Server</strong> Security Assessment</summary>

### Security Assessment: 2026-03-09

**🔍 MCP-Specific Security**: 95/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- MCP-scan found no security issues in 1 configuration file(s)

**📦 Third-Party Dependencies**: 60/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **26 potential issues found**
- Found 26 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 100/100 ✅
*Static analysis for common security vulnerabilities in source code*

✅ **No issues found**
- No critical security vulnerabilities found


</details>

<details id="security-details-filesystem">
<summary><strong>Filesystem Server</strong> Security Assessment</summary>

### Security Assessment: 2026-03-09

**🔍 MCP-Specific Security**: 95/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- MCP-scan found no security issues in 1 configuration file(s)

**📦 Third-Party Dependencies**: 60/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **26 potential issues found**
- Found 26 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 100/100 ✅
*Static analysis for common security vulnerabilities in source code*

✅ **No issues found**
- No critical security vulnerabilities found


</details>

<details id="security-details-git">
<summary><strong>Git Server</strong> Security Assessment</summary>

### Security Assessment: 2026-03-09

**🔍 MCP-Specific Security**: 95/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- MCP-scan found no security issues in 1 configuration file(s)

**📦 Third-Party Dependencies**: 60/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **26 potential issues found**
- Found 26 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 100/100 ✅
*Static analysis for common security vulnerabilities in source code*

✅ **No issues found**
- No critical security vulnerabilities found


</details>

<details id="security-details-github">
<summary><strong>GitHub MCP Server</strong> Security Assessment</summary>

### Security Assessment: 2026-03-09

**🔍 MCP-Specific Security**: 95/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- MCP-scan found no security issues in 1 configuration file(s)

**📦 Third-Party Dependencies**: 50/100 ➖
*Scans package.json, requirements.txt, etc. for known CVEs*

➖ **Not applicable**
- Go dependency scanning not yet implemented

**🐛 Code Security Analysis**: 70/100 ➖
*Static analysis for common security vulnerabilities in source code*

➖ **Not applicable**
- ESLint security scanning not available


</details>

<details id="security-details-memory">
<summary><strong>Memory Server</strong> Security Assessment</summary>

### Security Assessment: 2026-03-09

**🔍 MCP-Specific Security**: 95/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- MCP-scan found no security issues in 1 configuration file(s)

**📦 Third-Party Dependencies**: 60/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **26 potential issues found**
- Found 26 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 100/100 ✅
*Static analysis for common security vulnerabilities in source code*

✅ **No issues found**
- No critical security vulnerabilities found


</details>

<details id="security-details-notion">
<summary><strong>Notion MCP Server</strong> Security Assessment</summary>

### Security Assessment: 2026-03-09

**🔍 MCP-Specific Security**: 90/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- No tool poisoning indicators found (basic check)

**📦 Third-Party Dependencies**: 60/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **2 potential issues found**
- Found 2 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 70/100 ➖
*Static analysis for common security vulnerabilities in source code*

➖ **Not applicable**
- ESLint security scanning not available


</details>

<details id="security-details-nuclei-scanner">
<summary><strong>Nuclei Security Scanner</strong> Security Assessment</summary>

### Security Assessment: 2026-03-09

**🔍 MCP-Specific Security**: 95/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- MCP-scan found no security issues in 1 configuration file(s)

**📦 Third-Party Dependencies**: 100/100 ➖
*Scans package.json, requirements.txt, etc. for known CVEs*

➖ **Not applicable**
- No recognized dependency files found

**🐛 Code Security Analysis**: 70/100 ➖
*Static analysis for common security vulnerabilities in source code*

➖ **Not applicable**
- ESLint security scanning not available


</details>

<details id="security-details-postgresql">
<summary><strong>PostgreSQL MCP Server</strong> Security Assessment</summary>

### Security Assessment: 2026-03-09

**🔍 MCP-Specific Security**: 90/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- No tool poisoning indicators found (basic check)

**📦 Third-Party Dependencies**: 100/100 ➖
*Scans package.json, requirements.txt, etc. for known CVEs*

➖ **Not applicable**
- No recognized dependency files found

**🐛 Code Security Analysis**: 50/100 ❌
*Static analysis for common security vulnerabilities in source code*

❌ **11 critical issues found**
- Found 11 critical security issue(s)


</details>

<details id="security-details-sequential-thinking">
<summary><strong>Sequential Thinking Server</strong> Security Assessment</summary>

### Security Assessment: 2026-03-09

**🔍 MCP-Specific Security**: 95/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- MCP-scan found no security issues in 1 configuration file(s)

**📦 Third-Party Dependencies**: 60/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **26 potential issues found**
- Found 26 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 100/100 ✅
*Static analysis for common security vulnerabilities in source code*

✅ **No issues found**
- No critical security vulnerabilities found


</details>

<details id="security-details-slack">
<summary><strong>Slack MCP Server</strong> Security Assessment</summary>

### Security Assessment: 2026-03-09

**🔍 MCP-Specific Security**: 90/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- No tool poisoning indicators found (basic check)

**📦 Third-Party Dependencies**: 50/100 ➖
*Scans package.json, requirements.txt, etc. for known CVEs*

➖ **Not applicable**
- Go dependency scanning not yet implemented

**🐛 Code Security Analysis**: 70/100 ➖
*Static analysis for common security vulnerabilities in source code*

➖ **Not applicable**
- ESLint security scanning not available


</details>

<details id="security-details-stripe">
<summary><strong>Stripe MCP Server</strong> Security Assessment</summary>

### Security Assessment: 2026-03-09

**🔍 MCP-Specific Security**: 95/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- MCP-scan found no security issues in 3 configuration file(s)

**📦 Third-Party Dependencies**: 100/100 ➖
*Scans package.json, requirements.txt, etc. for known CVEs*

➖ **Not applicable**
- No recognized dependency files found

**🐛 Code Security Analysis**: 50/100 ❌
*Static analysis for common security vulnerabilities in source code*

❌ **5 critical issues found**
- Found 5 critical security issue(s)


</details>

<details id="security-details-time">
<summary><strong>Time Server</strong> Security Assessment</summary>

### Security Assessment: 2026-03-09

**🔍 MCP-Specific Security**: 95/100 ✅
*Scans for MCP-specific threats like tool poisoning attacks*

✅ **No issues found**
- MCP-scan found no security issues in 1 configuration file(s)

**📦 Third-Party Dependencies**: 60/100 ⚠️
*Scans package.json, requirements.txt, etc. for known CVEs*

⚠️ **26 potential issues found**
- Found 26 vulnerability/vulnerabilities in dependencies

**🐛 Code Security Analysis**: 100/100 ✅
*Static analysis for common security vulnerabilities in source code*

✅ **No issues found**
- No critical security vulnerabilities found


</details>








































