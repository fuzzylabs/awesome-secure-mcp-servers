#!/usr/bin/env python3
"""
Automated MCP Server Discovery System
=====================================

This script automatically discovers new MCP servers from various sources:
- GitHub search for MCP-related repositories
- NPM registry for MCP packages
- PyPI for MCP packages
- Popular awesome lists and collections

Usage:
    python server-discovery.py --output discovered-servers.json --limit 50
"""

import argparse
import json
import logging
import requests
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional
from urllib.parse import urlparse
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MCPServerDiscovery:
    """Automated discovery system for MCP servers."""
    
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        self.session = requests.Session()
        if github_token:
            self.session.headers.update({
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json'
            })
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 second between requests
    
    def _rate_limit(self):
        """Implement rate limiting for API requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        self.last_request_time = time.time()
    
    def discover_servers(self, limit: int = 50) -> List[Dict]:
        """Discover MCP servers from multiple sources."""
        discovered = []
        
        logger.info("Starting MCP server discovery process...")
        
        # GitHub discovery
        try:
            github_servers = self._discover_github_servers(limit // 3)
            discovered.extend(github_servers)
            logger.info(f"Discovered {len(github_servers)} servers from GitHub")
        except Exception as e:
            logger.error(f"GitHub discovery failed: {e}")
        
        # NPM discovery
        try:
            npm_servers = self._discover_npm_servers(limit // 3)
            discovered.extend(npm_servers)
            logger.info(f"Discovered {len(npm_servers)} servers from NPM")
        except Exception as e:
            logger.error(f"NPM discovery failed: {e}")
        
        # PyPI discovery
        try:
            pypi_servers = self._discover_pypi_servers(limit // 3)
            discovered.extend(pypi_servers)
            logger.info(f"Discovered {len(pypi_servers)} servers from PyPI")
        except Exception as e:
            logger.error(f"PyPI discovery failed: {e}")
        
        # Awesome lists discovery
        try:
            awesome_servers = self._discover_awesome_lists()
            discovered.extend(awesome_servers)
            logger.info(f"Discovered {len(awesome_servers)} servers from awesome lists")
        except Exception as e:
            logger.error(f"Awesome lists discovery failed: {e}")
        
        # Deduplicate and rank
        unique_servers = self._deduplicate_servers(discovered)
        ranked_servers = self._rank_servers(unique_servers)
        
        logger.info(f"Total unique servers discovered: {len(ranked_servers)}")
        return ranked_servers[:limit]
    
    def _discover_github_servers(self, limit: int) -> List[Dict]:
        """Discover MCP servers from GitHub search."""
        servers = []
        
        # Search queries for MCP-related repositories
        search_queries = [
            "mcp-server language:python",
            "mcp-server language:typescript", 
            "mcp-server language:javascript",
            "model-context-protocol server",
            "mcp server",
            "anthropic mcp",
            "claude mcp server"
        ]
        
        for query in search_queries:
            self._rate_limit()
            
            try:
                response = self.session.get(
                    'https://api.github.com/search/repositories',
                    params={
                        'q': query,
                        'sort': 'stars',
                        'order': 'desc',
                        'per_page': limit // len(search_queries)
                    }
                )
                response.raise_for_status()
                
                search_results = response.json()
                
                for repo in search_results.get('items', []):
                    server_info = self._extract_github_server_info(repo)
                    if server_info:
                        servers.append(server_info)
                        
            except Exception as e:
                logger.warning(f"GitHub search failed for query '{query}': {e}")
                continue
        
        return servers
    
    def _extract_github_server_info(self, repo: Dict) -> Optional[Dict]:
        """Extract server information from GitHub repository data."""
        try:
            # Skip forks and archived repositories
            if repo.get('fork', False) or repo.get('archived', False):
                return None
            
            # Look for MCP indicators in name, description, or topics
            name = repo.get('name', '').lower()
            description = repo.get('description', '').lower() if repo.get('description') else ''
            topics = [t.lower() for t in repo.get('topics', [])]
            
            mcp_indicators = ['mcp', 'model-context-protocol', 'claude', 'anthropic']
            server_indicators = ['server', 'tool', 'integration']
            
            has_mcp = any(indicator in name or indicator in description for indicator in mcp_indicators)
            has_server = any(indicator in name or indicator in description for indicator in server_indicators)
            has_mcp_topic = any(indicator in topics for indicator in mcp_indicators)
            
            if not (has_mcp and (has_server or has_mcp_topic)):
                return None
            
            # Extract version information (basic)
            latest_version = self._get_latest_github_version(repo['full_name'])
            
            return {
                'name': repo['name'],
                'repository': repo['html_url'],
                'description': repo.get('description', ''),
                'stars': repo.get('stargazers_count', 0),
                'forks': repo.get('forks_count', 0),
                'language': repo.get('language', 'unknown'),
                'topics': repo.get('topics', []),
                'updated_at': repo.get('updated_at'),
                'latest_version': latest_version,
                'source': 'github',
                'maintainer': {
                    'name': repo['owner']['login'],
                    'type': 'organization' if repo['owner']['type'] == 'Organization' else 'individual',
                    'contact': repo['owner']['html_url']
                }
            }
            
        except Exception as e:
            logger.warning(f"Failed to extract info from GitHub repo: {e}")
            return None
    
    def _get_latest_github_version(self, repo_full_name: str) -> Optional[str]:
        """Get the latest release version from GitHub."""
        try:
            self._rate_limit()
            response = self.session.get(
                f'https://api.github.com/repos/{repo_full_name}/releases/latest'
            )
            
            if response.status_code == 200:
                release = response.json()
                tag_name = release.get('tag_name', '')
                # Clean up version tag (remove 'v' prefix if present)
                return tag_name.lstrip('v') if tag_name else None
            return None
            
        except Exception:
            return None
    
    def _discover_npm_servers(self, limit: int) -> List[Dict]:
        """Discover MCP servers from NPM registry."""
        servers = []
        
        search_terms = ['mcp-server', 'model-context-protocol', 'claude-mcp', 'anthropic-mcp']
        
        for term in search_terms:
            try:
                response = requests.get(
                    'https://registry.npmjs.org/-/v1/search',
                    params={
                        'text': term,
                        'size': limit // len(search_terms),
                        'quality': 0.65,
                        'popularity': 0.98,
                        'maintenance': 0.5
                    }
                )
                response.raise_for_status()
                
                search_results = response.json()
                
                for package in search_results.get('objects', []):
                    server_info = self._extract_npm_server_info(package)
                    if server_info:
                        servers.append(server_info)
                        
            except Exception as e:
                logger.warning(f"NPM search failed for term '{term}': {e}")
                continue
        
        return servers
    
    def _extract_npm_server_info(self, package: Dict) -> Optional[Dict]:
        """Extract server information from NPM package data."""
        try:
            pkg = package.get('package', {})
            
            # Skip packages that don't look like MCP servers
            name = pkg.get('name', '').lower()
            description = pkg.get('description', '').lower()
            keywords = [k.lower() for k in pkg.get('keywords', [])]
            
            if not any(term in name or term in description or term in keywords 
                      for term in ['mcp', 'model-context-protocol']):
                return None
            
            # Get repository URL
            repo_url = None
            if pkg.get('links', {}).get('repository'):
                repo_url = pkg['links']['repository']
            elif pkg.get('repository', {}).get('url'):
                repo_url = pkg['repository']['url']
            
            return {
                'name': pkg.get('name'),
                'repository': repo_url,
                'description': pkg.get('description', ''),
                'npm_downloads': pkg.get('downloads', {}).get('weekly', 0),
                'version': pkg.get('version'),
                'language': 'javascript',
                'keywords': pkg.get('keywords', []),
                'updated_at': pkg.get('date'),
                'source': 'npm',
                'maintainer': {
                    'name': pkg.get('publisher', {}).get('username', 'unknown'),
                    'type': 'individual',  # NPM doesn't distinguish clearly
                    'contact': f"https://npmjs.com/~{pkg.get('publisher', {}).get('username', '')}"
                }
            }
            
        except Exception as e:
            logger.warning(f"Failed to extract info from NPM package: {e}")
            return None
    
    def _discover_pypi_servers(self, limit: int) -> List[Dict]:
        """Discover MCP servers from PyPI."""
        servers = []
        
        search_terms = ['mcp-server', 'model-context-protocol', 'claude-mcp', 'anthropic-mcp']
        
        for term in search_terms:
            try:
                # PyPI doesn't have a great search API, so we'll use a basic approach
                response = requests.get(
                    f'https://pypi.org/search/?q={term}&o=&c=Programming+Language+%3A%3A+Python'
                )
                
                # This is a simplified approach - in practice, we'd need to parse HTML
                # For now, we'll focus on known MCP server packages
                
                known_packages = [
                    'mcp-server-git',
                    'mcp-server-filesystem', 
                    'mcp-server-fetch',
                    'mcp-server-time',
                    'anthropic-mcp-server'
                ]
                
                for package_name in known_packages:
                    if term in package_name:
                        server_info = self._get_pypi_package_info(package_name)
                        if server_info:
                            servers.append(server_info)
                            
            except Exception as e:
                logger.warning(f"PyPI search failed for term '{term}': {e}")
                continue
        
        return servers
    
    def _get_pypi_package_info(self, package_name: str) -> Optional[Dict]:
        """Get information about a PyPI package."""
        try:
            response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
            if response.status_code != 200:
                return None
                
            data = response.json()
            info = data.get('info', {})
            
            return {
                'name': info.get('name'),
                'repository': info.get('home_page') or info.get('project_url'),
                'description': info.get('summary', ''),
                'version': info.get('version'),
                'language': 'python',
                'keywords': info.get('keywords', '').split(',') if info.get('keywords') else [],
                'updated_at': data.get('last_serial'),  # This isn't a great timestamp
                'source': 'pypi',
                'maintainer': {
                    'name': info.get('author', 'unknown'),
                    'type': 'individual',
                    'contact': info.get('author_email', '')
                }
            }
            
        except Exception as e:
            logger.warning(f"Failed to get PyPI package info for {package_name}: {e}")
            return None
    
    def _discover_awesome_lists(self) -> List[Dict]:
        """Discover servers from awesome-mcp-servers and similar lists."""
        servers = []
        
        awesome_lists = [
            'https://raw.githubusercontent.com/wong2/awesome-mcp-servers/main/README.md',
            'https://raw.githubusercontent.com/modelcontextprotocol/servers/main/README.md'
        ]
        
        for list_url in awesome_lists:
            try:
                response = requests.get(list_url)
                response.raise_for_status()
                
                # Parse markdown for GitHub repository links
                content = response.text
                github_pattern = r'https://github\.com/([^/]+/[^/)]+)'
                matches = re.findall(github_pattern, content)
                
                for match in matches:
                    if 'mcp' in match.lower():
                        repo_url = f'https://github.com/{match}'
                        server_info = {
                            'name': match.split('/')[-1],
                            'repository': repo_url,
                            'source': 'awesome-list',
                            'maintainer': {
                                'name': match.split('/')[0],
                                'type': 'organization',
                                'contact': f'https://github.com/{match.split("/")[0]}'
                            }
                        }
                        servers.append(server_info)
                        
            except Exception as e:
                logger.warning(f"Failed to process awesome list {list_url}: {e}")
                continue
        
        return servers
    
    def _deduplicate_servers(self, servers: List[Dict]) -> List[Dict]:
        """Remove duplicate servers based on repository URL."""
        seen_repos = set()
        unique_servers = []
        
        for server in servers:
            repo_url = server.get('repository')
            if repo_url and repo_url not in seen_repos:
                seen_repos.add(repo_url)
                unique_servers.append(server)
        
        return unique_servers
    
    def _rank_servers(self, servers: List[Dict]) -> List[Dict]:
        """Rank servers by popularity and quality indicators."""
        def calculate_score(server):
            score = 0
            
            # GitHub stars (if available)
            stars = server.get('stars', 0)
            score += min(stars / 10, 50)  # Max 50 points for stars
            
            # NPM downloads (if available)
            downloads = server.get('npm_downloads', 0)
            score += min(downloads / 100, 30)  # Max 30 points for downloads
            
            # Recent activity (if available)
            if server.get('updated_at'):
                try:
                    from datetime import datetime
                    updated = datetime.fromisoformat(server['updated_at'].replace('Z', '+00:00'))
                    days_old = (datetime.now(timezone.utc) - updated).days
                    recency_score = max(0, 20 - (days_old / 30))  # Max 20 points, decreasing over time
                    score += recency_score
                except Exception:
                    pass
            
            # Official/enterprise maintainers
            maintainer_type = server.get('maintainer', {}).get('type', '')
            if maintainer_type == 'organization':
                score += 15
            
            # Language preference (TypeScript/Python preferred for MCP)
            language = server.get('language', '').lower()
            if language in ['typescript', 'python']:
                score += 10
            elif language in ['javascript']:
                score += 5
            
            return score
        
        # Sort by calculated score
        ranked = sorted(servers, key=calculate_score, reverse=True)
        
        # Add ranking score to each server
        for i, server in enumerate(ranked):
            server['discovery_score'] = calculate_score(server)
            server['discovery_rank'] = i + 1
        
        return ranked

def main():
    parser = argparse.ArgumentParser(
        description='Discover new MCP servers automatically',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--output',
        required=True,
        help='Output JSON file for discovered servers'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=50,
        help='Maximum number of servers to discover (default: 50)'
    )
    
    parser.add_argument(
        '--github-token',
        help='GitHub token for API access (optional but recommended)'
    )
    
    args = parser.parse_args()
    
    # Initialize discovery system
    discovery = MCPServerDiscovery(github_token=args.github_token)
    
    # Discover servers
    discovered_servers = discovery.discover_servers(limit=args.limit)
    
    # Save results
    output_data = {
        'discovery_timestamp': datetime.now(timezone.utc).isoformat(),
        'total_discovered': len(discovered_servers),
        'discovery_sources': ['github', 'npm', 'pypi', 'awesome-lists'],
        'servers': discovered_servers
    }
    
    with open(args.output, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    logger.info(f"Discovery complete! Found {len(discovered_servers)} servers")
    logger.info(f"Results saved to {args.output}")

if __name__ == '__main__':
    main()