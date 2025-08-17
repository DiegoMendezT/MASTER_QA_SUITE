#!/usr/bin/env python3
"""
MASTER QA SUITE v2.0 - System Verification Script
Run this to verify all components are properly installed and configured
"""

# MASTER_QA_SUITE
# Project: MASTER_QA_SUITE
# File: verify_setup.py
# Purpose: System verification script for MASTER_QA_SUITE components and dependencies.
# Maintainer: DiegoMendezT / InnerCouncil
# Last updated: 2025-08-10 13:55 UTC
#
# This file is part of the Akashic Records. All changes must be attributed and timestamped.
# Agile Voice Attribution (Full Team):
# - Product Owner: Guides product vision and backlog priorities.
# - Scrum Master: Facilitates process, removes impediments, ensures agile adherence.
# - Development Team: Designers, developers, testers, and specialists responsible for delivery.
# - Stakeholders: Provide input and feedback on product direction and features.
# - Subject Matter Experts: Offer specialized technical or domain knowledge.
# - QA Voice: [Diego Alejandro] — Ensures quality, test coverage, and user advocacy.
# - Shadow QA: [Diego's Shadow] — Represents blindspots, risks, and unspoken challenges.
# - Teacher as Copilot, Gatekeeper as Copilot, Release Captain: AI/InnerCouncil voices for governance, traceability, and decision synthesis.
#
# All major decisions, changes, and logic evolutions must be attributed to one or more of these voices in docs/decision_log.md.

import os
import sys


def verify_imports():
    """Verify all required packages can be imported"""
    print("🔍 Verifying imports...")
    
    required_packages = [
        'selenium',
        'streamlit', 
        'pytest',
        'yaml',
        'chromedriver_autoinstaller',
        'webdriver_manager'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError as e:
            print(f"  ❌ {package} - {e}")
            failed_imports.append(package)
    
    return len(failed_imports) == 0

def verify_file_structure():
    """Verify project structure is complete"""
    print("\n🗂️  Verifying project structure...")
    
    required_files = [
        'conftest.py',
        'pytest.ini',
        'requirements.txt',
        'README.md',
        '.gitignore',
        'config/settings.yaml',
        'pages/base_page.py',
        'tests/test_google.py',
        'drivers/webdriver_factory.py',
        'streamlit_ui/app.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def verify_python_version():
    """Verify Python version"""
    print("\n🐍 Python Version Check...")
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 11:
        print("  ✅ Python version compatible")
        return True
    else:
        print("  ⚠️  Python 3.11+ recommended for optimal compatibility")
        return False

def main():
    """Main verification function"""
    print("MASTER QA SUITE v2.0 - System Verification")
    print("=" * 50)
    
    # Check Python version
    python_ok = verify_python_version()
    
    # Check imports
    imports_ok = verify_imports()
    
    # Check file structure
    files_ok = verify_file_structure()
    
    print("\n" + "=" * 50)
    print("📋 VERIFICATION SUMMARY:")
    
    if python_ok and imports_ok and files_ok:
        print("🎉 ALL CHECKS PASSED!")
        print("\n🚀 Ready to run tests:")
        print("   python -m pytest tests/ -v")
        print("\n🖥️  Ready to launch UI:")
        print("   streamlit run streamlit_ui/app.py")
        return True
    else:
        print("❌ SOME ISSUES FOUND - Please review above")
        return False

if __name__ == "__main__":
    main()
