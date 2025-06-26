#!/usr/bin/env python3
"""
Update Security Data and Generate README
=========================================

This script combines the functionality of updating the security data in
data/servers.json with the generation of the README.md file.
"""

import argparse
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ArtifactsUpdater:
    """Update servers.json and generate README.md."""

    def __init__(self):
        self.status_mapping = {
            (85, 100): 'verified-secure',
            (70, 84): 'conditional',
            (50, 69): 'under-review',
            (0, 49): 'not-recommended'
        }
        self.security_badges = {
            'verified-secure': '🛡️ Verified Secure',
            'conditional': '⚠️ Conditional',
            'under-review': '🔄 Under Review',
            'not-recommended': '❌ Not Recommended',
            'deprecated': '🗑️ Deprecated',
            'awaiting-scan': '⏳ Awaiting Scan'
        }

    def update_and_generate(self, servers_file: str, scan_results_file: str, readme_file: str, dry_run: bool = False):
        """Update security data and generate README."""
        try:
            # Load input files
            logger.info("Loading servers data and scan results...")
            servers_data = self._load_json_file(servers_file)
            scan_results = self._load_json_file(scan_results_file)

            # Update servers data with scan results
            logger.info("Updating servers data with scan results...")
            updated_data = self._update_servers_data(servers_data, scan_results)

            # Generate new README content
            logger.info("Generating new README content...")
            new_readme_content = self._generate_readme(readme_file, updated_data)

            if dry_run:
                logger.info("DRY RUN: Skipping file writing.")
                print("Updated servers.json content:")
                print(json.dumps(updated_data, indent=2))
                print("\nNew README.md content:")
                print(new_readme_content)
                return

            # Save updated data
            self._save_json_file(updated_data, servers_file)

            # Save updated README
            with open(readme_file, 'w') as f:
                f.write(new_readme_content)
            logger.info(f"Successfully updated {readme_file}")

        except Exception as e:
            logger.error(f"Failed to update artifacts: {e}")
            raise

    def _load_json_file(self, file_path: str) -> Dict:
        """Load and parse JSON file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load {file_path}: {e}")
            raise

    def _save_json_file(self, data: Dict, file_path: str) -> None:
        """Save data to JSON file."""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved updated data to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save {file_path}: {e}")
            raise

    def _update_servers_data(self, servers_data: Dict, scan_results: Dict) -> Dict:
        """Update servers data with scan results."""
        updated_data = servers_data.copy()
        updated_data['last_updated'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

        scan_lookup = {result['server_slug']: result for result in scan_results.get('results', [])}

        updated_servers = []
        for server in updated_data['servers']:
            slug = server['slug']
            if slug in scan_lookup:
                logger.info(f"Updating server: {server['name']}")
                updated_server = server.copy()
                scan_result = scan_lookup[slug]

                updated_versions = []
                for version in server['versions']:
                    version_scan = next((vs for vs in scan_result['versions'] if vs['version'] == version['version']), None)
                    if version_scan:
                        updated_version = self._update_server_version(version, {'versions': [version_scan], 'scanner_version': scan_result['scanner_version']})
                        updated_versions.append(updated_version)
                    else:
                        updated_versions.append(version)
                updated_server['versions'] = updated_versions
                updated_servers.append(updated_server)
            else:
                updated_servers.append(server)

        updated_data['servers'] = updated_servers
        return updated_data

    def _update_server_version(self, server_version: Dict, scan_result: Dict) -> Dict:
        """Update a server version with scan results."""
        security_scan = self._map_scan_result_to_server_format(scan_result)
        updated_version = server_version.copy()
        updated_version['security_scan'] = security_scan
        updated_version['security_status'] = self._determine_security_status(security_scan['overall_score'])
        updated_version['is_recommended'] = updated_version['security_status'] in ['verified-secure', 'conditional']
        logger.info(f"Updated version {updated_version['version']} - Score: {security_scan['overall_score']}, Status: {updated_version['security_status']}")
        return updated_version

    def _map_scan_result_to_server_format(self, scan_result: Dict) -> Dict:
        """Convert scan result format to servers.json format."""
        version_scan = scan_result['versions'][0]
        scan_date = version_scan['scan_date']
        if '+' in scan_date:
            dt = datetime.fromisoformat(scan_date.replace('Z', '+00:00'))
            scan_date = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        security_scan = {
            'scan_date': scan_date,
            'scanner_version': scan_result['scanner_version'],
            'static_analysis': version_scan['static_analysis'],
            'dependency_scan': version_scan['dependency_scan'],
            'tool_poisoning_check': version_scan['mcp_security_scan'],
            'overall_score': version_scan['overall_score']
        }
        if 'container_scan' in version_scan:
            security_scan['container_scan'] = version_scan['container_scan']
        if 'security_documentation_check' in version_scan:
            security_scan['security_documentation'] = version_scan['security_documentation_check']
        return security_scan

    def _determine_security_status(self, overall_score: int) -> str:
        """Determine security status based on overall score."""
        for (min_score, max_score), status in self.status_mapping.items():
            if min_score <= overall_score <= max_score:
                return status
        return 'under-review'

    def _generate_readme(self, readme_file: str, servers_data: Dict) -> str:
        """Generate the new README content."""
        with open(readme_file, 'r') as f:
            readme_content = f.read()

        new_tables = self._generate_security_tables(servers_data)
        start_idx, end_idx = self._find_section_boundaries(readme_content)
        lines = readme_content.split('\n')
        new_lines = lines[:start_idx] + new_tables + lines[end_idx:]
        return '\n'.join(new_lines)

    def _generate_security_tables(self, servers_data: Dict[str, Any]) -> List[str]:
        """Generate all security status tables and detailed breakdowns."""
        servers = servers_data.get('servers', [])
        categories = self._group_servers_by_category(servers)
        lines = [
            "## Security Status by Category",
            "",
            f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}  ",
            f"**Total Servers:** {len(servers)}",
            "",
        ]
        category_order = ['official', 'enterprise', 'security-tools', 'community', 'under-review', 'deprecated']
        for category in category_order:
            if categories[category]:
                lines.extend(self._generate_category_section(category, categories[category]))

        lines.extend([
            "---",
            "",
            "## 📊 Detailed Security Assessments",
            "",
            "_Click on server scores above to jump to detailed security breakdowns:_",
            "",
        ])

        for server in sorted(servers, key=lambda s: s.get('name', '').lower()):
            version_data = self._get_latest_version(server)
            if not self._is_awaiting_scan(version_data):
                server_slug = server.get('slug', 'unknown')
                details = self._generate_security_details(version_data, server_slug)
                if details:
                    lines.extend([
                        f'<details id="security-details-{server_slug}">',
                        f'<summary><strong>{server.get("name", "Unknown")}</strong> Security Assessment</summary>',
                        "",
                        details,
                        "",
                        "</details>",
                        ""
                    ])
        return lines

    def _group_servers_by_category(self, servers: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group servers by category."""
        categories = {
            'official': [], 'enterprise': [], 'security-tools': [],
            'community': [], 'under-review': [], 'deprecated': []
        }
        for server in servers:
            category = server.get('category', 'under-review')
            if category in categories:
                categories[category].append(server)
            else:
                categories['under-review'].append(server)
        return categories

    def _generate_category_section(self, category: str, servers: List[Dict[str, Any]]) -> List[str]:
        """Generate a category section with table."""
        category_titles = {
            'official': 'Official Servers', 'enterprise': 'Enterprise Servers',
            'security-tools': 'Security Tools', 'community': 'Community Servers',
            'under-review': 'Under Review', 'deprecated': 'Deprecated Servers'
        }
        title = category_titles.get(category, category.title())
        lines = [
            f"### {title}",
            "",
            "| Server | Version | Security Status | Description |",
            "|--------|---------|----------------|-------------|"
        ]
        for server in sorted(servers, key=lambda s: s.get('name', '').lower()):
            lines.append(self._generate_server_table_row(server))
        lines.append("")
        return lines

    def _generate_server_table_row(self, server: Dict[str, Any]) -> str:
        """Generate a table row for a server."""
        name = server.get('name', 'Unknown')
        repo = server.get('repository', '#')
        description = server.get('description', 'No description')
        server_slug = server.get('slug', 'unknown')
        version_data = self._get_latest_version(server)
        version = version_data.get('version', 'N/A')
        security_status = self._format_security_status(version_data)
        score = self._get_security_score(version_data, server_slug)
        name_link = f"[{name}]({repo})"
        return f"| {name_link} | {version} | {security_status}{score} | {description} |"

    def _get_latest_version(self, server: Dict[str, Any]) -> Dict[str, Any]:
        """Get the latest recommended version or most recent version."""
        versions = server.get('versions', [])
        if not versions:
            return {}
        recommended = [v for v in versions if v.get('is_recommended', False)]
        if recommended:
            return recommended[0]
        return versions[0]

    def _is_awaiting_scan(self, version: Dict[str, Any]) -> bool:
        """Check if server is awaiting scan."""
        return version.get('security_scan', {}).get('static_analysis', {}).get('details', '') == 'Repository not available'

    def _format_security_status(self, version: Dict[str, Any]) -> str:
        """Format security status with badge."""
        if self._is_awaiting_scan(version):
            return self.security_badges['awaiting-scan']
        status = version.get('security_status', 'under-review')
        return self.security_badges.get(status, f'🔄 {status.title()}')

    def _get_security_score(self, version: Dict[str, Any], server_slug: str) -> str:
        """Get formatted security score with clickable details."""
        if self._is_awaiting_scan(version):
            return ""
        score = version.get('security_scan', {}).get('overall_score')
        if score is not None:
            return f" ([📊 Score: {score}/100](#security-details-{server_slug}))"
        return ""

    def _generate_security_details(self, version: Dict[str, Any], server_slug: str) -> str:
        """Generate detailed security breakdown section."""
        scan = version.get('security_scan', {})
        if not scan:
            return ""
        
        details = [f"### Security Assessment: {scan.get('scan_date', 'Unknown date')[:10]}", ""]
        
        # MCP Security Analysis
        mcp_scan = scan.get('tool_poisoning_check', {})
        if mcp_scan:
            details.extend(self._format_scan_details("🔍 MCP-Specific Security", "Scans for MCP-specific threats like tool poisoning attacks", mcp_scan))

        # Dependency Scan
        dep_scan = scan.get('dependency_scan', {})
        if dep_scan:
            details.extend(self._format_scan_details("📦 Third-Party Dependencies", "Scans package.json, requirements.txt, etc. for known CVEs", dep_scan))

        # Static Analysis
        static = scan.get('static_analysis', {})
        if static:
            details.extend(self._format_scan_details("🐛 Code Security Analysis", "Static analysis for common security vulnerabilities in source code", static))

        # Container Security
        container = scan.get('container_scan', {})
        if container:
            details.extend(self._format_scan_details("🐳 Container Security", "Analyzes Dockerfile and container configurations for security issues", container))

        # Documentation
        docs = scan.get('security_documentation', {})
        if docs:
            details.extend(self._format_scan_details("📋 Security Documentation", "Checks for security guidelines, vulnerability reporting, and usage instructions", docs))

        return "\n".join(details)

    def _format_scan_details(self, title: str, subtitle: str, scan_data: Dict) -> List[str]:
        """Format a generic scan detail section."""
        status = scan_data.get('status', 'unknown')
        score = scan_data.get('score', 0)
        details_text = scan_data.get('details', 'No details')
        issues = scan_data.get('issues_found', 0)
        status_emoji = "✅" if status == "pass" else "⚠️" if status == "warning" else "❌" if status == "fail" else "➖"

        lines = [f"**{title}**: {score}/100 {status_emoji}", f"*{subtitle}*", ""]
        
        if status == "pass":
            lines.append(f"✅ **No issues found**")
            lines.append(f"- {details_text}")
        elif status == "warning":
            lines.append(f"⚠️ **{issues} potential issues found**")
            lines.append(f"- {details_text}")
        elif status == "fail":
            lines.append(f"❌ **{issues} critical issues found**")
            lines.append(f"- {details_text}")
        elif status == "not-applicable":
            lines.append(f"➖ **Not applicable**")
            lines.append(f"- {details_text}")

        lines.append("")
        return lines

    def _find_section_boundaries(self, readme_content: str) -> Tuple[int, int]:
        """Find the start and end of the security tables section."""
        lines = readme_content.split('\n')
        section_markers = ["## Security Status by Category"]
        start_idx = -1
        for i, line in enumerate(lines):
            if any(marker in line for marker in section_markers):
                start_idx = i
                break
        if start_idx == -1:
            return len(lines) - 1, len(lines) - 1

        # Find the end after security assessments section ends
        end_markers = ["</details>"]
        end_idx = len(lines)
        in_assessments = False
        for i in range(start_idx + 1, len(lines)):
            if "## 📊 Detailed Security Assessments" in lines[i]:
                in_assessments = True
            elif in_assessments and lines[i].strip() == "</details>":
                # Look for the last closing details tag
                end_idx = i + 1
        return start_idx, end_idx

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Update security data and generate README.')
    parser.add_argument('--servers', default='data/servers.json', help='Servers data file')
    parser.add_argument('--scan-results', required=True, help='Scan results JSON file')
    parser.add_argument('--readme', default='README.md', help='README file to update')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed')
    args = parser.parse_args()

    updater = ArtifactsUpdater()
    updater.update_and_generate(args.servers, args.scan_results, args.readme, args.dry_run)

if __name__ == '__main__':
    main()
