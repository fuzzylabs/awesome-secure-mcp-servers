#!/usr/bin/env python3
"""
Security Data Updater for MCP Servers
=====================================

This script merges security scan results back into the servers.json file,
updating the security_scan and security_status fields with real data.
"""

import argparse
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SecurityDataUpdater:
    """Update servers.json with real security scan results."""
    
    def __init__(self):
        self.status_mapping = {
            (85, 100): 'verified-secure',
            (70, 84): 'conditional', 
            (50, 69): 'under-review',
            (0, 49): 'not-recommended'
        }
    
    def determine_security_status(self, overall_score: int) -> str:
        """Determine security status based on overall score."""
        for (min_score, max_score), status in self.status_mapping.items():
            if min_score <= overall_score <= max_score:
                return status
        return 'under-review'
    
    def map_scan_result_to_server_format(self, scan_result: Dict) -> Dict:
        """Convert scan result format to servers.json format."""
        version_scan = scan_result['versions'][0]  # Assuming one version per scan
        
        # Convert scan_date to proper ISO format (max 3 decimal places, Z suffix)
        scan_date = version_scan['scan_date']
        if '+' in scan_date:
            # Convert +00:00 format to Z and limit milliseconds
            dt = datetime.fromisoformat(scan_date.replace('Z', '+00:00'))
            scan_date = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        
        # Map scan components to servers.json format
        security_scan = {
            'scan_date': scan_date,
            'scanner_version': scan_result['scanner_version'],
            'static_analysis': {
                'status': version_scan['static_analysis']['status'],
                'details': version_scan['static_analysis']['details'],
                'score': version_scan['static_analysis']['score'],
                'issues_found': version_scan['static_analysis'].get('issues_found', 0)
            },
            'dependency_scan': {
                'status': version_scan['dependency_scan']['status'], 
                'details': version_scan['dependency_scan']['details'],
                'score': version_scan['dependency_scan']['score'],
                'issues_found': version_scan['dependency_scan'].get('issues_found', 0)
            },
            'tool_poisoning_check': {
                'status': version_scan['mcp_security_scan']['status'],
                'details': version_scan['mcp_security_scan']['details'], 
                'score': version_scan['mcp_security_scan']['score'],
                'issues_found': version_scan['mcp_security_scan'].get('issues_found', 0)
            },
            'overall_score': version_scan['overall_score']
        }
        
        # Add container scan if available
        if version_scan.get('container_scan'):
            security_scan['container_scan'] = {
                'status': version_scan['container_scan']['status'],
                'details': version_scan['container_scan']['details'],
                'score': version_scan['container_scan']['score']
            }
        
        # Add security documentation check
        if version_scan.get('security_documentation_check'):
            security_scan['security_documentation'] = {
                'status': version_scan['security_documentation_check']['status'],
                'details': version_scan['security_documentation_check']['details'],
                'score': version_scan['security_documentation_check']['score']
            }
        
        return security_scan
    
    def update_server_version(self, server_version: Dict, scan_result: Dict) -> Dict:
        """Update a server version with scan results."""
        # Map scan results to server format
        security_scan = self.map_scan_result_to_server_format(scan_result)
        
        # Update version data
        updated_version = server_version.copy()
        updated_version['security_scan'] = security_scan
        updated_version['security_status'] = self.determine_security_status(
            security_scan['overall_score']
        )
        
        # Update recommendation based on security status
        if updated_version['security_status'] in ['verified-secure', 'conditional']:
            updated_version['is_recommended'] = True
        else:
            updated_version['is_recommended'] = False
        
        logger.info(
            f"Updated version {updated_version['version']} - "
            f"Score: {security_scan['overall_score']}, "
            f"Status: {updated_version['security_status']}"
        )
        
        return updated_version
    
    def update_servers_data(self, servers_data: Dict, scan_results: Dict) -> Dict:
        """Update servers data with scan results."""
        updated_data = servers_data.copy()
        
        # Update last_updated timestamp
        updated_data['last_updated'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Create lookup for scan results by server slug
        scan_lookup = {}
        for result in scan_results.get('results', []):
            scan_lookup[result['server_slug']] = result
        
        # Update each server
        updated_servers = []
        for server in updated_data['servers']:
            slug = server['slug']
            
            if slug in scan_lookup:
                logger.info(f"Updating server: {server['name']}")
                updated_server = server.copy()
                scan_result = scan_lookup[slug]
                
                # Update each version that was scanned
                updated_versions = []
                for version in server['versions']:
                    # Find matching scan result for this version
                    version_scan = None
                    for scanned_version in scan_result['versions']:
                        if scanned_version['version'] == version['version']:
                            version_scan = {
                                'versions': [scanned_version],
                                'scanner_version': scan_result['scanner_version']
                            }
                            break
                    
                    if version_scan:
                        updated_version = self.update_server_version(version, version_scan)
                        updated_versions.append(updated_version)
                    else:
                        # Keep original version if not scanned
                        updated_versions.append(version)
                
                updated_server['versions'] = updated_versions
                updated_servers.append(updated_server)
            else:
                # Keep original server if not scanned
                updated_servers.append(server)
        
        updated_data['servers'] = updated_servers
        return updated_data
    
    def load_json_file(self, file_path: str) -> Dict:
        """Load and parse JSON file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load {file_path}: {e}")
            raise
    
    def save_json_file(self, data: Dict, file_path: str) -> None:
        """Save data to JSON file."""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved updated data to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save {file_path}: {e}")
            raise
    
    def update_security_data(self, servers_file: str, scan_results_file: str, 
                           output_file: Optional[str] = None) -> bool:
        """Main method to update security data."""
        try:
            # Load input files
            logger.info("Loading servers data and scan results...")
            servers_data = self.load_json_file(servers_file)
            scan_results = self.load_json_file(scan_results_file)
            
            # Update servers data with scan results
            logger.info("Updating servers data with scan results...")
            updated_data = self.update_servers_data(servers_data, scan_results)
            
            # Save updated data
            output_path = output_file or servers_file
            self.save_json_file(updated_data, output_path)
            
            # Report summary
            total_scanned = len(scan_results.get('results', []))
            logger.info(f"Successfully updated {total_scanned} servers with security data")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update security data: {e}")
            return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Update servers.json with security scan results')
    parser.add_argument('--servers', required=True, help='Path to servers.json file')
    parser.add_argument('--scan-results', required=True, help='Path to scan results JSON file')
    parser.add_argument('--output', help='Output file path (defaults to input servers file)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be updated without writing')
    
    args = parser.parse_args()
    
    updater = SecurityDataUpdater()
    
    if args.dry_run:
        logger.info("DRY RUN: Would update security data but not writing to file")
        # Load and process but don't save
        servers_data = updater.load_json_file(args.servers)
        scan_results = updater.load_json_file(args.scan_results)
        updated_data = updater.update_servers_data(servers_data, scan_results)
        logger.info("DRY RUN: Update completed successfully (no files written)")
        return 0
    
    success = updater.update_security_data(args.servers, args.scan_results, args.output)
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())