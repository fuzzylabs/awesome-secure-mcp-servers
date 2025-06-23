#!/usr/bin/env python3
"""
Security Report Generator for MCP Servers
=========================================

This script generates human-readable security reports from scan results.
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

class SecurityReportGenerator:
    """Generate security reports from scan results."""
    
    def __init__(self):
        self.report_lines = []
    
    def generate_report(self, scan_results: Dict[str, Any]) -> str:
        """Generate a comprehensive security report."""
        self.report_lines = []
        
        # Header
        self._add_header(scan_results)
        
        # Summary
        self._add_summary(scan_results)
        
        # Detailed results for each server
        for result in scan_results.get('results', []):
            if 'error' in result:
                self._add_error_result(result)
            else:
                self._add_server_result(result)
        
        # Footer
        self._add_footer()
        
        return '\n'.join(self.report_lines)
    
    def _add_header(self, scan_results: Dict[str, Any]):
        """Add report header."""
        self.report_lines.extend([
            "# MCP Server Security Validation Report",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"**Scanner Version:** {scan_results.get('scanner_version', 'unknown')}",
            f"**Servers Scanned:** {scan_results.get('total_servers_scanned', 0)}",
            ""
        ])
    
    def _add_summary(self, scan_results: Dict[str, Any]):
        """Add summary section."""
        results = scan_results.get('results', [])
        if not results:
            return
        
        # Calculate summary statistics
        total_servers = len(results)
        error_count = len([r for r in results if 'error' in r])
        successful_scans = total_servers - error_count
        
        if successful_scans == 0:
            return
        
        # Get score distribution
        scores = []
        status_counts = {'verified-secure': 0, 'conditional': 0, 'under-review': 0, 'not-recommended': 0}
        
        for result in results:
            if 'error' not in result:
                for version in result.get('versions', []):
                    if 'overall_score' in version:
                        scores.append(version['overall_score'])
                    
                    # Count latest version statuses (assume first version is latest)
                    if version == result.get('versions', [{}])[0]:
                        version_status = self._determine_status_from_score(version.get('overall_score', 0))
                        if version_status in status_counts:
                            status_counts[version_status] += 1
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        self.report_lines.extend([
            "## Summary",
            "",
            f"- **Total Servers:** {total_servers}",
            f"- **Successful Scans:** {successful_scans}",
            f"- **Failed Scans:** {error_count}",
            f"- **Average Security Score:** {avg_score:.1f}/100",
            "",
            "### Security Status Distribution",
            "",
            f"- 🛡️ **Verified Secure:** {status_counts['verified-secure']} servers",
            f"- ⚠️ **Conditional:** {status_counts['conditional']} servers", 
            f"- 🔄 **Under Review:** {status_counts['under-review']} servers",
            f"- ❌ **Not Recommended:** {status_counts['not-recommended']} servers",
            ""
        ])
    
    def _add_server_result(self, result: Dict[str, Any]):
        """Add detailed results for a single server."""
        server_name = result.get('server_name', 'Unknown')
        repository = result.get('repository', '')
        
        self.report_lines.extend([
            f"## {server_name}",
            "",
            f"**Repository:** {repository}",
            f"**Scan Date:** {result.get('scan_timestamp', 'Unknown')}",
            ""
        ])
        
        # Add version results
        versions = result.get('versions', [])
        if not versions:
            self.report_lines.extend([
                "⚠️ No version information available",
                ""
            ])
            return
        
        for version_result in versions:
            self._add_version_result(version_result)
    
    def _add_version_result(self, version_result: Dict[str, Any]):
        """Add results for a specific version."""
        version = version_result.get('version', 'Unknown')
        overall_score = version_result.get('overall_score', 0)
        status = self._determine_status_from_score(overall_score)
        status_emoji = self._get_status_emoji(status)
        
        self.report_lines.extend([
            f"### Version {version} {status_emoji}",
            "",
            f"**Overall Security Score:** {overall_score}/100",
            ""
        ])
        
        # Add detailed scan results
        scan_types = [
            ('static_analysis', 'Static Code Analysis'),
            ('dependency_scan', 'Dependency Vulnerability Scan'),
            ('tool_poisoning_check', 'Tool Poisoning Detection'),
            ('container_scan', 'Container Security Scan'),
            ('security_documentation_check', 'Security Documentation Review')
        ]
        
        for scan_key, scan_name in scan_types:
            if scan_key in version_result:
                self._add_scan_result(scan_name, version_result[scan_key])
        
        # Add recommendations
        recommendations = version_result.get('recommendations', [])
        if recommendations:
            self.report_lines.extend([
                "#### Recommendations",
                ""
            ])
            for rec in recommendations:
                self.report_lines.append(f"- {rec}")
            self.report_lines.append("")
        
        self.report_lines.append("---")
        self.report_lines.append("")
    
    def _add_scan_result(self, scan_name: str, scan_result: Dict[str, Any]):
        """Add results for a specific scan type."""
        status = scan_result.get('status', 'unknown')
        score = scan_result.get('score', 0)
        details = scan_result.get('details', 'No details available')
        issues = scan_result.get('issues_found', 0)
        
        status_emoji = {
            'pass': '✅',
            'warning': '⚠️',
            'fail': '❌',
            'not-applicable': '➖'
        }.get(status, '❓')
        
        self.report_lines.extend([
            f"#### {scan_name} {status_emoji}",
            "",
            f"**Score:** {score}/100",
            f"**Status:** {status.replace('-', ' ').title()}",
            f"**Issues Found:** {issues}",
            f"**Details:** {details}",
            ""
        ])
        
        # Add specific details based on scan type
        if scan_result.get('vulnerabilities'):
            self._add_vulnerability_details(scan_result['vulnerabilities'])
        
        if scan_result.get('suspicious_patterns'):
            self._add_suspicious_patterns(scan_result['suspicious_patterns'])
        
        if scan_result.get('security_issues'):
            self._add_security_issues(scan_result['security_issues'])
    
    def _add_vulnerability_details(self, vulnerabilities):
        """Add vulnerability details to the report."""
        if isinstance(vulnerabilities, dict):
            # NPM audit format
            total = sum(vulnerabilities.values()) if vulnerabilities else 0
            if total > 0:
                self.report_lines.extend([
                    "**Vulnerabilities by Severity:**",
                    ""
                ])
                for severity, count in vulnerabilities.items():
                    if count > 0:
                        self.report_lines.append(f"- {severity.title()}: {count}")
                self.report_lines.append("")
        elif isinstance(vulnerabilities, list):
            # Safety/other format
            if vulnerabilities:
                self.report_lines.extend([
                    "**Vulnerability Details:**",
                    ""
                ])
                for vuln in vulnerabilities[:5]:  # Limit to first 5
                    vuln_id = vuln.get('id', 'Unknown')
                    vuln_desc = vuln.get('description', 'No description')
                    self.report_lines.append(f"- **{vuln_id}:** {vuln_desc}")
                
                if len(vulnerabilities) > 5:
                    self.report_lines.append(f"- ... and {len(vulnerabilities) - 5} more")
                self.report_lines.append("")
    
    def _add_suspicious_patterns(self, patterns):
        """Add suspicious pattern details."""
        if patterns:
            self.report_lines.extend([
                "**Suspicious Patterns Found:**",
                ""
            ])
            for pattern in patterns[:3]:  # Limit to first 3
                file_name = pattern.get('file', 'Unknown file')
                matches = pattern.get('matches', 0)
                self.report_lines.append(f"- {file_name}: {matches} match(es)")
            
            if len(patterns) > 3:
                self.report_lines.append(f"- ... and {len(patterns) - 3} more files")
            self.report_lines.append("")
    
    def _add_security_issues(self, issues):
        """Add security issue details."""
        if issues:
            self.report_lines.extend([
                "**Security Issues:**",
                ""
            ])
            for issue in issues:
                self.report_lines.append(f"- {issue}")
            self.report_lines.append("")
    
    def _add_error_result(self, result: Dict[str, Any]):
        """Add error result for failed scans."""
        server_name = result.get('server_name', 'Unknown')
        error = result.get('error', 'Unknown error')
        
        self.report_lines.extend([
            f"## {server_name} ❌",
            "",
            f"**Scan Failed:** {error}",
            f"**Timestamp:** {result.get('scan_timestamp', 'Unknown')}",
            "",
            "---",
            ""
        ])
    
    def _add_footer(self):
        """Add report footer."""
        self.report_lines.extend([
            "",
            "---",
            "",
            "*This report was automatically generated by the MCP Server Security Scanner.*",
            "",
            "**Legend:**",
            "- 🛡️ Verified Secure (Score: 85-100)",
            "- ⚠️ Conditional (Score: 70-84)", 
            "- 🔄 Under Review (Score: 50-69)",
            "- ❌ Not Recommended (Score: 0-49)",
            "",
            "**Note:** Security validations are performed to the best of our ability with available tools and methods. Users should perform their own security assessments for production use."
        ])
    
    def _determine_status_from_score(self, score: int) -> str:
        """Determine security status from score."""
        if score >= 85:
            return 'verified-secure'
        elif score >= 70:
            return 'conditional'
        elif score >= 50:
            return 'under-review'
        else:
            return 'not-recommended'
    
    def _get_status_emoji(self, status: str) -> str:
        """Get emoji for security status."""
        return {
            'verified-secure': '🛡️',
            'conditional': '⚠️',
            'under-review': '🔄',
            'not-recommended': '❌',
            'deprecated': '🗑️'
        }.get(status, '❓')


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate security report from scan results'
    )
    
    parser.add_argument(
        '--scan-results',
        required=True,
        help='JSON file containing scan results'
    )
    
    parser.add_argument(
        '--output',
        required=True,
        help='Output markdown file for the report'
    )
    
    args = parser.parse_args()
    
    # Load scan results
    try:
        with open(args.scan_results, 'r') as f:
            scan_results = json.load(f)
    except Exception as e:
        print(f"Error loading scan results: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Generate report
    generator = SecurityReportGenerator()
    report = generator.generate_report(scan_results)
    
    # Save report
    try:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Security report generated: {args.output}")
    except Exception as e:
        print(f"Error saving report: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()