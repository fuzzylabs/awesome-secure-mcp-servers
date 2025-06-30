#!/usr/bin/env python3
"""
Simple test runner for core functionality
"""

import sys
import os
sys.path.insert(0, 'scripts')

def test_basic_functionality():
    """Test basic functionality of core scripts"""
    print("🧪 Running basic functionality tests...")
    
    # Test 1: Validate script can be imported and run
    try:
        from validate import Validator
        validator = Validator()
        print("✅ Validator imports successfully")
        
        # Test basic status determination
        test_data = {"servers": []}
        validator._validate_data(test_data) 
        print("✅ Validator basic functions work")
    except Exception as e:
        print(f"❌ Validator test failed: {e}")
        return False
    
    # Test 2: Update artifacts script functionality
    try:
        # Read the script and extract the class
        with open('scripts/update-artifacts.py', 'r') as f:
            script_content = f.read()
        
        # Extract just the class definition part
        class_start = script_content.find('class ArtifactsUpdater')
        main_start = script_content.find('def main():')
        class_code = script_content[class_start:main_start]
        
        # Add required imports
        imports = """
import argparse
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Configure logging to suppress during tests
logging.basicConfig(level=logging.ERROR)
"""
        
        exec(imports + class_code)
        updater = locals()['ArtifactsUpdater']()
        
        # Test basic functionality
        status = updater._determine_security_status(95)
        assert status == 'verified-secure', f"Expected 'verified-secure', got {status}"
        print("✅ ArtifactsUpdater basic functions work")
        
        # Test badge formatting
        badges = updater.security_badges
        assert 'verified-secure' in badges, "Missing verified-secure badge"
        print("✅ Security badges configured correctly")
        
    except Exception as e:
        print(f"❌ ArtifactsUpdater test failed: {e}")
        return False
    
    # Test 3: README duplication fix 
    sample_readme = """## Security Status by Category

### Official Servers

</details>
"""
    
    try:
        start_idx, end_idx = updater._find_section_boundaries(sample_readme)
        assert start_idx >= 0, "Should find section start"
        print("✅ Section boundary detection works")
    except Exception as e:
        print(f"❌ Section boundary test failed: {e}")
        return False
    
    print("🎉 All basic functionality tests passed!")
    return True

def test_data_validation():
    """Test data validation with actual project files"""
    print("\n🧪 Testing data validation with project files...")
    
    try:
        from validate import Validator
        validator = Validator()
        
        # Test with actual project files
        result = validator.validate('data/servers.json', 'data/schema.json')
        if result:
            print("✅ Project data validation passes")
        else:
            print("⚠️ Project data validation has issues:")
            for error in validator.errors:
                print(f"  - {error}")
            for warning in validator.warnings:
                print(f"  - WARNING: {warning}")
        
        return result
        
    except Exception as e:
        print(f"❌ Data validation test failed: {e}")
        return False

def test_makefile_commands():
    """Test that Makefile commands work"""
    print("\n🧪 Testing Makefile commands...")
    
    # Test validate command
    result = os.system('make validate >/dev/null 2>&1')
    if result == 0:
        print("✅ make validate works")
    else:
        print("❌ make validate failed")
        return False
    
    return True

if __name__ == '__main__':
    success = True
    
    success &= test_basic_functionality()
    success &= test_data_validation() 
    success &= test_makefile_commands()
    
    print(f"\n{'🎉 All tests passed!' if success else '❌ Some tests failed!'}")
    sys.exit(0 if success else 1)