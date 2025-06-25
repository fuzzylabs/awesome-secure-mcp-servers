#!/usr/bin/env python3
"""
Data and Schema Validation Script
=================================

This script validates the servers.json file against the JSON schema
and performs additional semantic data validation.
"""

import argparse
import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Any

import jsonschema

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Validator:
    """Validates servers.json against the schema and custom rules."""

    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate(self, data_file: str, schema_file: str) -> bool:
        """Perform both schema and data validation."""
        logger.info("Starting validation...")
        try:
            data = self._load_json_file(data_file)
            schema = self._load_json_file(schema_file)

            # 1. JSON Schema Validation
            schema_valid = self._validate_schema(data, schema)
            if not schema_valid:
                self.print_results()
                return False

            # 2. Custom Data Validation
            self._validate_data(data)

            self.print_results()
            return len(self.errors) == 0

        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return False

    def _load_json_file(self, file_path: str) -> Dict:
        """Load and parse JSON file."""
        with open(file_path, 'r') as f:
            return json.load(f)

    def _validate_schema(self, data: Dict, schema: Dict) -> bool:
        """Validate data against JSON schema."""
        logger.info("Performing JSON schema validation...")
        try:
            jsonschema.validate(instance=data, schema=schema)
            logger.info("JSON schema validation passed.")
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.errors.append(f"Schema validation error: {e.message} at {e.json_path}")
            return False

    def _validate_data(self, data: Dict):
        """Perform custom data validation checks."""
        logger.info("Performing custom data validation...")
        servers = data.get('servers', [])
        self._check_for_duplicates(servers)
        for i, server in enumerate(servers):
            self._validate_server(server, i)

    def _validate_server(self, server: Dict, index: int):
        """Validate a single server entry."""
        server_prefix = f"Server {index} ({server.get('name', 'unnamed')})"

        # Validate slug format
        if 'slug' in server and not re.match(r'^[a-z0-9-]+$', server['slug']):
            self.errors.append(f"{server_prefix}: Invalid slug format '{server['slug']}'")

        # Validate versions
        versions = server.get('versions', [])
        if not versions:
            self.warnings.append(f"{server_prefix}: No versions defined.")
        for i, version in enumerate(versions):
            self._validate_version(version, f"{server_prefix} version {i}")

    def _validate_version(self, version: Dict, prefix: str):
        """Validate a single version entry."""
        # Validate version format (simple semver check)
        if 'version' in version and not re.match(r'^\d+\.\d+\.\d+', version['version']):
            self.warnings.append(f"{prefix}: Version '{version['version']}' may not be semantic.")

    def _check_for_duplicates(self, servers: List[Dict]):
        """Check for duplicate slugs and names."""
        slugs = set()
        names = set()
        for i, server in enumerate(servers):
            if 'slug' in server:
                if server['slug'] in slugs:
                    self.errors.append(f"Duplicate slug '{server['slug']}' at server index {i}")
                slugs.add(server['slug'])
            if 'name' in server:
                if server['name'].lower() in names:
                    self.warnings.append(f"Potential duplicate name '{server['name']}' at server index {i}")
                names.add(server['name'].lower())

    def print_results(self):
        """Print validation errors and warnings."""
        logger.info("Validation results:")
        if self.errors:
            logger.error("Errors found:")
            for error in self.errors:
                logger.error(f"- {error}")
        if self.warnings:
            logger.warning("Warnings found:")
            for warning in self.warnings:
                logger.warning(f"- {warning}")
        if not self.errors and not self.warnings:
            logger.info("All validation checks passed.")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Validate server data and schema.')
    parser.add_argument('--data', default='data/servers.json', help='Path to the data file')
    parser.add_argument('--schema', default='data/schema.json', help='Path to the schema file')
    args = parser.parse_args()

    validator = Validator()
    if not validator.validate(args.data, args.schema):
        logger.error("Validation failed.")
        exit(1)
    else:
        logger.info("Validation successful.")

if __name__ == '__main__':
    main()
