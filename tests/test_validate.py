#!/usr/bin/env python3
"""
Tests for validate.py script
"""

import unittest
import tempfile
import json
import os
import sys

# Add scripts directory to path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from validate import Validator


class TestValidator(unittest.TestCase):
    """Test cases for Validator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = Validator()
        
        # Valid schema
        self.valid_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "schema_version": {"type": "string"},
                "last_updated": {"type": "string"},
                "servers": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "slug": {"type": "string", "pattern": "^[a-z0-9-]+$"},
                            "category": {"type": "string"},
                            "versions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "version": {"type": "string"},
                                        "security_status": {"type": "string"}
                                    },
                                    "required": ["version", "security_status"]
                                }
                            }
                        },
                        "required": ["name", "slug", "category", "versions"]
                    }
                }
            },
            "required": ["schema_version", "servers"]
        }
        
        # Valid servers data
        self.valid_servers = {
            "schema_version": "1.0.0",
            "last_updated": "2025-01-01T00:00:00Z",
            "servers": [
                {
                    "name": "Test Server One",
                    "slug": "test-server-one",
                    "category": "official",
                    "versions": [
                        {
                            "version": "1.0.0",
                            "security_status": "verified-secure"
                        }
                    ]
                },
                {
                    "name": "Test Server Two", 
                    "slug": "test-server-two",
                    "category": "community",
                    "versions": [
                        {
                            "version": "2.1.0",
                            "security_status": "conditional"
                        }
                    ]
                }
            ]
        }

    def test_valid_data_passes_validation(self):
        """Test that valid data passes all validation checks."""
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as data_file, \
             tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as schema_file:
            
            json.dump(self.valid_servers, data_file)
            data_file.flush()
            
            json.dump(self.valid_schema, schema_file)
            schema_file.flush()
            
            try:
                result = self.validator.validate(data_file.name, schema_file.name)
                self.assertTrue(result, "Valid data should pass validation")
                self.assertEqual(len(self.validator.errors), 0)
            finally:
                os.unlink(data_file.name)
                os.unlink(schema_file.name)

    def test_invalid_slug_format_detected(self):
        """Test that invalid slug formats are detected."""
        invalid_data = self.valid_servers.copy()
        invalid_data['servers'][0]['slug'] = 'Invalid_Slug!'  # Contains invalid characters
        
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as data_file, \
             tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as schema_file:
            
            json.dump(invalid_data, data_file)
            data_file.flush()
            
            json.dump(self.valid_schema, schema_file)
            schema_file.flush()
            
            try:
                result = self.validator.validate(data_file.name, schema_file.name)
                self.assertFalse(result, "Invalid slug should fail validation")
                self.assertGreater(len(self.validator.errors), 0)
                
                # Check that slug error is mentioned (either custom or schema validation)
                slug_error_found = any('slug' in error.lower() for error in self.validator.errors)
                self.assertTrue(slug_error_found, "Should detect invalid slug format")
            finally:
                os.unlink(data_file.name)
                os.unlink(schema_file.name)

    def test_duplicate_slugs_detected(self):
        """Test that duplicate slugs are detected."""
        invalid_data = self.valid_servers.copy()
        invalid_data['servers'][1]['slug'] = invalid_data['servers'][0]['slug']  # Duplicate slug
        
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as data_file, \
             tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as schema_file:
            
            json.dump(invalid_data, data_file)
            data_file.flush()
            
            json.dump(self.valid_schema, schema_file)
            schema_file.flush()
            
            try:
                result = self.validator.validate(data_file.name, schema_file.name)
                self.assertFalse(result, "Duplicate slugs should fail validation")
                
                # Check that duplicate error is mentioned
                duplicate_error_found = any('Duplicate slug' in error for error in self.validator.errors)
                self.assertTrue(duplicate_error_found, "Should detect duplicate slugs")
            finally:
                os.unlink(data_file.name)
                os.unlink(schema_file.name)

    def test_similar_names_warning(self):
        """Test that similar names generate warnings."""
        warning_data = self.valid_servers.copy()
        warning_data['servers'][1]['name'] = warning_data['servers'][0]['name'].upper()  # Same name, different case
        
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as data_file, \
             tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as schema_file:
            
            json.dump(warning_data, data_file)
            data_file.flush()
            
            json.dump(self.valid_schema, schema_file)
            schema_file.flush()
            
            try:
                self.validator.validate(data_file.name, schema_file.name)
                
                # Should generate warning about potential duplicate names
                duplicate_warning_found = any('duplicate name' in warning.lower() for warning in self.validator.warnings)
                self.assertTrue(duplicate_warning_found, "Should warn about potential duplicate names")
            finally:
                os.unlink(data_file.name)
                os.unlink(schema_file.name)

    def test_missing_versions_warning(self):
        """Test that servers with no versions generate warnings."""
        warning_data = self.valid_servers.copy()
        warning_data['servers'][0]['versions'] = []  # No versions
        
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as data_file, \
             tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as schema_file:
            
            json.dump(warning_data, data_file)
            data_file.flush()
            
            json.dump(self.valid_schema, schema_file)
            schema_file.flush()
            
            try:
                self.validator.validate(data_file.name, schema_file.name)
                
                # Should generate warning about no versions
                no_versions_warning = any('No versions' in warning for warning in self.validator.warnings)
                self.assertTrue(no_versions_warning, "Should warn about servers with no versions")
            finally:
                os.unlink(data_file.name)
                os.unlink(schema_file.name)

    def test_non_semantic_version_warning(self):
        """Test that non-semantic versions generate warnings."""
        warning_data = self.valid_servers.copy()
        warning_data['servers'][0]['versions'][0]['version'] = 'latest'  # Non-semantic version
        
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as data_file, \
             tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as schema_file:
            
            json.dump(warning_data, data_file)
            data_file.flush()
            
            json.dump(self.valid_schema, schema_file)
            schema_file.flush()
            
            try:
                self.validator.validate(data_file.name, schema_file.name)
                
                # Should generate warning about version format
                version_warning = any('may not be semantic' in warning for warning in self.validator.warnings)
                self.assertTrue(version_warning, "Should warn about non-semantic versions")
            finally:
                os.unlink(data_file.name)
                os.unlink(schema_file.name)

    def test_schema_validation_error(self):
        """Test that schema validation errors are properly handled."""
        invalid_data = {"invalid": "structure"}  # Missing required fields
        
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as data_file, \
             tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as schema_file:
            
            json.dump(invalid_data, data_file)
            data_file.flush()
            
            json.dump(self.valid_schema, schema_file)
            schema_file.flush()
            
            try:
                result = self.validator.validate(data_file.name, schema_file.name)
                self.assertFalse(result, "Invalid schema should fail validation")
                self.assertGreater(len(self.validator.errors), 0)
                
                # Should have schema validation error
                schema_error = any('Schema validation error' in error for error in self.validator.errors)
                self.assertTrue(schema_error, "Should detect schema validation errors")
            finally:
                os.unlink(data_file.name)
                os.unlink(schema_file.name)

    def test_file_loading_error_handling(self):
        """Test error handling for file loading issues."""
        # Test with non-existent file
        result = self.validator.validate('/nonexistent/file.json', '/nonexistent/schema.json')
        self.assertFalse(result, "Should handle missing files gracefully")


if __name__ == '__main__':
    unittest.main()