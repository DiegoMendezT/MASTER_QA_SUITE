"""
MASTER QA SUITE v2.5 - Clean System Verification (ASCII only)
No Unicode characters - Windows compatible
"""
import importlib
import os
import sys


def verify_imports():
    """Verify all required packages can be imported"""
    print("Verifying imports...")
    
    required_packages = [
        'selenium',
        'pytest',
        'yaml',
        'requests',
        'streamlit'
    ]
    
    success = True
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"  OK {package}")
        except ImportError as e:
            print(f"  FAILED {package} - {e}")
            success = False
    
    return success

def verify_file_structure():
    """Verify essential project files exist"""
    print("\nVerifying project structure...")
    
    required_files = [
        'conftest.py',
        'pytest.ini', 
        'requirements.txt',
        'config/settings.yaml',
        'tests/test_self_reflection.py',
        'pages/__init__.py',
        'utils/__init__.py'
    ]
    
    success = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  OK {file_path}")
        else:
            print(f"  MISSING {file_path}")
            success = False
    
    return success

def verify_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    print(f"\nPython version: {version.major}.{version.minor}.{version.micro}")
    
    if version >= (3, 8):
        print("  OK Python version compatible")
        return True
    else:
        print("  WARNING Python 3.8+ recommended")
        return False

def main():
    """Main verification function"""
    print("MASTER QA SUITE v2.5 - System Verification")
    print("=" * 50)
    
    # Check Python version
    python_ok = verify_python_version()
    
    # Check imports
    imports_ok = verify_imports()
    
    # Check file structure
    files_ok = verify_file_structure()
    
    print("\n" + "=" * 50)
    if python_ok and imports_ok and files_ok:
        print("SUCCESS - All systems operational!")
        print("\nReady to launch:")
        print("  pytest - Run tests")
        print("  streamlit run streamlit_launcher.py - Launch UI")
        return 0
    else:
        print("ISSUES FOUND - Please review above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
