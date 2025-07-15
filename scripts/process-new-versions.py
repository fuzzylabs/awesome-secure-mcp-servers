#!/usr/bin/env python3
"""
Process New Versions - Process detected new versions and update servers.json
"""
import argparse
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_json_file(file_path: str) -> Dict:
    """Load JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        raise


def save_json_file(data: Dict, file_path: str):
    """Save JSON file"""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved updated data to {file_path}")
    except Exception as e:
        logger.error(f"Error saving {file_path}: {e}")
        raise


def create_new_version_entry(new_version: Dict) -> Dict:
    """Create a new version entry for servers.json"""
    return {
        "version": new_version['version'],
        "release_date": new_version['release_date'],
        "security_status": "under-review",
        "is_recommended": False,
        "security_scan": {
            "scan_date": None,
            "scanner_version": None,
            "static_analysis": {
                "status": "pending",
                "details": "Awaiting security scan",
                "score": 0,
                "issues_found": 0,
                "tools_used": []
            },
            "dependency_scan": {
                "status": "pending",
                "details": "Awaiting security scan",
                "score": 0,
                "issues_found": 0,
                "vulnerabilities": {
                    "info": 0,
                    "low": 0,
                    "moderate": 0,
                    "high": 0,
                    "critical": 0,
                    "total": 0
                }
            },
            "tool_poisoning_check": {
                "status": "pending",
                "details": "Awaiting security scan",
                "score": 0,
                "issues_found": 0
            },
            "container_security": {
                "status": "pending",
                "details": "Awaiting security scan",
                "score": 0,
                "issues_found": 0
            },
            "security_documentation": {
                "status": "pending",
                "details": "Awaiting security scan",
                "score": 0,
                "has_security_md": False,
                "has_vulnerability_reporting": False
            },
            "overall_score": 0,
            "recommendations": [
                "New version detected - requires security validation"
            ]
        }
    }


def update_servers_with_new_versions(servers_data: Dict, new_versions: List[Dict]) -> Dict:
    """Update servers data with new versions"""
    updated_servers = servers_data.copy()
    
    # Create a mapping of slug to server for quick lookup
    server_map = {server['slug']: server for server in updated_servers['servers']}
    
    for new_version in new_versions:
        slug = new_version['slug']
        
        if slug not in server_map:
            logger.warning(f"Server with slug '{slug}' not found in servers.json")
            continue
        
        server = server_map[slug]
        
        # Create new version entry
        new_version_entry = create_new_version_entry(new_version)
        
        # Add to the beginning of versions list (most recent first)
        server['versions'].insert(0, new_version_entry)
        
        # Update is_recommended for older versions
        for i, version_entry in enumerate(server['versions']):
            if i == 0:
                # New version gets is_recommended=False until security scan
                version_entry['is_recommended'] = False
            else:
                # Older versions lose recommendation status
                version_entry['is_recommended'] = False
        
        logger.info(f"Added new version {new_version['version']} for {server['name']}")
    
    # Update last_updated timestamp
    updated_servers['last_updated'] = datetime.now(timezone.utc).isoformat()
    
    return updated_servers


def main():
    parser = argparse.ArgumentParser(description='Process new versions and update servers.json')
    parser.add_argument('--new-versions', required=True, help='Path to new versions JSON file')
    parser.add_argument('--servers', required=True, help='Path to servers.json file')
    parser.add_argument('--output', required=True, help='Output file for updated servers.json')
    
    args = parser.parse_args()
    
    # Load new versions
    new_versions = load_json_file(args.new_versions)
    
    # Load servers data
    servers_data = load_json_file(args.servers)
    
    # Update servers with new versions
    updated_servers = update_servers_with_new_versions(servers_data, new_versions)
    
    # Save updated servers
    save_json_file(updated_servers, args.output)
    
    logger.info(f"Processed {len(new_versions)} new versions successfully")


if __name__ == '__main__':
    main()