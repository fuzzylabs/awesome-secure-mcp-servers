# Awesome Secure MCP Servers [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of security-validated Model Context Protocol (MCP) servers with version-specific vulnerability assessments

The Model Context Protocol (MCP) enables secure connections between AI assistants and external systems. This list focuses on MCP servers that have been security-validated to ensure they operate safely and as advertised.

## Security Validation

Each MCP server in this list has undergone security validation including:

- **Automated Security Scanning**: Static analysis and vulnerability detection
- **Tool Poisoning Analysis**: Detection of malicious instructions in tool descriptions
- **Token Security Review**: Assessment of authentication and authorization practices
- **Container Security**: Evaluation of containerized deployment safety
- **Version Tracking**: Security status maintained per version

## Legend

- 🛡️ **Verified Secure**: Passed comprehensive security validation
- ⚠️ **Conditional**: Secure with specific configuration requirements
- 🔄 **Under Review**: Currently undergoing security validation
- ❌ **Not Recommended**: Known security issues
- 📊 **Version**: Latest validated secure version

## Official Servers

Maintained by Anthropic and the MCP team.

### Core Servers

| Server | Version | Security | Description |
|--------|---------|----------|-------------|
| [Everything](https://github.com/modelcontextprotocol/servers/tree/main/src/everything) | 📊 0.5.0 | 🛡️ | Reference server demonstrating all MCP features |
| [Filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) | 📊 0.4.1 | 🛡️ | Secure file operations with configurable access controls |
| [Fetch](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) | 📊 0.3.2 | 🛡️ | Web content fetching and conversion |
| [Git](https://github.com/modelcontextprotocol/servers/tree/main/src/git) | 📊 0.2.1 | 🛡️ | Git repository operations |
| [Memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) | 📊 0.1.3 | 🛡️ | Persistent memory and knowledge graphs |

## Enterprise Verified Servers

Production-ready servers maintained by companies with security attestations.

### Cloud & Infrastructure

| Server | Version | Security | Description |
|--------|---------|----------|-------------|
| [AWS](https://github.com/aws/aws-mcp-server) | 📊 1.2.0 | 🛡️ | AWS service integration with IAM controls |
| [Google Drive](https://github.com/google/mcp-googledrive) | 📊 0.8.1 | 🛡️ | Google Drive file operations |
| [Kubernetes](https://github.com/kubernetes-sigs/mcp-kubernetes) | 📊 0.6.0 | ⚠️ | Kubernetes cluster management (requires RBAC) |

### Development Tools

| Server | Version | Security | Description |
|--------|---------|----------|-------------|
| [GitHub](https://github.com/github/mcp-github-server) | 📊 2.1.0 | 🛡️ | GitHub repository operations |
| [Docker](https://github.com/docker/mcp-docker) | 📊 1.5.2 | ⚠️ | Docker container management (requires socket access) |
| [Postgres](https://github.com/postgres/mcp-postgres) | 📊 1.3.1 | 🛡️ | PostgreSQL database operations |

## Security Tools

MCP servers specifically designed for defensive security operations.

### Vulnerability Management

| Server | Version | Security | Description |
|--------|---------|----------|-------------|
| [Nuclei](https://github.com/cyproxio/mcp-for-security/tree/main/nuclei) | 📊 0.2.0 | 🛡️ | Template-based vulnerability scanner |
| [Nmap](https://github.com/cyproxio/mcp-for-security/tree/main/nmap) | 📊 0.1.8 | 🛡️ | Network scanning and service detection |
| [HTTP Security Headers](https://github.com/cyproxio/mcp-for-security/tree/main/http-headers) | 📊 0.1.2 | 🛡️ | HTTP security header analysis |

### Cloud Security

| Server | Version | Security | Description |
|--------|---------|----------|-------------|
| [Scout Suite](https://github.com/cyproxio/mcp-for-security/tree/main/scout-suite) | 📊 0.3.0 | 🛡️ | Multi-cloud security auditing |
| [MobSF](https://github.com/cyproxio/mcp-for-security/tree/main/mobsf) | 📊 0.2.1 | 🛡️ | Mobile application security testing |

## Community Verified Servers

Community-maintained servers that have passed security validation.

### Productivity

| Server | Version | Security | Description |
|--------|---------|----------|-------------|
| [Slack](https://github.com/slack-samples/mcp-slack) | 📊 1.0.3 | 🛡️ | Slack workspace integration |
| [Email](https://github.com/community/mcp-email) | 📊 0.4.2 | ⚠️ | Email operations (requires OAuth) |

### Development

| Server | Version | Security | Description |
|--------|---------|----------|-------------|
| [SQLite](https://github.com/community/mcp-sqlite) | 📊 0.7.1 | 🛡️ | SQLite database operations |
| [Redis](https://github.com/community/mcp-redis) | 📊 0.5.0 | ⚠️ | Redis cache operations (requires authentication) |

## Under Review

Servers currently undergoing security validation.

| Server | Version | Security | Description |
|--------|---------|----------|-------------|
| [Anthropic Computer Use](https://github.com/anthropics/anthropic-computer-use) | 📊 0.1.0 | 🔄 | Desktop automation (high-privilege operations) |
| [Puppeteer](https://github.com/community/mcp-puppeteer) | 📊 0.3.0 | 🔄 | Web browser automation |

## Security Guidelines

### For Users

1. **Version Pinning**: Always use specific versions rather than "latest"
2. **Container Deployment**: Run MCP servers in containers when possible
3. **Principle of Least Privilege**: Grant minimal necessary permissions
4. **Regular Updates**: Monitor for security updates and patches
5. **Environment Isolation**: Use separate environments for different security contexts

### For Server Developers

1. **Security Documentation**: Clearly document security implications
2. **Input Validation**: Validate all inputs from the MCP client
3. **Authentication**: Implement proper authentication and authorization
4. **Audit Logging**: Log all operations for security auditing
5. **Container Support**: Provide secure container configurations

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- How to submit new servers for security validation
- Security validation process and criteria
- Reporting security vulnerabilities

## Security Vulnerability Reporting

If you discover a security vulnerability in any listed MCP server:

1. **DO NOT** create a public issue
2. Email security details to: security@awesome-secure-mcp-servers.org
3. Include version information and reproduction steps
4. We will coordinate with server maintainers for responsible disclosure

## Related Projects

- [Official MCP Servers](https://github.com/modelcontextprotocol/servers) - Reference implementations
- [MCP for Security](https://github.com/cyproxio/mcp-for-security) - Security-focused MCP servers
- [Awesome MCP Servers](https://github.com/wong2/awesome-mcp-servers) - Comprehensive MCP server list

## License

This list is published under the [MIT License](LICENSE).

---

**Disclaimer**: Security validations are performed to the best of our ability with available tools and methods. Users should perform their own security assessments for production use. The security status of servers may change over time with new versions or discovered vulnerabilities.