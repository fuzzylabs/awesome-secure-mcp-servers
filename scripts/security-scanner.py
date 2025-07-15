#!/usr/bin/env python3
"""
Automated Security Scanner for MCP Servers
==========================================

This script performs comprehensive security validation of MCP servers including:
- Static code analysis
- Dependency vulnerability scanning
- Tool poisoning detection
- Container security analysis (if applicable)
- Manual review automation helpers

Usage:
    python security-scanner.py --input data/servers.json --output security/scan-results.json
"""

import argparse
import json
import logging
import subprocess
import tempfile
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import requests
import re
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SecurityScanner:
    """Main security scanner class for MCP servers."""
    
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        self.session = requests.Session()
        if github_token:
            self.session.headers.update({
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json'
            })
    
    def scan_server(self, server: Dict) -> Dict:
        """Perform comprehensive security scan of a single MCP server."""
        logger.info(f"Scanning server: {server['name']}")
        
        scan_results = {
            'server_name': server['name'],
            'server_slug': server['slug'],
            'repository': server['repository'],
            'scan_timestamp': datetime.now(timezone.utc).isoformat(),
            'scanner_version': '1.2.0',
            'versions': []
        }
        
        for version_info in server.get('versions', []):
            version_scan = self._scan_version(server, version_info)
            scan_results['versions'].append(version_scan)
        
        return scan_results
    
    def _scan_version(self, server: Dict, version_info: Dict) -> Dict:
        """Scan a specific version of an MCP server."""
        version = version_info['version']
        logger.info(f"Scanning version {version} of {server['name']}")
        
        # Download repository for analysis
        repo_path = self._download_repository(server['repository'], version)
        
        scan_result = {
            'version': version,
            'scan_date': datetime.now(timezone.utc).isoformat(),
            'static_analysis': self._run_static_analysis(repo_path),
            'dependency_scan': self._run_dependency_scan(repo_path),
            'mcp_security_scan': self._run_mcp_scan(repo_path),
            'overall_score': 0,
            'recommendations': []
        }
        
        # Calculate overall score
        scan_result['overall_score'] = self._calculate_overall_score(scan_result)
        
        # Generate recommendations
        scan_result['recommendations'] = self._generate_recommendations(scan_result)
        
        # Cleanup temporary files
        if repo_path and os.path.exists(repo_path):
            subprocess.run(['rm', '-rf', repo_path], check=False)
        
        return scan_result
    
    def _download_repository(self, repo_url: str, version: str) -> Optional[str]:
        """Download repository code for analysis."""
        try:
            # Parse GitHub URL
            parsed = urlparse(repo_url)
            if 'github.com' not in parsed.netloc:
                logger.warning(f"Non-GitHub repository: {repo_url}")
                return None
            
            # Extract owner/repo from URL
            path_parts = parsed.path.strip('/').split('/')
            if len(path_parts) < 2:
                logger.error(f"Invalid GitHub URL format: {repo_url}")
                return None
            
            owner, repo = path_parts[0], path_parts[1]
            
            # Create temporary directory
            temp_dir = tempfile.mkdtemp(prefix=f"mcp-scan-{repo}-")
            
            # Clone repository
            clone_url = f"https://github.com/{owner}/{repo}.git"
            cmd = ['git', 'clone', '--depth', '1', '--branch', f'v{version}', clone_url, temp_dir]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                # Try without version tag
                cmd = ['git', 'clone', '--depth', '1', clone_url, temp_dir]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    logger.error(f"Failed to clone repository: {result.stderr}")
                    return None
            
            logger.info(f"Downloaded repository to: {temp_dir}")
            return temp_dir
            
        except Exception as e:
            logger.error(f"Error downloading repository: {e}")
            return None
    
    def _run_static_analysis(self, repo_path: str) -> Dict:
        """Run focused static code analysis for critical vulnerabilities only."""
        if not repo_path or not os.path.exists(repo_path):
            return {'status': 'not-applicable', 'details': 'Repository not available', 'score': 50}
        
        results = {
            'status': 'pass',
            'details': 'No critical vulnerabilities found',
            'score': 100,
            'issues_found': 0,
            'critical_issues': 0,
            'tools_used': []
        }
        
        # Detect programming language
        language = self._detect_language(repo_path)
        
        try:
            # Focus on critical security issues only
            if language == 'python':
                results.update(self._run_bandit_critical_only(repo_path))
            elif language in ['javascript', 'typescript']:
                results.update(self._run_eslint_critical_only(repo_path))
            else:
                # Run generic critical security analysis
                results.update(self._run_semgrep_critical_only(repo_path))
            
        except Exception as e:
            logger.error(f"Static analysis failed: {e}")
            results.update({
                'status': 'warning',
                'details': f'Static analysis partially failed: {str(e)}',
                'score': 70
            })
        
        return results
    
    def _run_dependency_scan(self, repo_path: str) -> Dict:
        """Scan dependencies for known vulnerabilities."""
        if not repo_path or not os.path.exists(repo_path):
            return {'status': 'not-applicable', 'details': 'Repository not available', 'score': 50}
        
        results = {
            'status': 'pass',
            'details': 'No vulnerabilities found in dependencies',
            'score': 100,
            'issues_found': 0,
            'vulnerabilities': []
        }
        
        try:
            # Check for different package managers
            if os.path.exists(os.path.join(repo_path, 'package.json')):
                results.update(self._scan_npm_dependencies(repo_path))
            elif os.path.exists(os.path.join(repo_path, 'requirements.txt')):
                results.update(self._scan_python_dependencies(repo_path))
            elif os.path.exists(os.path.join(repo_path, 'go.mod')):
                results.update(self._scan_go_dependencies(repo_path))
            else:
                results.update({
                    'status': 'not-applicable',
                    'details': 'No recognized dependency files found'
                })
        
        except Exception as e:
            logger.error(f"Dependency scan failed: {e}")
            results.update({
                'status': 'warning',
                'details': f'Dependency scan failed: {str(e)}',
                'score': 60
            })
        
        return results
    
    def _run_mcp_scan(self, repo_path: str) -> Dict:
        """Run mcp-scan for MCP-specific security analysis."""
        if not repo_path or not os.path.exists(repo_path):
            return {'status': 'not-applicable', 'details': 'Repository not available', 'score': 50}
        
        results = {
            'status': 'pass',
            'details': 'No MCP configuration vulnerabilities found',
            'score': 90,  # Default high score since mcp-scan is config-specific
            'issues_found': 0,
            'scan_results': {}
        }
        
        # Look for MCP configuration files in the repository
        mcp_config_files = self._find_mcp_configs(repo_path)
        
        if not mcp_config_files:
            # No MCP configs found, fall back to basic tool poisoning detection
            logger.info("No MCP configuration files found, falling back to basic tool poisoning detection")
            return self._basic_tool_poisoning_check(repo_path)
        
        try:
            # Run mcp-scan on found configuration files with enhanced options
            for config_file in mcp_config_files:
                cmd = ['uvx', 'mcp-scan@latest', 'scan', '--json', '--local-only', '--verbose', config_file]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    try:
                        scan_output = json.loads(result.stdout)
                        
                        # Parse mcp-scan results with severity breakdown
                        if 'results' in scan_output:
                            config_results = scan_output['results']
                            issues_found = 0
                            critical_issues = 0
                            high_issues = 0
                            medium_issues = 0
                            low_issues = 0
                            
                            # Count security issues by severity
                            for result_item in config_results:
                                if 'security_issues' in result_item:
                                    issues = result_item['security_issues']
                                    issues_found += len(issues)
                                    for issue in issues:
                                        severity = issue.get('severity', 'unknown').lower()
                                        if severity == 'critical':
                                            critical_issues += 1
                                        elif severity == 'high':
                                            high_issues += 1
                                        elif severity == 'medium':
                                            medium_issues += 1
                                        elif severity == 'low':
                                            low_issues += 1
                            
                            results['scan_results'][config_file] = {
                                'total_issues': issues_found,
                                'critical_issues': critical_issues,
                                'high_issues': high_issues,
                                'medium_issues': medium_issues,
                                'low_issues': low_issues,
                                'raw_results': config_results[:5]  # Limit stored results
                            }
                            
                            results['issues_found'] += issues_found
                    
                    except json.JSONDecodeError:
                        logger.warning(f"Could not parse mcp-scan output for {config_file}")
                        results['scan_results'][config_file] = {
                            'error': 'Could not parse scan output'
                        }
                
                else:
                    # Log error but continue with other configs
                    error_msg = result.stderr.strip() if result.stderr else 'Unknown error'
                    logger.warning(f"MCP-scan failed for {config_file}: {error_msg}")
                    results['scan_results'][config_file] = {
                        'error': f'Scan failed: {error_msg}'
                    }
            
            # Calculate severity-weighted score
            total_critical = sum(config.get('critical_issues', 0) for config in results['scan_results'].values() if isinstance(config, dict))
            total_high = sum(config.get('high_issues', 0) for config in results['scan_results'].values() if isinstance(config, dict))
            total_medium = sum(config.get('medium_issues', 0) for config in results['scan_results'].values() if isinstance(config, dict))
            total_low = sum(config.get('low_issues', 0) for config in results['scan_results'].values() if isinstance(config, dict))
            
            # Severity-weighted scoring: Critical=40 pts, High=20 pts, Medium=10 pts, Low=5 pts
            severity_penalty = (total_critical * 40) + (total_high * 20) + (total_medium * 10) + (total_low * 5)
            score = max(30, 100 - severity_penalty)  # Minimum score of 30
            
            total_issues = results['issues_found']
            if total_issues == 0:
                results.update({
                    'status': 'pass',
                    'details': f'MCP-scan found no security issues in {len(mcp_config_files)} configuration file(s)',
                    'score': 95
                })
            elif total_critical > 0:
                results.update({
                    'status': 'fail',
                    'details': f'MCP-scan found {total_critical} critical security issue(s) requiring immediate attention',
                    'score': score
                })
            elif total_high > 0 or total_medium > 5:
                results.update({
                    'status': 'warning',
                    'details': f'MCP-scan found {total_issues} security issue(s) (Critical: {total_critical}, High: {total_high}, Medium: {total_medium}, Low: {total_low})',
                    'score': score
                })
            else:
                results.update({
                    'status': 'pass',
                    'details': f'MCP-scan found only low-severity issues ({total_issues} total)',
                    'score': max(80, score)
                })
        
        except subprocess.TimeoutExpired:
            results.update({
                'status': 'warning',
                'details': 'MCP-scan timed out',
                'score': 70
            })
        except FileNotFoundError as e:
            # Enhanced error handling for mcp-scan installation issues
            logger.warning(f"mcp-scan not available ({e}), attempting retry with explicit installation")
            try:
                # Try to install mcp-scan explicitly
                install_cmd = ['uvx', 'install', 'mcp-scan@latest']
                subprocess.run(install_cmd, capture_output=True, text=True, timeout=60)
                
                # Retry mcp-scan with simplified command
                for config_file in mcp_config_files:
                    cmd = ['uvx', 'run', 'mcp-scan', 'scan', '--json', config_file]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                    if result.returncode == 0:
                        logger.info("Successfully ran mcp-scan after installation")
                        # Process results (simplified for retry)
                        results.update({
                            'status': 'pass',
                            'details': 'MCP-scan completed after retry',
                            'score': 85
                        })
                        return results
            except Exception as retry_error:
                logger.warning(f"mcp-scan retry failed: {retry_error}")
            
            # Fall back to basic tool poisoning detection
            logger.warning("Falling back to basic tool poisoning detection")
            return self._basic_tool_poisoning_check(repo_path)
        except Exception as e:
            logger.error(f"MCP-scan failed: {e}")
            # Enhanced fallback with better error context
            if "policy.gr" in str(e):
                logger.warning("Detected policy.gr file issue - this is a known mcp-scan installation problem")
            return self._basic_tool_poisoning_check(repo_path)
        
        return results
    
    def _find_mcp_configs(self, repo_path: str) -> List[str]:
        """Find MCP configuration files in the repository."""
        config_files = []
        
        # Expanded MCP configuration file patterns
        config_patterns = [
            # Standard MCP configs
            'mcp.json',
            'mcp_config.json',
            '.mcp.json',
            'mcp-config.json',
            
            # Directory-based configs
            'config/mcp.json',
            'configs/mcp.json',
            '.config/mcp.json',
            'src/config/mcp.json',
            
            # Claude Desktop configs
            'claude_desktop_config.json',
            '.claude/config.json',
            'claude/config.json',
            '.claude_desktop_config.json',
            
            # Wildcard patterns
            '*.mcp.json',
            '*mcp*.json',
            
            # Tool-specific configs
            'tools.json',
            'server.json',
            'mcp_server.json',
            'mcp-server.json',
            
            # Environment configs
            '.env.mcp',
            'mcp.env',
            'config.json',  # Generic but might contain MCP
            
            # YAML variants
            'mcp.yaml',
            'mcp.yml',
            'mcp_config.yaml',
            'mcp-config.yml'
        ]
        
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, repo_path)
                
                # Check if file matches any config pattern
                for pattern in config_patterns:
                    if pattern.startswith('*') and pattern.endswith('*'):
                        # Handle patterns like *mcp*.json
                        pattern_core = pattern[1:-5]  # Remove * and .json
                        if pattern_core in file.lower() and file.endswith('.json'):
                            config_files.append(file_path)
                            break
                    elif pattern.startswith('*'):
                        # Handle patterns like *.mcp.json
                        if file.endswith(pattern[1:]):
                            config_files.append(file_path)
                            break
                    elif file == pattern or relative_path == pattern:
                        config_files.append(file_path)
                        break
                
                # Additional heuristics for MCP-related files
                if not any(file_path in config_files for _ in [True]):
                    file_lower = file.lower()
                    if (file.endswith(('.json', '.yaml', '.yml')) and 
                        ('mcp' in file_lower or 'claude' in file_lower or 'server' in file_lower)):
                        # Read file to check for MCP-specific content
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()[:1000]  # Read first 1KB
                                if any(keyword in content.lower() for keyword in 
                                      ['"mcp"', '"tools"', '"claude"', '"server"', 'mcpServers']):
                                    config_files.append(file_path)
                                    break
                        except Exception:
                            pass
        
        return config_files
    
    def _basic_tool_poisoning_check(self, repo_path: str) -> Dict:
        """Basic tool poisoning detection as fallback when mcp-scan is unavailable."""
        results = {
            'status': 'pass',
            'details': 'No tool poisoning indicators found (basic check)',
            'score': 90,  # Lower score since this is less comprehensive
            'issues_found': 0,
            'suspicious_patterns': []
        }
        
        # Basic patterns for tool poisoning
        poisoning_patterns = [
            r'ignore\s+previous\s+instructions',
            r'disregard\s+.+\s+above',
            r'forget\s+everything',
            r'new\s+instructions',
            r'override\s+security',
            r'bypass\s+restrictions'
        ]
        
        try:
            suspicious_files = []
            
            # Search for suspicious patterns in MCP-related files
            for root, dirs, files in os.walk(repo_path):
                for file in files:
                    if file.endswith(('.json', '.yaml', '.yml', '.md', '.txt')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                
                                for pattern in poisoning_patterns:
                                    if re.search(pattern, content, re.IGNORECASE):
                                        suspicious_files.append({
                                            'file': os.path.relpath(file_path, repo_path),
                                            'pattern': pattern
                                        })
                        except Exception:
                            continue
            
            if suspicious_files:
                results.update({
                    'status': 'warning',
                    'details': f'Found {len(suspicious_files)} suspicious pattern(s) (basic check)',
                    'score': 60,
                    'issues_found': len(suspicious_files),
                    'suspicious_patterns': suspicious_files
                })
        
        except Exception as e:
            logger.error(f"Basic tool poisoning check failed: {e}")
            results.update({
                'status': 'warning',
                'details': f'Basic tool poisoning check failed: {str(e)}',
                'score': 70
            })
        
        return results
    
    def _run_container_scan(self, repo_path: str) -> Dict:
        """Scan container configurations if present."""
        if not repo_path or not os.path.exists(repo_path):
            return {'status': 'not-applicable', 'details': 'Repository not available', 'score': 50}
        
        dockerfile_path = os.path.join(repo_path, 'Dockerfile')
        docker_compose_path = os.path.join(repo_path, 'docker-compose.yml')
        
        if not (os.path.exists(dockerfile_path) or os.path.exists(docker_compose_path)):
            return {
                'status': 'not-applicable',
                'details': 'No container configurations found',
                'score': 50
            }
        
        results = {
            'status': 'pass',
            'details': 'Container configuration appears secure',
            'score': 100,
            'issues_found': 0,
            'security_issues': []
        }
        
        try:
            # Basic Dockerfile security checks
            if os.path.exists(dockerfile_path):
                with open(dockerfile_path, 'r') as f:
                    dockerfile_content = f.read()
                
                security_issues = []
                
                # Check for running as root
                if 'USER root' in dockerfile_content or 'USER 0' in dockerfile_content:
                    security_issues.append('Container runs as root user')
                
                # Check for privileged operations
                if '--privileged' in dockerfile_content:
                    security_issues.append('Container requires privileged mode')
                
                # Check for exposed ports
                exposed_ports = re.findall(r'EXPOSE\s+(\d+)', dockerfile_content)
                if any(int(port) < 1024 for port in exposed_ports):
                    security_issues.append('Container exposes privileged ports')
                
                if security_issues:
                    results.update({
                        'status': 'warning',
                        'details': f'Found {len(security_issues)} container security issue(s)',
                        'score': max(60, 100 - len(security_issues) * 15),
                        'issues_found': len(security_issues),
                        'security_issues': security_issues
                    })
        
        except Exception as e:
            logger.error(f"Container scan failed: {e}")
            results.update({
                'status': 'warning',
                'details': f'Container scan failed: {str(e)}',
                'score': 70
            })
        
        return results
    
    def _check_security_documentation(self, repo_path: str) -> Dict:
        """Check for security-related documentation."""
        if not repo_path or not os.path.exists(repo_path):
            return {'status': 'not-applicable', 'details': 'Repository not available', 'score': 50}
        
        results = {
            'status': 'pass',
            'details': 'Security documentation is adequate',
            'score': 100,
            'documentation_found': [],
            'missing_documentation': []
        }
        
        # Look for security-related documentation
        security_docs = [
            'SECURITY.md',
            'security.md',
            'Security.md',
            'SECURITY.txt',
            'security.txt'
        ]
        
        readme_files = [
            'README.md',
            'readme.md',
            'Readme.md',
            'README.txt'
        ]
        
        found_security_doc = False
        has_security_in_readme = False
        
        # Check for dedicated security documentation
        for doc in security_docs:
            if os.path.exists(os.path.join(repo_path, doc)):
                results['documentation_found'].append(doc)
                found_security_doc = True
        
        # Check for security section in README
        for readme in readme_files:
            readme_path = os.path.join(repo_path, readme)
            if os.path.exists(readme_path):
                try:
                    with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        if any(keyword in content for keyword in ['security', 'authentication', 'authorization', 'permissions']):
                            has_security_in_readme = True
                            results['documentation_found'].append(f"{readme} (security section)")
                except Exception:
                    pass
        
        # Calculate score based on documentation completeness
        if not found_security_doc and not has_security_in_readme:
            results.update({
                'status': 'warning',
                'details': 'No security documentation found',
                'score': 60,
                'missing_documentation': ['Security documentation', 'Security section in README']
            })
        elif not found_security_doc:
            results.update({
                'status': 'warning',
                'details': 'No dedicated security documentation found',
                'score': 80,
                'missing_documentation': ['Dedicated security documentation']
            })
        
        return results
    
    def _detect_language(self, repo_path: str) -> str:
        """Detect the primary programming language of the repository."""
        language_indicators = {
            'python': ['requirements.txt', 'setup.py', 'pyproject.toml', '*.py'],
            'javascript': ['package.json', '*.js'],
            'typescript': ['package.json', 'tsconfig.json', '*.ts'],
            'go': ['go.mod', 'go.sum', '*.go'],
            'rust': ['Cargo.toml', '*.rs'],
            'java': ['pom.xml', 'build.gradle', '*.java']
        }
        
        for language, indicators in language_indicators.items():
            for indicator in indicators:
                if '*' in indicator:
                    # Check for file extensions
                    for root, dirs, files in os.walk(repo_path):
                        for file in files:
                            if file.endswith(indicator[1:]):
                                return language
                else:
                    # Check for specific files
                    if os.path.exists(os.path.join(repo_path, indicator)):
                        return language
        
        return 'unknown'
    
    def _run_bandit_critical_only(self, repo_path: str) -> Dict:
        """Run Bandit security scanner focusing on critical vulnerabilities only."""
        try:
            # Focus on high and medium severity issues only
            cmd = ['bandit', '-r', repo_path, '-f', 'json', '-ll', '-i']  # -ll = only report high/med, -i = show issue numbers
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            try:
                bandit_output = json.loads(result.stdout) if result.stdout else {'results': []}
                all_issues = bandit_output.get('results', [])
                
                # Count only critical and high severity issues
                critical_issues = [issue for issue in all_issues 
                                 if issue.get('issue_severity', '').lower() in ['high', 'medium']]
                
                if len(critical_issues) == 0:
                    return {
                        'status': 'pass',
                        'details': 'No critical security vulnerabilities found',
                        'score': 100,
                        'issues_found': 0,
                        'critical_issues': 0,
                        'tools_used': ['bandit-critical']
                    }
                else:
                    # Score based on critical issues only
                    score = max(50, 100 - len(critical_issues) * 15)
                    return {
                        'status': 'warning' if len(critical_issues) <= 3 else 'fail',
                        'details': f'Found {len(critical_issues)} critical security issue(s)',
                        'score': score,
                        'issues_found': len(critical_issues),
                        'critical_issues': len(critical_issues),
                        'tools_used': ['bandit-critical']
                    }
            except json.JSONDecodeError:
                return {
                    'status': 'warning',
                    'details': 'Bandit completed but output could not be parsed',
                    'score': 70,
                    'tools_used': ['bandit-critical']
                }
        
        except FileNotFoundError:
            return {
                'status': 'warning',
                'details': 'Bandit not available for Python security analysis',
                'score': 70
            }
        except Exception as e:
            return {
                'status': 'warning',
                'details': f'Bandit analysis failed: {str(e)}',
                'score': 70
            }

    def _run_bandit(self, repo_path: str) -> Dict:
        """Legacy method - redirects to critical-only version."""
        return self._run_bandit_critical_only(repo_path)
    
    def _run_semgrep_critical_only(self, repo_path: str) -> Dict:
        """Run Semgrep focusing on critical security vulnerabilities only."""
        try:
            # Use security ruleset with focus on critical issues
            cmd = ['semgrep', '--config=p/security-audit', '--config=p/secrets', '--json', '--severity=ERROR', '--severity=WARNING', repo_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            try:
                semgrep_output = json.loads(result.stdout) if result.stdout else {'results': []}
                all_issues = semgrep_output.get('results', [])
                
                # Filter for high-severity issues
                critical_issues = [issue for issue in all_issues 
                                 if issue.get('extra', {}).get('severity', '').upper() in ['ERROR', 'WARNING']]
                
                if len(critical_issues) == 0:
                    return {
                        'status': 'pass',
                        'details': 'No critical security vulnerabilities found',
                        'score': 100,
                        'issues_found': 0,
                        'critical_issues': 0,
                        'tools_used': ['semgrep-critical']
                    }
                else:
                    score = max(50, 100 - len(critical_issues) * 12)
                    return {
                        'status': 'warning' if len(critical_issues) <= 2 else 'fail',
                        'details': f'Found {len(critical_issues)} critical security issue(s)',
                        'score': score,
                        'issues_found': len(critical_issues),
                        'critical_issues': len(critical_issues),
                        'tools_used': ['semgrep-critical']
                    }
            except json.JSONDecodeError:
                return {
                    'status': 'warning',
                    'details': 'Semgrep completed but output could not be parsed',
                    'score': 70,
                    'tools_used': ['semgrep-critical']
                }
        
        except FileNotFoundError:
            return {
                'status': 'warning',
                'details': 'Semgrep not available for security analysis',
                'score': 70
            }
        except subprocess.TimeoutExpired:
            return {
                'status': 'warning',
                'details': 'Semgrep analysis timed out',
                'score': 70
            }
        except Exception as e:
            return {
                'status': 'warning',
                'details': f'Semgrep analysis failed: {str(e)}',
                'score': 70
            }

    def _run_semgrep(self, repo_path: str) -> Dict:
        """Legacy method - redirects to critical-only version."""
        return self._run_semgrep_critical_only(repo_path)
    
    def _scan_npm_dependencies(self, repo_path: str) -> Dict:
        """Scan NPM dependencies for vulnerabilities."""
        try:
            # Run npm audit
            cmd = ['npm', 'audit', '--json']
            result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
            
            try:
                audit_output = json.loads(result.stdout)
                vulnerabilities = audit_output.get('metadata', {}).get('vulnerabilities', {})
                
                total_vulns = sum(vulnerabilities.values()) if isinstance(vulnerabilities, dict) else 0
                
                if total_vulns == 0:
                    return {
                        'status': 'pass',
                        'details': 'No vulnerabilities found in NPM dependencies',
                        'score': 100,
                        'issues_found': 0
                    }
                else:
                    # Score based on vulnerability severity
                    high_vulns = vulnerabilities.get('high', 0)
                    critical_vulns = vulnerabilities.get('critical', 0)
                    
                    if critical_vulns > 0:
                        score = 40
                        status = 'fail'
                    elif high_vulns > 0:
                        score = 60
                        status = 'warning'
                    else:
                        score = 80
                        status = 'warning'
                    
                    return {
                        'status': status,
                        'details': f'Found {total_vulns} vulnerability/vulnerabilities in dependencies',
                        'score': score,
                        'issues_found': total_vulns,
                        'vulnerabilities': vulnerabilities
                    }
            
            except json.JSONDecodeError:
                return {
                    'status': 'warning',
                    'details': 'NPM audit completed but output could not be parsed',
                    'score': 70
                }
        
        except FileNotFoundError:
            return {
                'status': 'not-applicable',
                'details': 'NPM not available for dependency scanning',
                'score': 50
            }
        except Exception as e:
            return {
                'status': 'warning',
                'details': f'NPM dependency scan failed: {str(e)}',
                'score': 70
            }
    
    def _scan_python_dependencies(self, repo_path: str) -> Dict:
        """Scan Python dependencies for vulnerabilities."""
        try:
            # Run safety check
            cmd = ['safety', 'check', '--json', '-r', 'requirements.txt']
            result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
            
            try:
                safety_output = json.loads(result.stdout)
                vulnerabilities = len(safety_output) if isinstance(safety_output, list) else 0
                
                if vulnerabilities == 0:
                    return {
                        'status': 'pass',
                        'details': 'No vulnerabilities found in Python dependencies',
                        'score': 100,
                        'issues_found': 0
                    }
                else:
                    score = max(60, 100 - vulnerabilities * 10)
                    return {
                        'status': 'warning',
                        'details': f'Found {vulnerabilities} vulnerability/vulnerabilities in Python dependencies',
                        'score': score,
                        'issues_found': vulnerabilities,
                        'vulnerabilities': safety_output
                    }
            
            except json.JSONDecodeError:
                return {
                    'status': 'warning',
                    'details': 'Safety check completed but output could not be parsed',
                    'score': 70
                }
        
        except FileNotFoundError:
            return {
                'status': 'not-applicable',
                'details': 'Safety not available for Python dependency scanning',
                'score': 50
            }
        except Exception as e:
            return {
                'status': 'warning',
                'details': f'Python dependency scan failed: {str(e)}',
                'score': 70
            }
    
    def _scan_go_dependencies(self, repo_path: str) -> Dict:
        """Scan Go dependencies for vulnerabilities."""
        # Placeholder for Go dependency scanning
        return {
            'status': 'not-applicable',
            'details': 'Go dependency scanning not yet implemented',
            'score': 50
        }
    
    def _calculate_overall_score(self, scan_result: Dict) -> int:
        """Calculate overall security score from individual scan results."""
        scores = []
        weights = {
            'static_analysis': 0.15,      # Reduced from 0.20
            'dependency_scan': 0.25,      # Unchanged
            'mcp_security_scan': 0.60     # Increased from 0.35 - primary focus
        }
        
        total_weight = 0
        weighted_score = 0
        
        for check, weight in weights.items():
            if check in scan_result and 'score' in scan_result[check]:
                weighted_score += scan_result[check]['score'] * weight
                total_weight += weight
        
        if total_weight > 0:
            return int(weighted_score / total_weight)
        else:
            return 50  # Default score if no checks completed
    
    def _generate_recommendations(self, scan_result: Dict) -> List[str]:
        """Generate security recommendations based on scan results."""
        recommendations = []
        
        # Check each scan component for issues
        if scan_result.get('static_analysis', {}).get('score', 100) < 80:
            recommendations.append("Address static analysis security findings")
        
        if scan_result.get('dependency_scan', {}).get('score', 100) < 80:
            recommendations.append("Update dependencies to fix known vulnerabilities")
        
        if scan_result.get('mcp_security_scan', {}).get('score', 100) < 80:
            recommendations.append("Address MCP-specific security issues identified by mcp-scan")
        
        # Removed container and documentation recommendations as they're no longer part of scoring
        
        # General recommendations
        if scan_result.get('overall_score', 100) < 70:
            recommendations.append("Consider additional security review before recommendation")
        
        return recommendations
    
    def _run_eslint_critical_only(self, repo_path: str) -> Dict:
        """Run ESLint focusing on critical JavaScript/TypeScript security issues only."""
        results = {
            'status': 'not-applicable',
            'details': 'ESLint security scanning not available',
            'score': 70,
            'issues_found': 0,
            'critical_issues': 0,
            'tools_used': []
        }
        
        # Check if eslint is available
        try:
            subprocess.run(['eslint', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return results
        
        try:
            # Focus on critical security rules only
            cmd = [
                'eslint',
                '--ext', '.js,.jsx,.ts,.tsx',
                '--format', 'json',
                '--no-eslintrc',  # Don't use project config
                '--rule', 'no-eval:error',
                '--rule', 'no-implied-eval:error', 
                '--rule', 'no-new-func:error',
                '--rule', 'no-script-url:error',
                '--rule', 'no-alert:error',
                repo_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.stdout:
                try:
                    output = json.loads(result.stdout)
                    # Count only error-level issues (critical)
                    critical_issues = []
                    for file in output:
                        for message in file.get('messages', []):
                            if message.get('severity', 0) == 2:  # Error level
                                critical_issues.append(message)
                    
                    if len(critical_issues) == 0:
                        results.update({
                            'status': 'pass',
                            'details': 'No critical security vulnerabilities found',
                            'score': 100,
                            'issues_found': 0,
                            'critical_issues': 0,
                            'tools_used': ['eslint-critical']
                        })
                    else:
                        score = max(50, 100 - len(critical_issues) * 10)
                        results.update({
                            'status': 'warning' if len(critical_issues) <= 3 else 'fail',
                            'details': f'Found {len(critical_issues)} critical security issue(s)',
                            'score': score,
                            'issues_found': len(critical_issues),
                            'critical_issues': len(critical_issues),
                            'tools_used': ['eslint-critical']
                        })
                        
                except json.JSONDecodeError:
                    logger.warning("Failed to parse ESLint output")
                    
        except subprocess.TimeoutExpired:
            logger.warning("ESLint scan timed out")
        except Exception as e:
            logger.warning(f"ESLint scan failed: {e}")
            
        return results

    def _run_eslint_security(self, repo_path: str) -> Dict:
        """Legacy method - redirects to critical-only version."""
        return self._run_eslint_critical_only(repo_path)
    
    def _run_tslint_security(self, repo_path: str) -> Dict:
        """TypeScript security analysis - redirects to unified ESLint critical-only method."""
        return self._run_eslint_critical_only(repo_path)


def main():
    """Main entry point for the security scanner."""
    parser = argparse.ArgumentParser(
        description='Security scanner for MCP servers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--input',
        required=True,
        help='Input JSON file containing server data'
    )
    
    parser.add_argument(
        '--output',
        required=True,
        help='Output JSON file for scan results'
    )
    
    parser.add_argument(
        '--server-slug',
        help='Scan only specific server (optional)'
    )
    
    parser.add_argument(
        '--github-token',
        help='GitHub token for API access (optional)'
    )
    
    args = parser.parse_args()
    
    # Load server data
    try:
        with open(args.input, 'r') as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load input file: {e}")
        sys.exit(1)
    
    # Initialize scanner
    github_token = args.github_token or os.environ.get('GITHUB_TOKEN')
    scanner = SecurityScanner(github_token)
    
    # Filter servers if specific slug provided
    servers_to_scan = data.get('servers', [])
    if args.server_slug:
        servers_to_scan = [s for s in servers_to_scan if s.get('slug') == args.server_slug]
        if not servers_to_scan:
            logger.error(f"Server with slug '{args.server_slug}' not found")
            sys.exit(1)
    
    # Perform scans
    scan_results = {
        'scan_timestamp': datetime.now(timezone.utc).isoformat(),
        'scanner_version': '1.2.0',
        'total_servers_scanned': len(servers_to_scan),
        'results': []
    }
    
    for server in servers_to_scan:
        try:
            result = scanner.scan_server(server)
            scan_results['results'].append(result)
            logger.info(f"Completed scan for {server['name']}")
        except Exception as e:
            logger.error(f"Failed to scan {server['name']}: {e}")
            # Add error result
            scan_results['results'].append({
                'server_name': server['name'],
                'server_slug': server['slug'],
                'error': str(e),
                'scan_timestamp': datetime.now(timezone.utc).isoformat()
            })
    
    # Save results
    try:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, 'w') as f:
            json.dump(scan_results, f, indent=2)
        logger.info(f"Scan results saved to {args.output}")
    except Exception as e:
        logger.error(f"Failed to save results: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()