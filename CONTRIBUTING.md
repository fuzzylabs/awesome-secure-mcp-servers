# Contributing to Awesome Secure MCP Servers

Thank you for helping make the MCP ecosystem more secure! This project depends on community involvement to provide trustworthy, transparent security assessments.

## 🎯 How You Can Help

### 🔍 **Challenge Our Work**
- Review our security assessments and tell us if you disagree
- Test our automated scanning tools on servers you know well
- Audit our methodology and suggest improvements
- Point out errors or biases in our evaluations

### 🛠️ **Improve Our Tools**
- Contribute to our [open-source scanning scripts](./scripts/)
- Add support for new programming languages or frameworks
- Improve detection of security anti-patterns
- Help reduce false positives/negatives

### 📊 **Share Your Expertise**
- Join our manual security review process
- Provide expert opinions on complex security questions
- Help develop better assessment criteria
- Review and validate automated scan results

### 🚀 **Submit Servers**
- Nominate MCP servers for security assessment
- Provide context about server security features
- Help us understand real-world usage patterns

## 🔍 Complete Transparency Policy

**Everything we do is open:**
- All scan results are published (including failures)
- All tools and methodology are open source
- All review criteria are documented
- All assessment decisions are explained
- Community feedback is public and tracked

## 📋 Security Assessment Process

### 🤖 Automated Scanning (Objective)

**What our tools check:**
- Static code analysis for common vulnerabilities
- Dependency scanning for known CVEs
- Tool poisoning detection (MCP-specific threat)
- Container security configuration
- Code quality and security practices

**What our tools DON'T check:**
- Runtime behavior or logic flaws
- Complex business logic vulnerabilities  
- Advanced cryptographic implementations
- Social engineering or phishing potential
- Zero-day vulnerabilities

**Tools we use:**
- `bandit` (Python security analysis)
- `semgrep` (multi-language security patterns)
- `npm audit` / `safety` (dependency vulnerabilities)
- Custom tool poisoning detection scripts

### 👥 Manual Review (Subjective)

**What reviewers assess:**
- Architecture and design security
- Authentication/authorization implementation
- Security documentation quality
- Adherence to security best practices
- Risk assessment for intended use cases

**Review limitations:**
- Based on available documentation and code
- Limited by individual reviewer expertise
- Subjective interpretation of security practices
- No hands-on testing or penetration testing
- Time-constrained review process

## How to Contribute

### Submitting a New MCP Server

1. **Fork this repository**
2. **Create a new branch** for your submission
3. **Add your server** to the appropriate category in README.md
4. **Include required information** (see [Submission Guidelines](#submission-guidelines))
5. **Submit a pull request** with detailed information
6. **Wait for security validation** (automated and manual review)

### Updating Existing Servers

1. **Version Updates**: Report new versions that need security validation
2. **Security Issues**: Report discovered vulnerabilities (see [Reporting Issues](#reporting-issues))
3. **Documentation**: Improve server descriptions or security notes

## Security Validation Process

All submitted MCP servers undergo a comprehensive security validation process:

### Automated Security Scanning

1. **Static Code Analysis**: Automated scanning for common vulnerabilities
2. **Dependency Scanning**: Check for known vulnerabilities in dependencies
3. **Container Security**: If containerized, scan container images
4. **Tool Poisoning Detection**: Analysis of tool descriptions for malicious content

### Manual Security Review

1. **Architecture Review**: Assess overall security design
2. **Authentication Analysis**: Review auth mechanisms and token handling
3. **Permission Evaluation**: Analyze required permissions and access controls
4. **Documentation Review**: Verify security documentation completeness

### Validation Timeline

- **Initial Review**: 3-5 business days for automated scanning
- **Manual Review**: 7-14 business days depending on complexity
- **Total Process**: Typically 2-3 weeks for comprehensive validation

## Submission Guidelines

### Required Information

When submitting a new MCP server, include:

```markdown
| [Server Name](github-url) | 📊 version | 🔄 | Brief description |
```

### Additional Details Required

1. **Server Information**:
   - Name and brief description
   - GitHub repository URL
   - Current version number
   - MCP protocol version compatibility
   - Programming language(s)

2. **Security Information**:
   - Authentication method used
   - Required permissions
   - Container/Docker support
   - Known security considerations
   - Recommended security configuration

3. **Deployment Information**:
   - Installation instructions
   - Configuration requirements
   - Environment variables needed
   - Network requirements

### Example Submission

```markdown
## New Server Submission: ExampleMCP

**Repository**: https://github.com/example/example-mcp
**Version**: 1.2.3
**MCP Protocol**: 2024-11-05
**Language**: TypeScript
**Category**: Development Tools

**Description**: 
Secure file processing server with sandboxed execution environment.

**Security Features**:
- OAuth 2.0 authentication
- Sandboxed file processing
- Configurable access controls
- Audit logging

**Required Permissions**:
- File system read/write (configurable scope)
- Network access for OAuth

**Container Support**: Yes, Dockerfile provided

**Security Considerations**:
- Requires proper OAuth configuration
- File access should be limited to designated directories
- Network policies recommended for production use
```

## Security Criteria

### Passing Criteria

To be listed as "Verified Secure" 🛡️, servers must:

1. **Authentication**: Implement secure authentication mechanisms
2. **Authorization**: Proper access controls and permission checking
3. **Input Validation**: Validate all inputs from MCP clients
4. **Error Handling**: Secure error handling without information leakage
5. **Dependencies**: No known high-severity vulnerabilities in dependencies
6. **Documentation**: Clear security documentation and configuration guidance

### Conditional Listing

Servers marked as "Conditional" ⚠️ may have:

- High-privilege requirements with proper documentation
- Complex configuration needs for security
- Limited scope of validated security features

### Rejection Criteria

Servers will be rejected if they:

- Contain known high-severity security vulnerabilities
- Lack basic authentication mechanisms
- Have tool poisoning vulnerabilities
- Provide insufficient security documentation
- Expose sensitive system functions without proper controls

## Version Management

### Version Tracking

We track security validation per version:

- **Major versions**: Full security re-validation required
- **Minor versions**: Security impact assessment
- **Patch versions**: Vulnerability scanning only

### Version Updates

When submitting version updates:

1. **Include changelog** highlighting security-relevant changes
2. **Note breaking changes** that might affect security
3. **Update MCP protocol compatibility** if changed
4. **Mention dependency updates** and security implications

### Deprecation

Servers may be moved to deprecated status if:

- No longer maintained by original authors
- Contain unpatched security vulnerabilities
- Incompatible with current MCP protocol versions

## Reporting Issues

### Security Vulnerabilities

**CRITICAL**: Do not report security vulnerabilities publicly.

1. **Email**: security@awesome-secure-mcp-servers.org
2. **Include**:
   - Server name and version
   - Vulnerability description
   - Proof of concept (if applicable)
   - Suggested remediation

### General Issues

For non-security issues, create a GitHub issue with:

- Clear description of the problem
- Server name and version
- Steps to reproduce
- Expected vs actual behavior

## Review Process

### Pull Request Review

1. **Automated Checks**: CI/CD pipeline runs security scans
2. **Maintainer Review**: Manual review of submission
3. **Security Validation**: Comprehensive security assessment
4. **Community Feedback**: Open for community comments
5. **Final Approval**: Merge after successful validation

### Review Criteria

PRs are evaluated on:

- **Completeness**: All required information provided
- **Accuracy**: Correct and up-to-date information
- **Security**: Passes security validation
- **Quality**: Follows contribution guidelines
- **Relevance**: Fits within project scope

## Code of Conduct

This project follows a standard Code of Conduct. Please be respectful and constructive in all interactions.

## Getting Help

- **Questions**: Open a GitHub issue with the "question" label
- **Security Concerns**: Email security@awesome-secure-mcp-servers.org
- **General Discussion**: Use GitHub Discussions

## Recognition

Contributors will be recognized in:

- GitHub contributors list
- Annual contributor acknowledgments
- Security researcher credits (for vulnerability reports)

Thank you for helping make the MCP ecosystem more secure!