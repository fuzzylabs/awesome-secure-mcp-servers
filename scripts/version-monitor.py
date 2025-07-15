#!/usr/bin/env python3
"""
Version Monitor - Monitor MCP servers for new versions
"""
import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Dict, List, Optional

import requests
from github import Github
from packaging import version
from packaging.version import InvalidVersion

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VersionMonitor:
    """Monitor MCP servers for new versions"""
    
    def __init__(self, github_token: str):
        self.github = Github(github_token)
        self.github_token = github_token
        
    def get_latest_version(self, repo_url: str) -> Optional[Dict]:
        """Get the latest version from a GitHub repository"""
        try:
            # Extract owner/repo from URL
            if 'github.com' not in repo_url:
                return None
                
            parts = repo_url.replace('https://github.com/', '').replace('.git', '').split('/')
            if len(parts) < 2:
                return None
                
            owner, repo = parts[0], parts[1]
            
            # Get repository
            repository = self.github.get_repo(f"{owner}/{repo}")
            
            # Get latest release
            try:
                latest_release = repository.get_latest_release()
                return {
                    'version': latest_release.tag_name.lstrip('v'),
                    'release_date': latest_release.published_at.isoformat(),
                    'url': latest_release.html_url
                }
            except Exception:
                # If no releases, try to get latest tag
                try:
                    tags = repository.get_tags()
                    if tags.totalCount > 0:
                        latest_tag = tags[0]
                        return {
                            'version': latest_tag.name.lstrip('v'),
                            'release_date': latest_tag.commit.commit.author.date.isoformat(),
                            'url': f"{repo_url}/releases/tag/{latest_tag.name}"
                        }
                except Exception:
                    pass
                    
            return None
            
        except Exception as e:
            logger.warning(f"Error getting latest version for {repo_url}: {e}")
            return None
    
    def compare_versions(self, current: str, latest: str) -> bool:
        """Compare two versions, return True if latest is newer"""
        try:
            return version.parse(latest) > version.parse(current)
        except InvalidVersion:
            # Fallback to string comparison
            return latest != current
    
    def check_for_new_versions(self, servers_data: Dict, force_scan: bool = False) -> List[Dict]:
        """Check all servers for new versions"""
        new_versions = []
        
        for server in servers_data.get('servers', []):
            logger.info(f"Checking versions for {server['name']}")
            
            # Get current version (latest in versions list)
            if not server.get('versions'):
                continue
                
            current_version_entry = server['versions'][0]  # Assume first is latest
            current_version = current_version_entry['version']
            
            # Get latest version from repository
            latest_info = self.get_latest_version(server['repository'])
            if not latest_info:
                logger.warning(f"Could not determine latest version for {server['name']}")
                continue
                
            latest_version = latest_info['version']
            
            # Check if we have a new version
            if self.compare_versions(current_version, latest_version):
                logger.info(f"New version found for {server['name']}: {current_version} -> {latest_version}")
                
                new_versions.append({
                    'server': server['name'],
                    'slug': server['slug'],
                    'repository': server['repository'],
                    'previous_version': current_version,
                    'version': latest_version,
                    'release_date': latest_info['release_date'],
                    'release_url': latest_info['url']
                })
            else:
                logger.info(f"No new version for {server['name']} (current: {current_version})")
        
        return new_versions
    
    def save_new_versions(self, new_versions: List[Dict], output_file: str):
        """Save new versions to output file"""
        if new_versions:
            with open(output_file, 'w') as f:
                json.dump(new_versions, f, indent=2)
            logger.info(f"Saved {len(new_versions)} new versions to {output_file}")
        else:
            logger.info("No new versions found")


def main():
    parser = argparse.ArgumentParser(description='Monitor MCP servers for new versions')
    parser.add_argument('--servers', required=True, help='Path to servers.json file')
    parser.add_argument('--output', required=True, help='Output file for new versions')
    parser.add_argument('--force-scan', action='store_true', help='Force scan all servers')
    
    args = parser.parse_args()
    
    # Get GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        logger.error("GITHUB_TOKEN environment variable is required")
        sys.exit(1)
    
    # Load servers data
    try:
        with open(args.servers, 'r') as f:
            servers_data = json.load(f)
    except Exception as e:
        logger.error(f"Error loading servers data: {e}")
        sys.exit(1)
    
    # Initialize monitor
    monitor = VersionMonitor(github_token)
    
    # Check for new versions
    new_versions = monitor.check_for_new_versions(servers_data, args.force_scan)
    
    # Save results
    monitor.save_new_versions(new_versions, args.output)
    
    logger.info(f"Version monitoring complete. Found {len(new_versions)} new versions.")


if __name__ == '__main__':
    main()