#!/usr/bin/env python3
"""
Process Discovered Servers
===========================

This script processes the output from server-discovery.py and determines
which servers should be added to the database.

Usage:
    python process-discovered-servers.py --discovered discovered.json --existing servers.json --output candidates.json
"""

import argparse
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_discovered_servers(discovered_file: str, existing_file: str, output_file: str):
    """Process discovered servers and generate candidates for addition."""
    
    # Load discovered servers
    with open(discovered_file, 'r') as f:
        discovered_data = json.load(f)
    
    # Load existing servers
    with open(existing_file, 'r') as f:
        existing_data = json.load(f)
    
    discovered_servers = discovered_data.get('servers', [])
    existing_servers = existing_data.get('servers', [])
    
    logger.info(f"Processing {len(discovered_servers)} discovered servers")
    logger.info(f"Comparing against {len(existing_servers)} existing servers")
    
    # Get existing repository URLs for deduplication
    existing_repos = set()
    for server in existing_servers:
        if server.get('repository'):
            existing_repos.add(normalize_repo_url(server['repository']))
    
    # Filter and rank new servers
    new_servers = []
    for server in discovered_servers:
        if should_include_server(server, existing_repos):
            candidate = convert_to_server_format(server)
            if candidate:
                new_servers.append(candidate)
    
    logger.info(f"Found {len(new_servers)} new server candidates")
    
    # Update the servers data
    updated_servers_data = existing_data.copy()
    updated_servers_data['servers'].extend(new_servers)
    updated_servers_data['last_updated'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Prepare output
    output_data = {
        'processing_timestamp': datetime.now(timezone.utc).isoformat(),
        'total_discovered': len(discovered_servers),
        'total_existing': len(existing_servers),
        'new_candidates': len(new_servers),
        'new_servers': new_servers,
        'updated_servers': updated_servers_data
    }
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    logger.info(f"Processing complete. Results saved to {output_file}")

def normalize_repo_url(url: str) -> str:
    """Normalize repository URL for comparison."""
    if not url:
        return ""
    
    # Remove trailing slashes and .git extensions
    normalized = url.rstrip('/').rstrip('.git')
    
    # Convert to lowercase for comparison
    return normalized.lower()

def should_include_server(server: Dict, existing_repos: set) -> bool:
    """Determine if a discovered server should be included."""
    
    # Check if already exists
    repo_url = normalize_repo_url(server.get('repository', ''))
    if repo_url in existing_repos:
        return False
    
    # Minimum quality thresholds
    min_discovery_score = 10  # Minimum discovery score
    min_stars = 5  # Minimum GitHub stars (if available)
    
    discovery_score = server.get('discovery_score', 0)
    stars = server.get('stars', 0)
    
    if discovery_score < min_discovery_score:
        logger.debug(f"Excluding {server.get('name')} - low discovery score: {discovery_score}")
        return False
    
    if stars is not None and stars < min_stars and server.get('source') == 'github':
        logger.debug(f"Excluding {server.get('name')} - insufficient stars: {stars}")
        return False
    
    # Check for required fields
    if not server.get('name') or not server.get('repository'):
        logger.debug(f"Excluding server - missing required fields")
        return False
    
    # Exclude obvious test/demo repositories
    name = server.get('name', '').lower()
    description = server.get('description', '').lower()
    
    exclude_patterns = [
        'test', 'demo', 'example', 'template', 'boilerplate',
        'tutorial', 'learning', 'practice', 'experiment'
    ]
    
    for pattern in exclude_patterns:
        if pattern in name or pattern in description:
            logger.debug(f"Excluding {server.get('name')} - appears to be {pattern}")
            return False
    
    return True

def convert_to_server_format(discovered_server: Dict) -> Optional[Dict]:
    """Convert discovered server to our database format."""
    try:
        name = discovered_server.get('name', '').strip()
        if not name:
            return None
        
        # Generate a slug from the name
        slug = re.sub(r'[^a-zA-Z0-9-]', '-', name.lower()).strip('-')
        slug = re.sub(r'-+', '-', slug)  # Remove multiple consecutive dashes
        
        # Determine category based on maintainer and characteristics
        maintainer = discovered_server.get('maintainer', {})
        category = determine_category(discovered_server, maintainer)
        
        # Extract version info
        version = discovered_server.get('latest_version') or discovered_server.get('version', '0.1.0')
        
        # Create the server entry
        server_entry = {
            "name": name,
            "slug": slug,
            "repository": discovered_server.get('repository'),
            "category": category,
            "description": discovered_server.get('description', ''),
            "maintainer": {
                "name": maintainer.get('name', 'Unknown'),
                "type": maintainer.get('type', 'individual'),
                "contact": maintainer.get('contact', '')
            },
            "versions": [
                {
                    "version": version,
                    "release_date": datetime.now(timezone.utc).strftime('%Y-%m-%d'),
                    "security_status": "under-review",
                    "is_recommended": False,
                    "security_scan": {
                        "scan_date": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                        "scanner_version": "1.2.0",
                        "static_analysis": {
                            "status": "not-applicable",
                            "details": "Security scan not yet performed",
                            "score": 50,
                            "issues_found": 0
                        },
                        "dependency_scan": {
                            "status": "not-applicable",
                            "details": "Dependency scan not yet performed",
                            "score": 50,
                            "issues_found": 0
                        },
                        "tool_poisoning_check": {
                            "status": "not-applicable",
                            "details": "MCP security scan not yet performed",
                            "score": 50,
                            "issues_found": 0
                        },
                        "manual_review": {
                            "reviewer": "automated-discovery",
                            "review_date": datetime.now(timezone.utc).strftime('%Y-%m-%d'),
                            "architecture_review": {
                                "status": "pass",
                                "details": f"Discovered via automated system - discovery score: {discovered_server.get('discovery_score', 0)}",
                                "score": min(80, 50 + discovered_server.get('discovery_score', 0) // 2)
                            },
                            "notes": f"Automatically discovered from {discovered_server.get('source', 'unknown source')}"
                        },
                        "overall_score": 50
                    },
                    "vulnerabilities": []
                }
            ],
            "mcp_protocol_versions": ["2024-11-05"],
            "tags": generate_tags(discovered_server)
        }
        
        return server_entry
        
    except Exception as e:
        logger.error(f"Failed to convert server {discovered_server.get('name')}: {e}")
        return None

def determine_category(server: Dict, maintainer: Dict) -> str:
    """Determine the appropriate category for a server."""
    maintainer_name = maintainer.get('name', '').lower()
    repo_url = server.get('repository', '').lower()
    
    # Official/Enterprise indicators
    official_orgs = ['anthropic', 'github', 'microsoft', 'google', 'aws', 'stripe', 'notion']
    
    if any(org in maintainer_name or org in repo_url for org in official_orgs):
        return 'enterprise'
    
    # High-quality community projects
    stars = server.get('stars', 0)
    discovery_score = server.get('discovery_score', 0)
    
    if stars > 100 or discovery_score > 50:
        return 'community'
    
    # Default to community
    return 'community'

def generate_tags(server: Dict) -> List[str]:
    """Generate appropriate tags for a server."""
    tags = []
    
    # Language tag
    language = server.get('language', '').lower()
    if language and language != 'unknown':
        tags.append(language)
    
    # Add keywords/topics if available
    keywords = server.get('keywords', [])
    topics = server.get('topics', [])
    
    all_keywords = keywords + topics
    
    # Filter and add relevant keywords
    relevant_keywords = []
    for keyword in all_keywords:
        if isinstance(keyword, str):
            keyword = keyword.lower().strip()
            if keyword and len(keyword) > 2 and keyword not in ['mcp', 'server']:
                relevant_keywords.append(keyword)
    
    tags.extend(relevant_keywords[:5])  # Limit to 5 additional tags
    
    # Add source tag
    source = server.get('source')
    if source:
        tags.append(f"discovered-{source}")
    
    return tags

def main():
    parser = argparse.ArgumentParser(
        description='Process discovered servers for inclusion'
    )
    
    parser.add_argument(
        '--discovered',
        required=True,
        help='Path to discovered servers JSON file'
    )
    
    parser.add_argument(
        '--existing',
        required=True,
        help='Path to existing servers JSON file'
    )
    
    parser.add_argument(
        '--output',
        required=True,
        help='Path to output candidates JSON file'
    )
    
    args = parser.parse_args()
    
    process_discovered_servers(args.discovered, args.existing, args.output)

if __name__ == '__main__':
    main()