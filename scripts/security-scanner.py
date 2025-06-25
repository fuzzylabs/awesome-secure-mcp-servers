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
            'container_scan': self._run_container_scan(repo_path),
            'security_documentation_check': self._check_security_documentation(repo_path),
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
        """Run static code analysis tools."""
        if not repo_path or not os.path.exists(repo_path):
            return {'status': 'not-applicable', 'details': 'Repository not available', 'score': 50}
        
        results = {
            'status': 'pass',
            'details': '',
            'score': 100,
            'issues_found': 0,
            'tools_used': []
        }
        
        # Detect programming language
        language = self._detect_language(repo_path)
        
        try:
            if language == 'python':
                results.update(self._run_bandit(repo_path))
            elif language == 'javascript':
                results.update(self._run_eslint_security(repo_path))
            elif language == 'typescript':
                results.update(self._run_tslint_security(repo_path))
            else:
                # Run generic security analysis
                results.update(self._run_semgrep(repo_path))
            
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
            # Run mcp-scan on found configuration files
            for config_file in mcp_config_files:
                cmd = ['uvx', 'mcp-scan@latest', 'scan', '--json', '--local-only', config_file]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    try:
                        scan_output = json.loads(result.stdout)
                        
                        # Parse mcp-scan results
                        if 'results' in scan_output:
                            config_results = scan_output['results']
                            issues_found = 0
                            critical_issues = 0
                            
                            # Count security issues
                            for result_item in config_results:
                                if 'security_issues' in result_item:
                                    issues = result_item['security_issues']
                                    issues_found += len(issues)
                                    critical_issues += sum(1 for issue in issues 
                                                         if issue.get('severity') in ['critical', 'high'])
                            
                            results['scan_results'][config_file] = {
                                'total_issues': issues_found,
                                'critical_issues': critical_issues,
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
            
            # Calculate overall score based on total issues found
            total_issues = results['issues_found']
            if total_issues == 0:
                results.update({
                    'status': 'pass',
                    'details': f'MCP-scan found no security issues in {len(mcp_config_files)} configuration file(s)',
                    'score': 95
                })
            elif total_issues <= 2:
                results.update({
                    'status': 'warning',
                    'details': f'MCP-scan found {total_issues} security issue(s) in configuration files',
                    'score': 80
                })
            else:
                results.update({
                    'status': 'warning',
                    'details': f'MCP-scan found {total_issues} security issue(s) in configuration files',
                    'score': max(60, 90 - total_issues * 10)
                })
        
        except subprocess.TimeoutExpired:
            results.update({
                'status': 'warning',
                'details': 'MCP-scan timed out',
                'score': 70
            })
        except FileNotFoundError:
            # Fall back to basic tool poisoning detection if mcp-scan not available
            logger.warning("uvx or mcp-scan not found, falling back to basic tool poisoning detection")
            return self._basic_tool_poisoning_check(repo_path)
        except Exception as e:
            logger.error(f"MCP-scan failed: {e}")
            # Fall back to basic tool poisoning detection
            return self._basic_tool_poisoning_check(repo_path)
        
        return results
    
    def _find_mcp_configs(self, repo_path: str) -> List[str]:
        """Find MCP configuration files in the repository."""
        config_files = []
        
        # Common MCP configuration file patterns
        config_patterns = [
            'mcp.json',
            'mcp_config.json',
            '.mcp.json',
            'config/mcp.json',
            'configs/mcp.json',
            '*.mcp.json',
            'claude_desktop_config.json',
            '.claude/config.json'
        ]
        
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, repo_path)
                
                # Check if file matches any config pattern
                for pattern in config_patterns:
                    if pattern.startswith('*'):
                        # Handle wildcard patterns
                        if file.endswith(pattern[1:]):
                            config_files.append(file_path)
                            break
                    elif file == pattern or relative_path == pattern:
                        config_files.append(file_path)
                        break
                    elif file.endswith('.json') and 'mcp' in file.lower():
                        # Additional heuristic for MCP-related JSON files
                        config_files.append(file_path)
                        break
        
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
    
    def _run_bandit(self, repo_path: str) -> Dict:
        """Run Bandit security scanner for Python code."""
        try:
            cmd = ['bandit', '-r', repo_path, '-f', 'json']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    'status': 'pass',
                    'details': 'Bandit found no security issues',
                    'score': 100,
                    'issues_found': 0,
                    'tools_used': ['bandit']
                }
            else:
                # Parse bandit output for issues
                try:
                    bandit_output = json.loads(result.stdout)
                    issues = len(bandit_output.get('results', []))
                    
                    if issues == 0:
                        status = 'pass'
                        score = 100
                    elif issues <= 5:
                        status = 'warning'
                        score = 80
                    else:
                        status = 'warning'
                        score = 60
                    
                    return {
                        'status': status,
                        'details': f'Bandit found {issues} potential security issue(s)',
                        'score': score,
                        'issues_found': issues,
                        'tools_used': ['bandit']
                    }
                except json.JSONDecodeError:
                    return {
                        'status': 'warning',
                        'details': 'Bandit completed but output could not be parsed',
                        'score': 70,
                        'tools_used': ['bandit']
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
    
    def _run_semgrep(self, repo_path: str) -> Dict:
        """Run Semgrep for generic security analysis."""
        try:
            cmd = ['semgrep', '--config=auto', '--json', repo_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            try:
                semgrep_output = json.loads(result.stdout)
                issues = len(semgrep_output.get('results', []))
                
                if issues == 0:
                    status = 'pass'
                    score = 100
                elif issues <= 3:
                    status = 'warning'
                    score = 85
                else:
                    status = 'warning'
                    score = 70
                
                return {
                    'status': status,
                    'details': f'Semgrep found {issues} potential security issue(s)',
                    'score': score,
                    'issues_found': issues,
                    'tools_used': ['semgrep']
                }
            except json.JSONDecodeError:
                return {
                    'status': 'warning',
                    'details': 'Semgrep completed but output could not be parsed',
                    'score': 70,
                    'tools_used': ['semgrep']
                }
        
        except FileNotFoundError:
            return {
                'status': 'warning',
                'details': 'Semgrep not available for security analysis',
                'score': 70
            }
        except Exception as e:
            return {
                'status': 'warning',
                'details': f'Semgrep analysis failed: {str(e)}',
                'score': 70
            }
    
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
            'static_analysis': 0.20,
            'dependency_scan': 0.25,
            'mcp_security_scan': 0.35,  # Higher weight for MCP-specific security
            'container_scan': 0.10,
            'security_documentation_check': 0.10
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
        
        if scan_result.get('container_scan', {}).get('score', 100) < 80:
            recommendations.append("Improve container security configuration")
        
        if scan_result.get('security_documentation_check', {}).get('score', 100) < 80:
            recommendations.append("Add comprehensive security documentation")
        
        # General recommendations
        if scan_result.get('overall_score', 100) < 70:
            recommendations.append("Consider additional security review before recommendation")
        
        return recommendations
    
    def _run_eslint_security(self, repo_path: str) -> Dict:
        """Run ESLint security analysis for JavaScript."""
        results = {
            'status': 'not-applicable',
            'details': 'ESLint security scanning not available',
            'score': 70,
            'issues_found': 0,
            'tools_used': []
        }
        
        # Check if eslint is available
        try:
            subprocess.run(['eslint', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return results
        
        try:
            # Run eslint with basic security rules
            cmd = [
                'eslint',
                '--format', 'json',
                '--no-eslintrc',  # Don't use project config
                '--rule', 'no-eval:error',
                '--rule', 'no-implied-eval:error', 
                '--rule', 'no-new-func:error',
                repo_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.stdout:
                try:
                    output = json.loads(result.stdout)
                    total_issues = sum(len(file.get('messages', [])) for file in output)
                    
                    if total_issues > 0:
                        results.update({
                            'status': 'warning',
                            'details': f'ESLint found {total_issues} potential security issue(s)',
                            'score': max(50, 90 - total_issues * 5),
                            'issues_found': total_issues,
                            'tools_used': ['eslint']
                        })
                    else:
                        results.update({
                            'status': 'pass',
                            'details': 'No security issues found by ESLint',
                            'score': 85,
                            'issues_found': 0,
                            'tools_used': ['eslint']
                        })
                        
                except json.JSONDecodeError:
                    logger.warning("Failed to parse ESLint output")
                    
        except subprocess.TimeoutExpired:
            logger.warning("ESLint scan timed out")
        except Exception as e:
            logger.warning(f"ESLint scan failed: {e}")
            
        return results
    
    def _run_tslint_security(self, repo_path: str) -> Dict:
        """Run TypeScript security analysis."""
        results = {
            'status': 'not-applicable',
            'details': 'TypeScript security scanning not available',
            'score': 70,
            'issues_found': 0,
            'tools_used': []
        }
        
        # Try ESLint with TypeScript support
        try:
            subprocess.run(['eslint', '--version'], capture_output=True, check=True)
            
            cmd = [
                'eslint',
                '--ext', '.ts,.tsx',
                '--format', 'json',
                '--no-eslintrc',
                '--rule', 'no-eval:error',
                '--rule', 'no-implied-eval:error',
                repo_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.stdout:
                try:
                    output = json.loads(result.stdout)
                    total_issues = sum(len(file.get('messages', [])) for file in output)
                    
                    if total_issues > 0:
                        results.update({
                            'status': 'warning',
                            'details': f'TypeScript analysis found {total_issues} potential security issue(s)',
                            'score': max(50, 90 - total_issues * 5),
                            'issues_found': total_issues,
                            'tools_used': ['eslint-typescript']
                        })
                    else:
                        results.update({
                            'status': 'pass',
                            'details': 'No security issues found in TypeScript analysis',
                            'score': 85,
                            'issues_found': 0,
                            'tools_used': ['eslint-typescript']
                        })
                        
                except json.JSONDecodeError:
                    logger.warning("Failed to parse TypeScript analysis output")
                    
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to Semgrep if ESLint not available
            return self._run_semgrep(repo_path)
        except subprocess.TimeoutExpired:
            logger.warning("TypeScript analysis timed out")
        except Exception as e:
            logger.warning(f"TypeScript analysis failed: {e}")
            
        return results


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