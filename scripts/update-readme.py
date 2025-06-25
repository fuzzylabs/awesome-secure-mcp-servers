#!/usr/bin/env python3
"""
README Generator for MCP Server Security Data
==============================================

This script generates the security status tables in README.md from the actual
security data in data/servers.json, replacing placeholder content with real
security assessments.
"""

import json
import re
import argparse
from datetime import datetime
from typing import Dict, List, Any, Tuple

class ReadmeGenerator:
    """Generate README content from security data."""
    
    def __init__(self):
        self.security_badges = {
            'verified-secure': '🛡️ Verified Secure',
            'conditional': '⚠️ Conditional', 
            'under-review': '🔄 Under Review',
            'not-recommended': '❌ Not Recommended',
            'deprecated': '🗑️ Deprecated',
            'awaiting-scan': '⏳ Awaiting Scan'
        }
        
    def load_servers_data(self, servers_file: str) -> Dict[str, Any]:
        """Load and validate servers data."""
        try:
            with open(servers_file, 'r') as f:
                data = json.load(f)
            
            if 'servers' not in data:
                raise ValueError("Invalid servers data: missing 'servers' key")
                
            return data
        except Exception as e:
            raise ValueError(f"Failed to load servers data: {e}")
    
    def get_latest_version(self, server: Dict[str, Any]) -> Dict[str, Any]:
        """Get the latest recommended version or most recent version."""
        versions = server.get('versions', [])
        if not versions:
            return {}
            
        # Prefer recommended versions
        recommended = [v for v in versions if v.get('is_recommended', False)]
        if recommended:
            return recommended[0]  # Assuming first is latest
            
        # Fall back to first version (assuming sorted by recency)
        return versions[0]
    
    def is_awaiting_scan(self, version: Dict[str, Any]) -> bool:
        """Check if server is awaiting scan (repository not available)."""
        scan = version.get('security_scan', {})
        static_analysis = scan.get('static_analysis', {})
        return static_analysis.get('details', '').strip() == 'Repository not available'
    
    def format_security_status(self, version: Dict[str, Any]) -> str:
        """Format security status with badge."""
        # Check if this is an unscanned server (repository not available)
        if self.is_awaiting_scan(version):
            return self.security_badges['awaiting-scan']
        
        status = version.get('security_status', 'under-review')
        return self.security_badges.get(status, f'🔄 {status.title()}')
    
    def get_security_score(self, version: Dict[str, Any], server_slug: str) -> str:
        """Get formatted security score with clickable details."""
        # Don't show scores for servers awaiting scan
        if self.is_awaiting_scan(version):
            return ""
        
        scan = version.get('security_scan', {})
        score = scan.get('overall_score')
        if score is not None:
            # Create expandable details section
            details = self.generate_security_details(version, server_slug)
            if details:
                return f" ([📊 Score: {score}/100](#security-details-{server_slug}))"
            else:
                return f" (Score: {score}/100)"
        return ""
    
    def generate_security_details(self, version: Dict[str, Any], server_slug: str) -> str:
        """Generate detailed security breakdown section."""
        scan = version.get('security_scan', {})
        if not scan:
            return ""
        
        details = [f"### Security Details: {server_slug}", ""]
        
        # MCP Security Analysis
        mcp_scan = scan.get('tool_poisoning_check', {})
        if mcp_scan:
            status = mcp_scan.get('status', 'unknown')
            score = mcp_scan.get('score', 0)
            details_text = mcp_scan.get('details', 'No details')
            status_emoji = "✅" if status == "pass" else "⚠️" if status == "warning" else "❌"
            details.append(f"**🔍 MCP Security**: {score}/100 {status_emoji}")
            details.append(f"- Status: {status}")
            details.append(f"- Details: {details_text}")
            details.append("")
        
        # Dependency Scan
        dep_scan = scan.get('dependency_scan', {})
        if dep_scan:
            status = dep_scan.get('status', 'unknown')
            score = dep_scan.get('score', 0)
            issues = dep_scan.get('issues_found', 0)
            status_emoji = "✅" if status == "pass" else "⚠️" if status == "warning" else "❌"
            details.append(f"**📦 Dependencies**: {score}/100 {status_emoji}")
            details.append(f"- Status: {status}")
            details.append(f"- Issues found: {issues}")
            details.append("")
        
        # Static Analysis
        static = scan.get('static_analysis', {})
        if static:
            status = static.get('status', 'unknown')
            score = static.get('score', 0)
            issues = static.get('issues_found', 0)
            status_emoji = "✅" if status == "pass" else "⚠️" if status == "warning" else "❌"
            details.append(f"**🐛 Static Analysis**: {score}/100 {status_emoji}")
            details.append(f"- Status: {status}")
            details.append(f"- Issues found: {issues}")
            details.append("")
        
        # Container Security
        container = scan.get('container_scan', {})
        if container:
            status = container.get('status', 'unknown')
            score = container.get('score', 0)
            status_emoji = "✅" if status == "pass" else "⚠️" if status == "warning" else "❌" if status == "fail" else "➖"
            details.append(f"**🐳 Container**: {score}/100 {status_emoji}")
            details.append(f"- Status: {status}")
            details.append("")
        
        # Documentation
        docs = scan.get('security_documentation', {})
        if docs:
            status = docs.get('status', 'unknown')
            score = docs.get('score', 0)
            status_emoji = "✅" if status == "pass" else "⚠️" if status == "warning" else "❌"
            details.append(f"**📋 Documentation**: {score}/100 {status_emoji}")
            details.append(f"- Status: {status}")
            details.append("")
        
        return "\n".join(details)
    
    def generate_server_table_row(self, server: Dict[str, Any]) -> str:
        """Generate a table row for a server."""
        name = server.get('name', 'Unknown')
        repo = server.get('repository', '#')
        description = server.get('description', 'No description')
        server_slug = server.get('slug', 'unknown')
        
        version_data = self.get_latest_version(server)
        version = version_data.get('version', 'N/A')
        security_status = self.format_security_status(version_data)
        score = self.get_security_score(version_data, server_slug)
        
        # Create clickable name with repository link
        name_link = f"[{name}]({repo})"
        
        return f"| {name_link} | {version} | {security_status}{score} | {description} |"
    
    def group_servers_by_category(self, servers: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group servers by category."""
        categories = {
            'official': [],
            'enterprise': [],
            'security-tools': [],
            'community': [],
            'under-review': [],
            'deprecated': []
        }
        
        for server in servers:
            category = server.get('category', 'under-review')
            if category in categories:
                categories[category].append(server)
            else:
                categories['under-review'].append(server)
        
        return categories
    
    def generate_category_section(self, category: str, servers: List[Dict[str, Any]]) -> List[str]:
        """Generate a category section with table."""
        if not servers:
            return []
            
        category_titles = {
            'official': 'Official Servers',
            'enterprise': 'Enterprise Servers', 
            'security-tools': 'Security Tools',
            'community': 'Community Servers',
            'under-review': 'Under Review',
            'deprecated': 'Deprecated Servers'
        }
        
        title = category_titles.get(category, category.title())
        
        lines = [
            f"### {title}",
            "",
            "| Server | Version | Security Status | Description |",
            "|--------|---------|----------------|-------------|"
        ]
        
        # Sort servers by name for consistent output
        sorted_servers = sorted(servers, key=lambda s: s.get('name', '').lower())
        
        for server in sorted_servers:
            lines.append(self.generate_server_table_row(server))
        
        lines.append("")  # Empty line after table
        return lines
    
    def generate_security_tables(self, servers_data: Dict[str, Any]) -> List[str]:
        """Generate all security status tables and detailed breakdowns."""
        servers = servers_data.get('servers', [])
        categories = self.group_servers_by_category(servers)
        
        lines = []
        
        # Add section header
        lines.extend([
            "## Security Status by Category",
            "",
            f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}  ",
            f"**Total Servers:** {len(servers)}",
            "",
        ])
        
        # Add categories in preferred order
        category_order = ['official', 'enterprise', 'security-tools', 'community', 'under-review', 'deprecated']
        
        for category in category_order:
            if categories[category]:  # Only include categories with servers
                lines.extend(self.generate_category_section(category, categories[category]))
        
        # Add security details sections for servers with scores
        lines.extend([
            "---",
            "",
            "## 📊 Detailed Security Assessments",
            "",
            "_Click on server scores above to jump to detailed security breakdowns:_",
            "",
        ])
        
        for server in servers:
            version_data = self.get_latest_version(server)
            if not self.is_awaiting_scan(version_data):
                server_slug = server.get('slug', 'unknown')
                details = self.generate_security_details(version_data, server_slug)
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
    
    def find_section_boundaries(self, readme_content: str) -> Tuple[int, int]:
        """Find the start and end of the security tables section."""
        lines = readme_content.split('\n')
        
        # Look for different possible section markers
        section_markers = [
            "## Sample Assessments (Demo Data)",
            "## Security Status by Category", 
            "### Official Servers (Sample)",
            "### Official Servers"
        ]
        
        start_idx = None
        for i, line in enumerate(lines):
            if any(marker in line for marker in section_markers):
                start_idx = i
                break
        
        if start_idx is None:
            # If no section found, insert before "Critical Disclaimers"
            for i, line in enumerate(lines):
                if "## Critical Disclaimers" in line:
                    return i, i
            # If that doesn't exist either, insert before the end
            return len(lines) - 10, len(lines) - 10
        
        # Find the end of the section (next ## header or specific markers)
        end_markers = [
            "## Critical Disclaimers",
            "## How to Help",
            "## Community & Resources",
            "## Contact & Support",
            "## License & Legal"
        ]
        
        end_idx = len(lines)
        for i in range(start_idx + 1, len(lines)):
            line = lines[i].strip()
            if any(marker in line for marker in end_markers):
                end_idx = i
                break
        
        return start_idx, end_idx
    
    def update_readme(self, readme_file: str, servers_file: str) -> bool:
        """Update README.md with current security data."""
        try:
            # Load data
            servers_data = self.load_servers_data(servers_file)
            
            # Read current README
            with open(readme_file, 'r') as f:
                readme_content = f.read()
            
            # Generate new security tables
            new_tables = self.generate_security_tables(servers_data)
            
            # Find section to replace
            start_idx, end_idx = self.find_section_boundaries(readme_content)
            
            # Split README into lines
            lines = readme_content.split('\n')
            
            # Replace the section
            new_lines = lines[:start_idx] + new_tables + lines[end_idx:]
            
            # Write updated README
            updated_content = '\n'.join(new_lines)
            
            # Only write if content actually changed
            if updated_content != readme_content:
                with open(readme_file, 'w') as f:
                    f.write(updated_content)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error updating README: {e}")
            return False
    
    def validate_data(self, servers_file: str) -> bool:
        """Validate servers data before updating README."""
        try:
            data = self.load_servers_data(servers_file)
            servers = data.get('servers', [])
            
            if not servers:
                print("Warning: No servers found in data")
                return False
            
            # Basic validation
            for i, server in enumerate(servers):
                required_fields = ['name', 'slug', 'repository', 'category', 'description']
                for field in required_fields:
                    if not server.get(field):
                        print(f"Warning: Server {i} missing required field: {field}")
                
                versions = server.get('versions', [])
                if not versions:
                    print(f"Warning: Server '{server.get('name')}' has no versions")
            
            print(f"Validation complete: {len(servers)} servers found")
            return True
            
        except Exception as e:
            print(f"Validation failed: {e}")
            return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Update README.md with security data')
    parser.add_argument('--readme', default='README.md', help='README file to update')
    parser.add_argument('--servers', default='data/servers.json', help='Servers data file')
    parser.add_argument('--validate-only', action='store_true', help='Only validate data')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed')
    
    args = parser.parse_args()
    
    generator = ReadmeGenerator()
    
    # Validate data first
    if not generator.validate_data(args.servers):
        print("Data validation failed")
        return 1
    
    if args.validate_only:
        print("Data validation passed")
        return 0
    
    if args.dry_run:
        # Show what the new tables would look like
        servers_data = generator.load_servers_data(args.servers)
        new_tables = generator.generate_security_tables(servers_data)
        print("New security tables that would be generated:")
        print("=" * 50)
        print('\n'.join(new_tables))
        return 0
    
    # Update README
    if generator.update_readme(args.readme, args.servers):
        print(f"✅ README updated successfully")
        return 0
    else:
        print("ℹ️ No changes needed - README already up to date")
        return 0

if __name__ == '__main__':
    exit(main())