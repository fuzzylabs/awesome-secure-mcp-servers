#!/usr/bin/env python3
"""
Tests for update-artifacts.py script
"""

import unittest
import tempfile
import json
import os
from datetime import datetime
import sys

# Add scripts directory to path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from update_artifacts import ArtifactsUpdater


class TestArtifactsUpdater(unittest.TestCase):
    """Test cases for ArtifactsUpdater class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.updater = ArtifactsUpdater()
        
        # Sample servers data
        self.sample_servers = {
            "schema_version": "1.0.0",
            "last_updated": "2025-01-01T00:00:00Z",
            "servers": [
                {
                    "name": "Test Server",
                    "slug": "test-server",
                    "repository": "https://github.com/test/repo",
                    "category": "official",
                    "description": "Test server for testing",
                    "maintainer": {
                        "name": "Test Maintainer",
                        "type": "official",
                        "contact": "test@example.com"
                    },
                    "versions": [
                        {
                            "version": "1.0.0",
                            "release_date": "2024-01-01",
                            "security_status": "under-review",
                            "is_recommended": false,
                            "security_scan": {
                                "scan_date": "2024-01-01T00:00:00Z",
                                "scanner_version": "1.0.0",
                                "static_analysis": {
                                    "status": "pass",
                                    "details": "No issues found",
                                    "score": 100
                                },
                                "dependency_scan": {
                                    "status": "pass", 
                                    "details": "No vulnerabilities",
                                    "score": 100
                                },
                                "tool_poisoning_check": {
                                    "status": "pass",
                                    "details": "No tool poisoning detected",
                                    "score": 100
                                },
                                "overall_score": 100
                            },
                            "vulnerabilities": []
                        }
                    ],
                    "mcp_protocol_versions": ["2024-11-05"],
                    "tags": ["test"]
                }
            ]
        }
        
        # Sample scan results
        self.sample_scan_results = {
            "scan_date": "2025-01-01T12:00:00Z",
            "scanner_version": "1.2.0",
            "results": [
                {
                    "server_slug": "test-server",
                    "scanner_version": "1.2.0",
                    "versions": [
                        {
                            "version": "1.0.0",
                            "scan_date": "2025-01-01T12:00:00Z",
                            "static_analysis": {
                                "status": "pass",
                                "details": "Updated: No issues found",
                                "score": 95
                            },
                            "dependency_scan": {
                                "status": "warning",
                                "details": "Updated: 1 minor vulnerability",
                                "score": 90
                            },
                            "mcp_security_scan": {
                                "status": "pass",
                                "details": "Updated: No MCP threats",
                                "score": 100
                            },
                            "overall_score": 95
                        }
                    ]
                }
            ]
        }
        
        # Sample README content
        self.sample_readme = """# Test README

Some intro content.

## Security Status by Category

**Last Updated:** Old timestamp
**Total Servers:** 0

### Official Servers

| Server | Version | Security Status | Description |
|--------|---------|----------------|-------------|

---

## 📊 Detailed Security Assessments

_Click on server scores above to jump to detailed security breakdowns:_

"""

    def test_status_mapping(self):
        """Test security status score mapping."""
        self.assertEqual(self.updater._determine_security_status(95), 'verified-secure')
        self.assertEqual(self.updater._determine_security_status(75), 'conditional')
        self.assertEqual(self.updater._determine_security_status(60), 'under-review')
        self.assertEqual(self.updater._determine_security_status(30), 'not-recommended')

    def test_security_badge_formatting(self):
        """Test security badge formatting."""
        badges = self.updater.security_badges
        self.assertIn('verified-secure', badges)
        self.assertIn('🛡️', badges['verified-secure'])
        self.assertIn('⚠️', badges['conditional'])
        self.assertIn('❌', badges['not-recommended'])

    def test_update_servers_data(self):
        """Test updating servers data with scan results."""
        updated_data = self.updater._update_servers_data(
            self.sample_servers, 
            self.sample_scan_results
        )
        
        # Check that data was updated
        self.assertNotEqual(updated_data['last_updated'], self.sample_servers['last_updated'])
        
        # Check that server was updated
        server = updated_data['servers'][0]
        version = server['versions'][0]
        
        # Should now be verified-secure with score 95
        self.assertEqual(version['security_status'], 'verified-secure')
        self.assertEqual(version['security_scan']['overall_score'], 95)
        self.assertTrue(version['is_recommended'])

    def test_security_details_generation(self):
        """Test generation of detailed security assessments."""
        version_data = self.sample_servers['servers'][0]['versions'][0]
        details = self.updater._generate_security_details(version_data, 'test-server')
        
        self.assertIn('Security Assessment:', details)
        self.assertIn('MCP-Specific Security', details)
        self.assertIn('Third-Party Dependencies', details)
        self.assertIn('Code Security Analysis', details)

    def test_find_section_boundaries(self):
        """Test README section boundary detection."""
        start_idx, end_idx = self.updater._find_section_boundaries(self.sample_readme)
        
        lines = self.sample_readme.split('\n')
        # Should find the Security Status section
        self.assertGreater(start_idx, 0)
        self.assertIn('Security Status by Category', lines[start_idx])

    def test_no_duplication_in_generation(self):
        """Test that README generation doesn't create duplicates."""
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.md', delete=False) as readme_file:
            readme_file.write(self.sample_readme)
            readme_file.flush()
            
            # Generate new content
            new_content = self.updater._generate_readme(readme_file.name, self.sample_servers)
            
            # Count occurrences of section headers
            official_count = new_content.count('### Official Servers')
            assessments_count = new_content.count('## 📊 Detailed Security Assessments')
            
            # Should only appear once each
            self.assertEqual(official_count, 1, "Official Servers section duplicated")
            self.assertEqual(assessments_count, 1, "Security Assessments section duplicated")
            
            # Clean up
            os.unlink(readme_file.name)

    def test_dry_run_mode(self):
        """Test dry-run mode doesn't write files."""
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as servers_file, \
             tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as scan_file, \
             tempfile.NamedTemporaryFile(mode='w+', suffix='.md', delete=False) as readme_file:
            
            # Write test data
            json.dump(self.sample_servers, servers_file)
            servers_file.flush()
            
            json.dump(self.sample_scan_results, scan_file)
            scan_file.flush()
            
            readme_file.write(self.sample_readme)
            readme_file.flush()
            
            # Get original modification times
            servers_mtime = os.path.getmtime(servers_file.name)
            readme_mtime = os.path.getmtime(readme_file.name)
            
            # Run in dry-run mode
            try:
                self.updater.update_and_generate(
                    servers_file.name,
                    scan_file.name, 
                    readme_file.name,
                    dry_run=True
                )
                
                # Files should not have been modified
                self.assertEqual(os.path.getmtime(servers_file.name), servers_mtime)
                self.assertEqual(os.path.getmtime(readme_file.name), readme_mtime)
                
            finally:
                # Clean up
                os.unlink(servers_file.name)
                os.unlink(scan_file.name)
                os.unlink(readme_file.name)

    def test_awaiting_scan_detection(self):
        """Test detection of servers awaiting scan."""
        # Create version with 'Repository not available'
        awaiting_version = {
            'security_scan': {
                'static_analysis': {
                    'details': 'Repository not available'
                }
            }
        }
        
        self.assertTrue(self.updater._is_awaiting_scan(awaiting_version))
        
        # Normal version should not be awaiting scan
        normal_version = self.sample_servers['servers'][0]['versions'][0]
        self.assertFalse(self.updater._is_awaiting_scan(normal_version))

    def test_security_score_formatting(self):
        """Test security score formatting with clickable links."""
        version_data = self.sample_servers['servers'][0]['versions'][0]
        score_text = self.updater._get_security_score(version_data, 'test-server')
        
        self.assertIn('📊 Score:', score_text)
        self.assertIn('/100', score_text)
        self.assertIn('#security-details-test-server', score_text)


if __name__ == '__main__':
    unittest.main()