# Awesome Secure MCP Servers [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A curated list of Model Context Protocol (MCP) servers with comprehensive security validation using the `mcp-scan` security assessment pipeline.

## Mission

This project provides transparent, reproducible security assessments of MCP servers using automated scanning tools to help developers make informed decisions about MCP server security.

## Transparency

All assessment components are publicly available:
- [Scan results](./security/) are published
- [Security scanning tools](./scripts/) are open source
- [Raw security data](./data/servers.json) is machine-readable
- [GitHub Actions workflows](./.github/workflows/) run publicly
- [Detailed methodology](./security/README.md) is documented

## Community Involvement

Help improve this project:
- **Found an error?** [Open an issue](../../issues/new)
- **Disagree with an assessment?** [Start a discussion](../../discussions)
- **Suggest improvements?** [Submit a PR](./CONTRIBUTING.md)
- **Security expert?** [Join our review process](./CONTRIBUTING.md#manual-security-review)

## Limitations

### What we do:
- Run automated security scans using `mcp-scan` by Invariant Labs for MCP-specific threats
- Check for known vulnerabilities in dependencies using language-specific tools
- Detect common security anti-patterns with static analysis
- Identify MCP-specific vulnerabilities including tool poisoning, cross-origin escalation, and rug pull attacks
- Provide reproducible, version-specific assessments with detailed scoring

### What we don't do:
- Guarantee security (no tool can do this)
- Test runtime behavior or complex attack scenarios
- Audit cryptographic implementations in detail
- Check for zero-day vulnerabilities
- Replace your own security assessment

### Security Assessment Process

**Automated Scanning:**
- **MCP Security Scan**: Using `mcp-scan` for MCP-specific threats (tool poisoning, cross-origin escalation, rug pulls)
- **Static Analysis**: Code patterns and potential vulnerabilities using language-specific tools
- **Dependency Scanning**: Known CVEs in third-party packages  
- **Container Security**: Dockerfile and image analysis when applicable

**Manual Review:**
- Architecture and design review
- Authentication/authorization assessment
- Documentation quality evaluation
- Security best practices compliance

**Scoring Method:**
- Weighted combination of scan results: MCP Security (35%), Dependencies (25%), Static Analysis (20%), Container (10%), Documentation (10%)
- Scores are indicative, not definitive
- Multiple reviewers for subjective assessments (see [review team](./REVIEWERS.md))
- See [detailed methodology](./security/README.md) for complete scoring breakdown

## Legend

- **Verified Secure**: Passed comprehensive security validation
- **Conditional**: Secure with specific configuration requirements  
- **Under Review**: Currently undergoing security validation
- **Not Recommended**: Known security issues
- **Version**: Latest validated secure version

## Security Status by Category

**Last Updated:** 2025-06-24 21:56 UTC  
**Total Servers:** 16

### Official Servers

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [Everything (Reference Server)](https://github.com/modelcontextprotocol/servers/tree/main/src/everything) | 0.5.0 | 🛡️ Verified Secure (Score: 93/100) | Reference server demonstrating all MCP features |
| [Fetch Server](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) | 0.3.2 | 🔄 Under Review (Score: 50/100) | Web content fetching and conversion for efficient LLM usage |
| [Filesystem Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) | 0.4.1 | 🛡️ Verified Secure (Score: 91/100) | Secure file operations with configurable access controls |
| [Git Server](https://github.com/modelcontextprotocol/servers/tree/main/src/git) | 0.2.1 | 🔄 Under Review (Score: 50/100) | Tools to read, search, and manipulate Git repositories |
| [Memory Server](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) | 0.1.3 | 🔄 Under Review (Score: 50/100) | Persistent memory using a local knowledge graph |
| [Sequential Thinking Server](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) | 0.1.0 | 🔄 Under Review (Score: 50/100) | Dynamic and reflective problem-solving through thought sequences |
| [Time Server](https://github.com/modelcontextprotocol/servers/tree/main/src/time) | 0.1.2 | 🔄 Under Review (Score: 50/100) | Time and timezone conversion capabilities |

### Enterprise Servers

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [AWS MCP Server](https://github.com/aws/aws-mcp-server) | 1.2.0 | 🔄 Under Review (Score: 50/100) | AWS service integration with IAM controls |
| [Docker Server](https://github.com/docker/mcp-docker) | 1.5.2 | ⚠️ Conditional (Score: 78/100) | Docker container management with security controls |
| [GitHub MCP Server](https://github.com/github/github-mcp-server) | 1.0.0 | 🔄 Under Review (Score: 50/100) | GitHub's official MCP Server for repository management |
| [Notion MCP Server](https://github.com/makenotion/notion-mcp-server) | 0.3.1 | 🔄 Under Review (Score: 50/100) | Notion official MCP server for workspace integration |
| [Stripe MCP Server](https://github.com/stripe/agent-toolkit) | 0.2.0 | 🔄 Under Review (Score: 50/100) | Interact with Stripe API for payments and financial data |

### Security Tools

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [Nuclei Security Scanner](https://github.com/cyproxio/mcp-for-security/tree/main/nuclei) | 0.2.0 | 🛡️ Verified Secure (Score: 88/100) | Template-based vulnerability scanner with extensive security checks |

### Community Servers

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [PostgreSQL MCP Server](https://github.com/postgres/mcp-postgres) | 0.4.2 | 🔄 Under Review (Score: 50/100) | PostgreSQL database operations and query execution |
| [Slack MCP Server](https://github.com/slack-samples/mcp-slack) | 1.0.3 | 🔄 Under Review (Score: 50/100) | Slack workspace integration for messaging and collaboration |

### Under Review

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|
| [Anthropic Computer Use](https://github.com/anthropics/anthropic-computer-use) | 0.1.0 | 🔄 Under Review (Score: 58/100) | Desktop automation with screen capture and input control |

## Critical Disclaimers

### Security Assessment Limitations
This list provides security indicators, not guarantees:

- **Automated scans** catch common issues but miss complex vulnerabilities
- **Manual reviews** are subjective and limited by reviewer expertise  
- **No runtime testing** - we don't test actual MCP server behavior
- **No penetration testing** - we don't attempt to exploit vulnerabilities
- **No guarantees** - security status can change at any time

### Your Responsibility
You must still:
- Perform your own security assessment for production use
- Keep servers updated and monitor for new vulnerabilities
- Follow the principle of least privilege
- Implement proper monitoring and incident response

## How to Help

### Review Our Work
- **Challenge our assessments** - if you disagree, tell us why
- **Audit our tools** - all scanning code is open source
- **Verify our data** - check scan results against actual repositories
- **Test our methodology** - try our tools on servers you know well

### Get Involved
- **Join discussions** on security assessment methodology
- **Submit servers** for community review
- **Contribute code** to improve our scanning tools
- **Share expertise** through manual security reviews

### Report Issues
- **Assessment errors** - wrong security status or score
- **Missing servers** - suggest additions with justification
- **Tool bugs** - problems with our scanning scripts
- **Process improvements** - better ways to assess security

## Community & Resources

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

## Contact & Support

- **General questions**: [Open a discussion](../../discussions)
- **Bug reports**: [Create an issue](../../issues)
- **Security vulnerabilities**: Create a private security advisory
- **Direct contact**: maintainers@fuzzylabs.ai

## License & Legal

This project is published under the [MIT License](LICENSE).

**Important**: We are not affiliated with Anthropic or the official MCP project. This is an independent community initiative focused on security assessment of MCP servers.

**Final Reminder**: Security assessments are performed to the best of our ability using available tools and methods. This list does not guarantee the security of any MCP server. Always perform your own security evaluation before using any software in production environments.