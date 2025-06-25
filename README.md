# Awesome Secure MCP Servers [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> **Secure Model Context Protocol (MCP) servers** with automated security validation, vulnerability scanning, and tool poisoning detection. Browse 16+ vetted MCP servers for Claude AI, ChatGPT, and other AI applications with confidence.

**Keywords**: MCP servers, Model Context Protocol, Claude AI, ChatGPT integration, secure AI tools, vulnerability scanning, tool poisoning detection, AI security, LLM integrations

## 🛡️ Security-First MCP Server Directory

Find **secure MCP servers** for your AI applications with confidence. Each server undergoes automated security scanning including dependency vulnerability checks, static analysis, and MCP-specific threat detection (tool poisoning, cross-origin attacks).

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

**Last Updated:** 2025-06-25 15:39 UTC  
**Total Servers:** 16

### Official Servers

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [Everything (Reference Server)](https://github.com/modelcontextprotocol/servers/tree/main/src/everything) | 0.5.0 | ⚠️ Conditional (Score: 80/100) | Reference server demonstrating all MCP features |
| [Fetch Server](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) | 0.3.2 | ⚠️ Conditional (Score: 80/100) | Web content fetching and conversion for efficient LLM usage |
| [Filesystem Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) | 0.4.1 | ⚠️ Conditional (Score: 80/100) | Secure file operations with configurable access controls |
| [Git Server](https://github.com/modelcontextprotocol/servers/tree/main/src/git) | 0.2.1 | ⚠️ Conditional (Score: 80/100) | Tools to read, search, and manipulate Git repositories |
| [Memory Server](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) | 0.1.3 | ⚠️ Conditional (Score: 80/100) | Persistent memory using a local knowledge graph |
| [Sequential Thinking Server](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) | 0.1.0 | ⚠️ Conditional (Score: 80/100) | Dynamic and reflective problem-solving through thought sequences |
| [Time Server](https://github.com/modelcontextprotocol/servers/tree/main/src/time) | 0.1.2 | ⚠️ Conditional (Score: 80/100) | Time and timezone conversion capabilities |

### Enterprise Servers

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [AWS MCP Server](https://github.com/awslabs/mcp) | 1.2.0 | ⏳ Awaiting Scan | AWS service integration with IAM controls |
| [Docker Server](https://github.com/QuantGeekDev/docker-mcp) | 1.5.2 | ⏳ Awaiting Scan | Docker container management with security controls |
| [GitHub MCP Server](https://github.com/github/github-mcp-server) | 1.0.0 | ⚠️ Conditional (Score: 78/100) | GitHub's official MCP Server for repository management |
| [Notion MCP Server](https://github.com/makenotion/notion-mcp-server) | 0.3.1 | ⚠️ Conditional (Score: 83/100) | Notion official MCP server for workspace integration |
| [Stripe MCP Server](https://github.com/stripe/agent-toolkit) | 0.2.0 | 🛡️ Verified Secure (Score: 85/100) | Interact with Stripe API for payments and financial data |

### Security Tools

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [Nuclei Security Scanner](https://github.com/cyproxio/mcp-for-security/tree/main/nuclei) | 0.2.0 | 🛡️ Verified Secure (Score: 85/100) | Template-based vulnerability scanner with extensive security checks |

### Community Servers

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [PostgreSQL MCP Server](https://github.com/crystaldba/postgres-mcp) | 0.4.2 | ⏳ Awaiting Scan | PostgreSQL database operations and query execution |
| [Slack MCP Server](https://github.com/korotovsky/slack-mcp-server) | 1.0.3 | ⏳ Awaiting Scan | Slack workspace integration for messaging and collaboration |

### Under Review

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [Anthropic Computer Use](https://github.com/anthropics/anthropic-computer-use) | 0.1.0 | ⏳ Awaiting Scan | Desktop automation with screen capture and input control |
