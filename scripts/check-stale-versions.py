#!/usr/bin/env python3
"""
Check Stale Versions - Check for servers with outdated versions
"""
import argparse
import json
import logging
from datetime import datetime, timezone, timedelta
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


def save_json_file(data: List[Dict], file_path: str):
    """Save JSON file"""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved stale versions data to {file_path}")
    except Exception as e:
        logger.error(f"Error saving {file_path}: {e}")
        raise


def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime object"""
    try:
        # Try different date formats
        formats = [
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
            except ValueError:
                continue
        
        # Fallback - try to parse ISO format
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        
    except Exception as e:
        logger.warning(f"Could not parse date '{date_str}': {e}")
        return datetime.now(timezone.utc)


def calculate_days_since_update(release_date: str, scan_date: str = None) -> int:
    """Calculate days since version was released or scanned"""
    now = datetime.now(timezone.utc)
    
    # Use scan date if available, otherwise use release date
    reference_date = scan_date if scan_date else release_date
    
    if not reference_date:
        return 0
    
    ref_datetime = parse_date(reference_date)
    return (now - ref_datetime).days


def check_stale_versions(servers_data: Dict, max_age_days: int) -> List[Dict]:
    """Check for stale versions in servers data"""
    stale_versions = []
    
    for server in servers_data.get('servers', []):
        # Get the latest version (first in list)
        if not server.get('versions'):
            continue
            
        latest_version = server['versions'][0]
        
        # Calculate days since update
        scan_date = None
        if latest_version.get('security_scan', {}).get('scan_date'):
            scan_date = latest_version['security_scan']['scan_date']
        
        days_since_update = calculate_days_since_update(
            latest_version['release_date'],
            scan_date
        )
        
        # Check if version is stale
        if days_since_update > max_age_days:
            stale_entry = {
                'server': server['name'],
                'slug': server['slug'],
                'repository': server['repository'],
                'version': latest_version['version'],
                'release_date': latest_version['release_date'],
                'last_updated': scan_date or latest_version['release_date'],
                'days_since_update': days_since_update,
                'security_status': latest_version.get('security_status', 'unknown'),
                'is_recommended': latest_version.get('is_recommended', False)
            }
            
            # Try to get latest version info from repository
            # Note: This would require GitHub API calls in a real implementation
            # For now, we'll just indicate it needs checking
            stale_entry['latest_version'] = 'Unknown - needs checking'
            stale_entry['needs_version_check'] = True
            
            stale_versions.append(stale_entry)
            logger.info(f"Found stale version: {server['name']} v{latest_version['version']} ({days_since_update} days old)")
    
    return stale_versions


def main():
    parser = argparse.ArgumentParser(description='Check for stale versions in MCP servers')
    parser.add_argument('--servers', required=True, help='Path to servers.json file')
    parser.add_argument('--max-age-days', type=int, default=90, help='Maximum age in days before version is considered stale')
    parser.add_argument('--output', required=True, help='Output file for stale versions')
    
    args = parser.parse_args()
    
    # Load servers data
    servers_data = load_json_file(args.servers)
    
    # Check for stale versions
    stale_versions = check_stale_versions(servers_data, args.max_age_days)
    
    # Save results
    if stale_versions:
        save_json_file(stale_versions, args.output)
    else:
        logger.info("No stale versions found")
    
    logger.info(f"Found {len(stale_versions)} stale versions (older than {args.max_age_days} days)")


if __name__ == '__main__':
    main()