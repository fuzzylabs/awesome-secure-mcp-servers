# Awesome Secure MCP Servers [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A community-driven, transparent list of security-assessed Model Context Protocol (MCP) servers

## 🎯 Our Mission

We believe the MCP ecosystem needs trustworthy security information. This project provides **transparent, reproducible security assessments** of MCP servers to help developers make informed decisions.

## 🔍 Complete Transparency

**Everything is open and auditable:**
- 📂 [All scan results](./security/) are published
- 🔧 [Security scanning tools](./scripts/) are open source
- 📊 [Raw security data](./data/servers.json) is machine-readable
- 🔄 [GitHub Actions workflows](./.github/workflows/) run publicly
- 📝 [Detailed methodology](./security/README.md) is documented

## 🤝 Community-Driven

**We need your help to make this better:**
- 🐛 **Found an error?** [Open an issue](../../issues/new)
- 🔍 **Disagree with an assessment?** [Start a discussion](../../discussions)
- 📈 **Suggest improvements?** [Submit a PR](./CONTRIBUTING.md)
- 🛡️ **Security expert?** [Join our review process](./CONTRIBUTING.md#manual-security-review)

## ⚠️ Important Limitations

**Please understand what this list does and doesn't provide:**

### ✅ What we do:
- Run automated security scans using open-source tools
- Check for known vulnerabilities in dependencies
- Detect common security anti-patterns
- Look for MCP-specific "tool poisoning" attacks
- Provide reproducible, version-specific assessments

### ❌ What we don't do:
- Guarantee security (no tool can do this)
- Test runtime behavior or complex attack scenarios
- Audit cryptographic implementations in detail
- Check for zero-day vulnerabilities
- Replace your own security assessment

### 🔬 Our Security Assessment Process

**Automated Scanning (Objective):**
- **Static Analysis**: Code patterns, potential vulnerabilities
- **Dependency Scanning**: Known CVEs in third-party packages  
- **Tool Poisoning Detection**: Malicious instructions in MCP tool descriptions
- **Container Security**: Dockerfile and image analysis

**Manual Review (Subjective):**
- Architecture and design review
- Authentication/authorization assessment
- Documentation quality evaluation
- Security best practices compliance

**Scoring Method:**
- Weighted combination of scan results (see [methodology](./security/README.md))
- Scores are **indicative, not definitive**
- Multiple reviewers for subjective assessments (see [review team](./REVIEWERS.md))

## Legend

- 🛡️ **Verified Secure**: Passed comprehensive security validation
- ⚠️ **Conditional**: Secure with specific configuration requirements
- 🔄 **Under Review**: Currently undergoing security validation
- ❌ **Not Recommended**: Known security issues
- 📊 **Version**: Latest validated secure version

## 🚧 Sample Assessments (Demo Data)

**Important**: The servers listed below are **examples with placeholder security assessments**. These are not real security evaluations - they demonstrate the format and structure of our assessment system.

### Official Servers (Sample)

*Note: These are placeholder assessments to show the system structure*

| Server | Version | Security | Description |
|--------|---------|----------|-------------|
| [Everything](https://github.com/modelcontextprotocol/servers/tree/main/src/everything) | 📊 0.5.0 | 🛡️ | Reference server demonstrating all MCP features |
| [Filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) | 📊 0.4.1 | 🛡️ | Secure file operations with configurable access controls |
| [Fetch](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) | 📊 0.3.2 | 🛡️ | Web content fetching and conversion |
| [Git](https://github.com/modelcontextprotocol/servers/tree/main/src/git) | 📊 0.2.1 | 🛡️ | Git repository operations |
| [Memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) | 📊 0.1.3 | 🛡️ | Persistent memory and knowledge graphs |

### Enterprise Servers (Sample)

*Note: These are placeholder assessments to demonstrate system capabilities*

| Server | Version | Security | Description |
|--------|---------|----------|-------------|
| [AWS](https://github.com/aws/aws-mcp-server) | 📊 1.2.0 | 🛡️ | AWS service integration with IAM controls |
| [Google Drive](https://github.com/google/mcp-googledrive) | 📊 0.8.1 | 🛡️ | Google Drive file operations |
| [Kubernetes](https://github.com/kubernetes-sigs/mcp-kubernetes) | 📊 0.6.0 | ⚠️ | Kubernetes cluster management (requires RBAC) |

### Security Tools (Sample)

*Note: These are placeholder assessments showing security tool evaluation*

| Server | Version | Security | Description |
|--------|---------|----------|-------------|
| [Nuclei](https://github.com/cyproxio/mcp-for-security/tree/main/nuclei) | 📊 0.2.0 | 🛡️ | Template-based vulnerability scanner |
| [Nmap](https://github.com/cyproxio/mcp-for-security/tree/main/nmap) | 📊 0.1.8 | 🛡️ | Network scanning and service detection |
| [HTTP Security Headers](https://github.com/cyproxio/mcp-for-security/tree/main/http-headers) | 📊 0.1.2 | 🛡️ | HTTP security header analysis |

### Community Servers (Sample)

*Note: These are placeholder assessments demonstrating community server review*

| Server | Version | Security | Description |
|--------|---------|----------|-------------|
| [Slack](https://github.com/slack-samples/mcp-slack) | 📊 1.0.3 | 🛡️ | Slack workspace integration |
| [Email](https://github.com/community/mcp-email) | 📊 0.4.2 | ⚠️ | Email operations (requires OAuth) |
| [SQLite](https://github.com/community/mcp-sqlite) | 📊 0.7.1 | 🛡️ | SQLite database operations |

### Under Review (Sample)

*Note: These demonstrate the review process for complex or high-risk servers*

| Server | Version | Security | Description |
|--------|---------|----------|-------------|
| [Anthropic Computer Use](https://github.com/anthropics/anthropic-computer-use) | 📊 0.1.0 | 🔄 | Desktop automation (high-privilege operations) |
| [Puppeteer](https://github.com/community/mcp-puppeteer) | 📊 0.3.0 | 🔄 | Web browser automation |

## 🚨 Critical Disclaimers

### Security Assessment Limitations
**This list provides security indicators, not guarantees:**

- ✅ **Automated scans** catch common issues but miss complex vulnerabilities
- ✅ **Manual reviews** are subjective and limited by reviewer expertise  
- ❌ **No runtime testing** - we don't test actual MCP server behavior
- ❌ **No penetration testing** - we don't attempt to exploit vulnerabilities
- ❌ **No guarantees** - security status can change at any time

### Your Responsibility
**You must still:**
- Perform your own security assessment for production use
- Keep servers updated and monitor for new vulnerabilities
- Follow the principle of least privilege
- Implement proper monitoring and incident response

## 🤝 How to Help

### 🔍 Review Our Work
- **Challenge our assessments** - if you disagree, tell us why
- **Audit our tools** - all scanning code is open source
- **Verify our data** - check scan results against actual repositories
- **Test our methodology** - try our tools on servers you know well

### 📬 Get Involved
- **Join discussions** on security assessment methodology
- **Submit servers** for community review
- **Contribute code** to improve our scanning tools
- **Share expertise** through manual security reviews

### 🐛 Report Issues
- **Assessment errors** - wrong security status or score
- **Missing servers** - suggest additions with justification
- **Tool bugs** - problems with our scanning scripts
- **Process improvements** - better ways to assess security

## 🔗 Community & Resources

### Official MCP Resources
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
- [MCP Documentation](https://docs.anthropic.com/claude/docs/mcp)

### Related Security Projects
- [MCP for Security](https://github.com/cyproxio/mcp-for-security) - Security-focused MCP servers
- [Awesome MCP Servers](https://github.com/wong2/awesome-mcp-servers) - Comprehensive MCP server list

### Security Research
- [MCP Security Best Practices](./security/README.md) - Our detailed methodology
- [Tool Poisoning Research](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)

---

## 📞 Contact & Support

- 💬 **General questions**: [Open a discussion](../../discussions)
- 🐛 **Bug reports**: [Create an issue](../../issues)
- 🔒 **Security vulnerabilities**: Create a private security advisory
- 📧 **Direct contact**: maintainers@fuzzylabs.ai

## 📄 License & Legal

This project is published under the [MIT License](LICENSE).

**Important**: We are not affiliated with Anthropic or the official MCP project. This is an independent community initiative focused on security assessment of MCP servers.

**Final Reminder**: Security assessments are performed to the best of our ability using available tools and methods. This list does not guarantee the security of any MCP server. Always perform your own security evaluation before using any software in production environments.