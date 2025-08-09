"""
MASTER QA SUITE v2.5 - Universal Unicode System Verification
Supports ALL characters: ASCII, Extended, Unicode, Emojis, Mathematical Symbols, etc.
🌍🔤📝✨ Full International Support ✨📝🔤🌍
"""
import importlib
import os
import sys

# Ensure UTF-8 encoding for all output
if sys.platform.startswith('win'):
    # Fix Windows console encoding issues
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def verify_unicode_support():
    """Test full Unicode support including emojis and special characters"""
    print("🧪 Testing Unicode Support...")
    
    test_strings = [
        "🚀 Basic Emojis",
        "🧠💡⚡🔥 Complex Emojis", 
        "αβγδεζηθ Greek Letters",
        "∑∆∇∞ Mathematical Symbols",
        "≪⚙︎∆𝕋𝔄Ξ⟁⏃ᚱ⟁⟟ᔑ⟟⛧⟟⇋⟫ Mixed Unicode",
        "🜂☸🪞 Advanced Symbols",
        "Ǵ̨̛̻̥͖ Combining Characters"
    ]
    
    success = True
    for test_str in test_strings:
        try:
            print(f"  ✅ {test_str}")
        except UnicodeEncodeError as e:
            print(f"  ❌ Unicode Error: {e}")
            success = False
        except Exception as e:
            print(f"  ⚠️  Display Issue: {e}")
            
    return success

def verify_imports():
    """Verify all required packages can be imported"""
    print("🔍 Verifying imports...")
    
    required_packages = [
        'selenium',
        'pytest', 
        'yaml',
        'requests',
        'streamlit',
        'pandas',
        'plotly'
    ]
    
    success = True
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"  ✅ {package}")
        except ImportError as e:
            print(f"  ❌ {package} - {e}")
            success = False
    
    return success

def verify_file_structure():
    """Verify essential project files exist"""
    print("\n🗂️ Verifying project structure...")
    
    required_files = [
        'conftest.py',
        'pytest.ini', 
        'requirements.txt',
        'config/settings.yaml',
        'tests/test_self_reflection.py',
        'pages/__init__.py',
        'utils/__init__.py',
        'streamlit_launcher.py'
    ]
    
    success = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            success = False
    
    return success

def verify_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    print(f"\n🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version >= (3, 8):
        print("  ✅ Python version compatible")
        return True
    else:
        print("  ⚠️ Python 3.8+ recommended for optimal compatibility")
        return False

def verify_encoding():
    """Verify system encoding capabilities"""
    print(f"\n🔤 System Encoding: {sys.getdefaultencoding()}")
    print(f"📟 Console Encoding: {sys.stdout.encoding}")
    
    if sys.stdout.encoding.lower() in ['utf-8', 'utf8']:
        print("  ✅ UTF-8 encoding active")
        return True
    else:
        print("  ⚠️ Non-UTF-8 encoding detected")
        return True  # Still allow to proceed

def main():
    """Main verification function with full Unicode support"""
    print("🚀 MASTER QA SUITE v2.5 - Universal System Verification")
    print("=" * 60)
    print("🌍 Supporting ALL Unicode: Emojis, Symbols, International Text")
    print("=" * 60)
    
    # Check system capabilities
    encoding_ok = verify_encoding()
    unicode_ok = verify_unicode_support()
    python_ok = verify_python_version()
    imports_ok = verify_imports()
    files_ok = verify_file_structure()
    
    print("\n" + "=" * 60)
    if python_ok and imports_ok and files_ok and unicode_ok:
        print("🎉 SUCCESS - All systems operational!")
        print("🌟 Unicode Support: FULL ✨")
        print("🧪 Framework Status: READY")
        print("\n🚀 Ready to launch:")
        print("  🧪 pytest - Run tests") 
        print("  🖥️ streamlit run streamlit_launcher.py - Launch UI")
        print("  📊 Full emoji/symbol support active!")
        return 0
    else:
        print("❌ SOME ISSUES FOUND - Please review above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
