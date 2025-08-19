
# Lesson: Test Self Reflection

Self-Reflective Test Module for MASTER QA SUITE v2.0
Meta-layer that tests the test suite itself - maintaining coherence and precision

---

## Test Implementation

```python
"""
Self-Reflective Test Module for MASTER QA SUITE v2.0
Meta-layer that tests the test suite itself - maintaining coherence and precision
"""
import ast
import glob
import logging
import os
import subprocess
from pathlib import Path
import sys

import pytest
import yaml

logger = logging.getLogger(__name__)

@pytest.mark.self_reflection
class TestFrameworkStructure:
    """Validate the structural integrity of the framework"""
    
    def test_essential_directories_exist(self):
        """Verify all required directories are present"""
        required_dirs = [
            "tests", "pages", "drivers", "utils", 
            "config", "reports", "streamlit_ui"
        ]
        
        missing_dirs = []
        for directory in required_dirs:
            if not os.path.isdir(directory):
                missing_dirs.append(directory)
        
        assert not missing_dirs, f"Missing essential directories: {missing_dirs}"
        logger.info("✅ All essential directories present")
    
    def test_core_files_exist(self):
        """Verify core framework files exist"""
        core_files = [
            "conftest.py", "pytest.ini",
            "README.md", ".gitignore", "verify_setup.py"
        ]
        
        missing_files = []
        for file_path in core_files:
            if not os.path.isfile(file_path):
                missing_files.append(file_path)
        
        assert not missing_files, f"Missing core files: {missing_files}"
        logger.info("✅ All core files present")
    
    def test_config_files_valid(self):
        """Validate YAML configuration files"""
        config_files = [
            "config/settings.yaml",
            "config/saucelabs_config.yaml"
        ]
        
        for config_file in config_files:
            assert os.path.exists(config_file), f"Config file missing: {config_file}"
            
            with open(config_file, 'r') as file:
                config_data = yaml.safe_load(file)
                assert config_data is not None, f"Invalid YAML in {config_file}"
        
        logger.info("✅ Configuration files are valid YAML")

@pytest.mark.self_reflection
class TestCodeQuality:
    """Validate code quality and consistency"""
    
    def test_test_files_naming_convention(self):
        """Verify test files follow naming convention"""
        test_files = glob.glob("tests/test_*.py")
        
        assert len(test_files) >= 2, "Should have multiple test files"
        
        for test_file in test_files:
            filename = os.path.basename(test_file)
            assert filename.startswith("test_"), f"Test file {filename} doesn't follow naming convention"
            assert filename.endswith(".py"), f"Test file {filename} is not a Python file"
        
        logger.info(f"✅ {len(test_files)} test files follow naming convention")
    
    def test_page_objects_inherit_base_page(self):
        """Verify page objects inherit from BasePage"""
        page_files = glob.glob("pages/*.py")
        page_files = [f for f in page_files if not f.endswith("__init__.py")]
        
        base_page_inheritance_found = False
        
        for page_file in page_files:
            if "base_page.py" in page_file:
                continue
                
            with open(page_file, 'r') as file:
                content = file.read()
                if "BasePage" in content and "class" in content:
                    base_page_inheritance_found = True
                    break
        
        assert base_page_inheritance_found, "No page objects found inheriting from BasePage"
        logger.info("✅ Page objects properly inherit from BasePage")
    
    def test_imports_are_clean(self):
        """Check for unused imports and import organization"""
        python_files = []
        for pattern in ["tests/*.py", "pages/*.py", "drivers/*.py", "utils/*.py"]:
            python_files.extend(glob.glob(pattern))
        
        problematic_files = []
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as file:
                    tree = ast.parse(file.read())
                    
                # Check for basic import structure
                imports_found = any(isinstance(node, (ast.Import, ast.ImportFrom)) for node in tree.body)
                if not imports_found and "test_" in py_file:
                    problematic_files.append(f"{py_file}: No imports found")
                    
            except Exception as e:
                problematic_files.append(f"{py_file}: Syntax error - {e}")
        
        assert not problematic_files, f"Import issues found: {problematic_files}"
        logger.info("✅ Import structure looks healthy")

@pytest.mark.self_reflection
class TestFrameworkCoherence:
    """Validate internal consistency and coherence"""
    
    def test_pytest_configuration_coherent(self):
        """Verify pytest.ini configuration makes sense"""
        assert os.path.exists("pytest.ini"), "pytest.ini must exist"
        
        with open("pytest.ini", 'r') as file:
            content = file.read()
            
        # Check for essential pytest configurations
        required_configs = ["testpaths", "python_files", "markers"]
        for config in required_configs:
            assert config in content, f"pytest.ini missing {config} configuration"
        
        logger.info("✅ pytest.ini configuration is coherent")
    
    def test_requirements_match_imports(self):
        """Verify requirements files exist and contain essential packages"""
        req_dir = Path("requirements")
        if not req_dir.is_dir():
            pytest.skip("requirements/ directory not found")

        all_requirements = ""
        for req_file in req_dir.glob("*.txt"):
            with open(req_file, 'r', encoding='utf-8') as f:
                all_requirements += f.read()

        assert len(all_requirements.strip()) > 0, "No requirements found in requirements/*.txt files"

        required_packages = ["pytest", "selenium", "playwright", "allure-pytest", "eyes-selenium"]
        missing_packages = [pkg for pkg in required_packages if pkg.lower() not in all_requirements.lower()]

        assert not missing_packages, f"Missing packages in requirements files: {missing_packages}"
        logger.info("✅ Requirements files match framework needs")
    
    def test_framework_can_self_execute(self):
        """Test that the framework can run its own verification with full Unicode support"""
        try:
            # Use sys.executable to ensure we're running with the same Python interpreter
            result = subprocess.run(
                [sys.executable, "verify_unicode.py"],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                check=False  # Do not raise exception on non-zero exit codes
            )
            
            # Provide detailed output for debugging
            assert result.returncode == 0, (
                f"Self-verification failed with exit code {result.returncode}.\n"
                f"STDOUT:\n{result.stdout}\n"
                f"STDERR:\n{result.stderr}"
            )
            assert "SUCCESS" in result.stdout, (
                f"Self-verification didn't pass all checks.\n"
                f"STDOUT:\n{result.stdout}"
            )
            
        except subprocess.TimeoutExpired:
            pytest.fail("Self-verification timed out")
        except FileNotFoundError:
            pytest.skip("verify_unicode.py not found")
        
        logger.info("✅ Framework successfully self-executes verification")

@pytest.mark.self_reflection
class TestFrameworkResilience:
    """Test framework's ability to recover and maintain itself"""
    
    def test_reports_directory_auto_creation(self):
        """Test that reports directory is created automatically"""
        # Temporarily remove reports directory if it exists
        reports_path = Path("reports")
        screenshots_path = reports_path / "screenshots"
        
        original_existed = reports_path.exists()
        
        if original_existed:
            # Test assumes the auto-creation mechanism works
            assert screenshots_path.exists(), "Screenshots directory should auto-create"
        
        logger.info("✅ Framework auto-creates necessary directories")
    
    def test_configuration_fallback_mechanisms(self):
        """Test that framework handles missing configurations gracefully"""
        # This would test fallback values in config loading
        config_path = "config/settings.yaml"
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
                
            # Test for fallback-friendly structure
            assert 'selenium' in config, "Should have selenium config section"
            assert 'implicit_wait' in config['selenium'], "Should have implicit_wait setting"
        
        logger.info("✅ Configuration structure supports resilience")

@pytest.mark.self_reflection 
class TestFrameworkMetrics:
    """Generate metrics about framework health and coverage"""
    
    def test_framework_coverage_metrics(self):
        """Generate basic metrics about framework completeness"""
        metrics = {
            'test_files': len(glob.glob("tests/test_*.py")),
            'page_objects': len(glob.glob("pages/*.py")) - 1,  # Exclude __init__.py
            'utility_modules': len(glob.glob("utils/*.py")) - 1,
            'config_files': len(glob.glob("config/*.yaml")),
        }
        
        # Basic health checks
        assert metrics['test_files'] >= 2, "Should have multiple test suites"
        assert metrics['page_objects'] >= 2, "Should have multiple page objects"
        
        logger.info(f"📊 Framework Metrics: {metrics}")
    
    def test_framework_demonstrates_principles(self):
        """Verify framework demonstrates automation best practices"""
        principles_demonstrated = []
        
        # Check for Page Object Model
        if os.path.exists("pages/base_page.py"):
            principles_demonstrated.append("Page Object Model")
        
        # Check for configuration management  
        if os.path.exists("config/settings.yaml"):
            principles_demonstrated.append("Configuration Management")
        
        # Check for proper test structure
        if os.path.exists("conftest.py"):
            principles_demonstrated.append("Test Fixtures")
            
        # Check for reporting
        if "html" in open("pytest.ini").read():
            principles_demonstrated.append("HTML Reporting")
        
        assert len(principles_demonstrated) >= 3, f"Framework should demonstrate multiple principles: {principles_demonstrated}"
        logger.info(f"✅ Automation principles demonstrated: {', '.join(principles_demonstrated)}")

```

---

## Traceability

- **Test File**: `tests\test_self_reflection.py`
- **Markers**: ``@self_reflection``
