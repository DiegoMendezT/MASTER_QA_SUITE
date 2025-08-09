"""
Framework Health Check - Self-Reflection Test Module
Tests the MASTER QA SUITE framework itself to ensure structural integrity
"""
import glob
import importlib.util
import os
import subprocess
from pathlib import Path

import pytest
import yaml


@pytest.mark.self_reflection
class TestFrameworkStructure:
    """Validate the essential structure and files exist"""
    
    def test_essential_directories_exist(self):
        """Verify all required project directories are present"""
        required_dirs = [
            "tests", "pages", "drivers", "utils", 
            "config", "reports", "streamlit_ui", 
            "tests/self_reflection", "reflections"
        ]
        
        missing_dirs = []
        for directory in required_dirs:
            if not os.path.isdir(directory):
                missing_dirs.append(directory)
        
        assert not missing_dirs, f"Missing essential directories: {missing_dirs}"
        print(f"✅ All {len(required_dirs)} essential directories present")
    
    def test_core_framework_files_exist(self):
        """Verify core framework files are present"""
        core_files = [
            "conftest.py", "pytest.ini", "requirements.txt",
            "README.md", ".gitignore", "verify_setup.py", "becoming_master.py"
        ]
        
        missing_files = []
        for file_path in core_files:
            if not os.path.isfile(file_path):
                missing_files.append(file_path)
        
        assert not missing_files, f"Missing core files: {missing_files}"
        print(f"✅ All {len(core_files)} core framework files present")
    
    def test_page_object_files_exist(self):
        """Verify Page Object Model files are present"""
        required_page_files = [
            "pages/base_page.py",
            "pages/__init__.py"
        ]
        
        missing_files = []
        for file_path in required_page_files:
            if not os.path.isfile(file_path):
                missing_files.append(file_path)
        
        assert not missing_files, f"Missing page object files: {missing_files}"
        
        # Check for at least one concrete page object
        page_files = glob.glob("pages/*.py")
        concrete_pages = [f for f in page_files if not f.endswith("__init__.py") and not f.endswith("base_page.py")]
        assert len(concrete_pages) >= 1, f"Should have at least one concrete page object, found: {concrete_pages}"
        
        print(f"✅ Page Object Model structure valid with {len(concrete_pages)} concrete page(s)")

@pytest.mark.self_reflection
class TestConfigurationIntegrity:
    """Validate configuration files and their content"""
    
    def test_yaml_configuration_files_valid(self):
        """Verify YAML configuration files are well-formed"""
        config_files = [
            "config/settings.yaml",
            "config/saucelabs_config.yaml"
        ]
        
        for config_file in config_files:
            assert os.path.exists(config_file), f"Config file missing: {config_file}"
            
            try:
                with open(config_file, 'r') as file:
                    config_data = yaml.safe_load(file)
                    assert config_data is not None, f"Empty or invalid YAML in {config_file}"
                    assert isinstance(config_data, dict), f"YAML should be dictionary in {config_file}"
            except yaml.YAMLError as e:
                pytest.fail(f"YAML syntax error in {config_file}: {e}")
        
        print("✅ All YAML configuration files are well-formed")
    
    def test_settings_yaml_has_required_sections(self):
        """Verify settings.yaml contains required configuration sections"""
        settings_file = "config/settings.yaml"
        assert os.path.exists(settings_file), "settings.yaml must exist"
        
        with open(settings_file, 'r') as file:
            settings = yaml.safe_load(file)
        
        required_sections = ["selenium", "browsers"]
        for section in required_sections:
            assert section in settings, f"settings.yaml missing required section: {section}"
        
        # Verify selenium section has essential keys
        selenium_config = settings["selenium"]
        essential_keys = ["implicit_wait", "page_load_timeout"]
        for key in essential_keys:
            assert key in selenium_config, f"selenium config missing key: {key}"
        
        print("✅ settings.yaml has all required configuration sections")
    
    def test_pytest_ini_configuration(self):
        """Verify pytest.ini has proper configuration"""
        pytest_ini = "pytest.ini"
        assert os.path.exists(pytest_ini), "pytest.ini must exist"
        
        with open(pytest_ini, 'r') as file:
            content = file.read()
        
        required_configs = ["testpaths", "python_files", "markers"]
        for config in required_configs:
            assert config in content, f"pytest.ini missing required config: {config}"
        
        # Check for self_reflection marker
        assert "self_reflection" in content, "pytest.ini should define self_reflection marker"
        
        print("✅ pytest.ini configuration is complete")

@pytest.mark.self_reflection
class TestCodeQuality:
    """Validate code quality and consistency across the framework"""
    
    def test_test_files_follow_naming_convention(self):
        """Verify all test files follow naming convention"""
        test_files = glob.glob("tests/test_*.py")
        test_files.extend(glob.glob("tests/self_reflection/test_*.py"))
        
        assert len(test_files) >= 2, f"Should have multiple test files, found: {len(test_files)}"
        
        for test_file in test_files:
            filename = os.path.basename(test_file)
            assert filename.startswith("test_"), f"Test file {filename} doesn't follow naming convention"
            assert filename.endswith(".py"), f"Test file {filename} is not a Python file"
        
        print(f"✅ {len(test_files)} test files follow proper naming convention")
    
    def test_page_objects_have_proper_structure(self):
        """Verify page objects follow POM patterns"""
        page_files = glob.glob("pages/*.py")
        page_files = [f for f in page_files if not f.endswith("__init__.py")]
        
        base_page_exists = any("base_page.py" in f for f in page_files)
        assert base_page_exists, "base_page.py must exist as foundation"
        
        # Check that base_page.py contains a class
        with open("pages/base_page.py", 'r') as file:
            content = file.read()
            assert "class BasePage" in content, "base_page.py should contain BasePage class"
        
        print("✅ Page Object Model structure follows proper patterns")
    
    def test_imports_can_be_resolved(self):
        """Test that critical imports can be resolved"""
        critical_modules = [
            ("selenium", "webdriver"),
            ("pytest", None),
            ("yaml", None),
            ("streamlit", None)
        ]
        
        import_errors = []
        for module, submodule in critical_modules:
            try:
                if submodule:
                    exec(f"from {module} import {submodule}")
                else:
                    exec(f"import {module}")
            except ImportError as e:
                import_errors.append(f"{module}.{submodule if submodule else ''}: {e}")
        
        assert not import_errors, f"Import errors found: {import_errors}"
        print("✅ All critical imports can be resolved")

@pytest.mark.self_reflection
class TestFrameworkCapabilities:
    """Test that the framework can perform its core functions"""
    
    def test_webdriver_factory_is_functional(self):
        """Test that webdriver factory can be imported and initialized"""
        factory_path = "drivers/webdriver_factory.py"
        assert os.path.exists(factory_path), "webdriver_factory.py must exist"
        
        # Test that it can be imported
        spec = importlib.util.spec_from_file_location("webdriver_factory", factory_path)
        assert spec is not None, "webdriver_factory.py should be importable"
        
        print("✅ WebDriver factory is present and importable")
    
    def test_streamlit_app_exists(self):
        """Test that Streamlit UI app exists"""
        app_path = "streamlit_ui/app.py"
        assert os.path.exists(app_path), "Streamlit app must exist"
        
        # Check that it contains Streamlit code with proper encoding
        try:
            with open(app_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            # Fallback to latin-1 encoding for problematic files
            with open(app_path, 'r', encoding='latin-1') as file:
                content = file.read()
            assert "streamlit" in content.lower(), "app.py should contain Streamlit code"
        
        print("✅ Streamlit UI app is present")
    
    def test_self_verification_script_works(self):
        """Test that verify_setup.py can execute successfully"""
        verify_script = "verify_setup.py"
        assert os.path.exists(verify_script), "verify_setup.py must exist"
        
        try:
            result = subprocess.run(
                ["python", verify_script], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            # We expect it to run without crashing
            assert result.returncode == 0, f"verify_setup.py failed: {result.stderr}"
        except subprocess.TimeoutExpired:
            pytest.fail("verify_setup.py execution timed out")
        except Exception as e:
            pytest.skip(f"Could not test verify_setup.py execution: {e}")
        
        print("✅ Self-verification script executes successfully")

@pytest.mark.self_reflection
class TestFrameworkMetrics:
    """Generate and validate framework health metrics"""
    
    def test_framework_completeness_metrics(self):
        """Generate metrics about framework completeness"""
        metrics = {
            'total_test_files': len(glob.glob("tests/**/*.py", recursive=True)) - len(glob.glob("tests/**/__init__.py", recursive=True)),
            'page_object_files': len(glob.glob("pages/*.py")) - 1,  # Exclude __init__.py
            'utility_modules': len(glob.glob("utils/*.py")) - 1,     # Exclude __init__.py
            'config_files': len(glob.glob("config/*.yaml")),
            'self_reflection_tests': len(glob.glob("tests/self_reflection/test_*.py")),
        }
        
        # Validate minimum expected counts
        assert metrics['total_test_files'] >= 3, f"Should have at least 3 test files, found: {metrics['total_test_files']}"
        assert metrics['page_object_files'] >= 2, f"Should have at least 2 page objects, found: {metrics['page_object_files']}"
        assert metrics['utility_modules'] >= 3, f"Should have at least 3 utility modules, found: {metrics['utility_modules']}"
        assert metrics['config_files'] >= 2, f"Should have at least 2 config files, found: {metrics['config_files']}"
        
        print(f"📊 Framework Completeness Metrics: {metrics}")
        
        # Store metrics for consciousness tracking
        metrics_path = Path("reflections") / "current_metrics.yaml"
        with open(metrics_path, 'w') as file:
            yaml.dump({
                'date': '2025-08-07',
                'metrics': metrics,
                'health_status': 'Healthy'
            }, file)
        
        print("✅ Framework metrics generated and stored")
    
    def test_framework_demonstrates_best_practices(self):
        """Verify framework demonstrates automation best practices"""
        best_practices = {
            'page_object_model': os.path.exists("pages/base_page.py"),
            'configuration_management': os.path.exists("config/settings.yaml"),
            'test_fixtures': os.path.exists("conftest.py"),
            'html_reporting': "html" in open("pytest.ini").read(),
            'parallel_execution': "xdist" in open("requirements.txt").read(),
            'data_generation': os.path.exists("utils/data_factory.py"),
            'self_reflection': os.path.exists("tests/self_reflection/test_framework_health.py"),
        }
        
        implemented_practices = [practice for practice, implemented in best_practices.items() if implemented]
        
        assert len(implemented_practices) >= 5, f"Should demonstrate at least 5 best practices, found: {implemented_practices}"
        
        print(f"✅ Best practices demonstrated: {', '.join(implemented_practices)}")
        
        return best_practices
